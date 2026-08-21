# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["pyelftools==0.32"]
# ///
# ─── How to run ───
# uv run --with ziglang==0.15.2 --with pyelftools==0.32 python -m labs.g03_compiler_analysis.run_harness

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final

from .answers import AnswerError, parse_answers, verify_issue_answers
from .comparison_contract import ComparisonError
from .compiler_compare import check_comparison
from .contracts import (
    AddressEvidence,
    AddressEvidenceError,
    recover_link_address,
)
from .defined_inputs import (
    DefinedInputError,
    InputProfile,
    load_input_set,
    render_driver,
)
from .elf_checks import ElfCheckError, ElfExpectation, verify_elf
from .submission import SubmissionError, resolve_submission, source_file
from .toolchain import (
    PINNED_CLANG_VERSION,
    ToolchainError,
    resolve_zig,
)

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
LAB_ROOT: Final = REPO_ROOT / "labs/g03_compiler_analysis"
REFERENCE_ROOT: Final = LAB_ROOT / "reference"
FIXTURE_ROOT: Final = REPO_ROOT / "fixtures/g03"
ARM_CONTRACT_FLAGS: Final = (
    "-mthumb",
    "-mfloat-abi=soft",
    "-ffreestanding",
    "-fno-builtin",
)
ZIG_ARM_FLAGS: Final = ("-mcpu=cortex_m4", *ARM_CONTRACT_FLAGS)
COMMAND_TIMEOUT_SECONDS: Final = 240


class HarnessError(Exception):
    pass


def run(
    command: list[str],
    output: Path | None = None,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy() if environment is None else environment.copy()
    if output is not None:
        repo_key = hashlib.sha256(str(REPO_ROOT).encode("utf-8")).hexdigest()[:12]
        global_cache = Path(
            os.environ.get(
                "G03_ZIG_CACHE",
                str(Path(tempfile.gettempdir()) / f"g03-zig-cache-{repo_key}"),
            )
        )
        local_cache = output.parent / "zig-cache" / "local"
        global_cache.mkdir(parents=True, exist_ok=True)
        local_cache.mkdir(parents=True, exist_ok=True)
        environment["ZIG_GLOBAL_CACHE_DIR"] = str(global_cache)
        environment["ZIG_LOCAL_CACHE_DIR"] = str(local_cache)
    try:
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise HarnessError(
            f"command timed out after {COMMAND_TIMEOUT_SECONDS}s: {' '.join(command)}"
        ) from error
    if result.returncode != 0:
        raise HarnessError("command failed: " + " ".join(command) + "\n" + result.stderr)
    if output is not None and not output.is_file():
        raise HarnessError(f"compiler did not create {output}")
    return result


def zig_cc(zig: Path) -> list[str]:
    return [str(zig), "cc"]


def check_g31(zig: Path, root: Path, build: Path) -> None:
    source = source_file(root, "arm32_call_path.c")
    obj = build / "g31.o"
    asm = build / "g31.s"
    base = [*zig_cc(zig), "-target", "thumb-freestanding-eabi", *ZIG_ARM_FLAGS]
    _ = run([*base, "-O0", "-g", "-c", str(source), "-o", str(obj)], obj)
    _ = run([*base, "-O0", "-S", str(source), "-o", str(asm)], asm)
    verify_elf(obj, ElfExpectation("EM_ARM", (".debug_info",), ("mix4", "call_mix4")))
    assembly = asm.read_text(encoding="utf-8")
    if "mix4" not in assembly or ("bl\tmix4" not in assembly and "bl mix4" not in assembly):
        raise HarnessError("G3.1 call site does not preserve a real mix4 call")
    print("PASS lab=G3.1 target=thumb cortex-m4 abi=AAPCS32 float=soft")


def check_g32(zig: Path, root: Path, build: Path) -> None:
    source = source_file(root, "aarch64_error_recovery.c")
    obj = build / "g32.o"
    _ = run(
        [
            *zig_cc(zig),
            "-target",
            "aarch64-freestanding",
            "-fPIC",
            "-g",
            "-c",
            str(source),
            "-o",
            str(obj),
        ],
        obj,
    )
    verify_elf(
        obj,
        ElfExpectation(
            "EM_AARCH64",
            (".debug_info", ".rela.text", ".symtab"),
            ("recover_signal", "vehicle_scale"),
        ),
    )
    answers = parse_answers(source_file(root, "aarch64_error_recovery.answers"))
    evidence = AddressEvidence(
        answers["binary_build_id"],
        answers["debug_build_id"],
        int(answers["load_bias"], 0),
        int(answers["runtime_address"], 0),
    )
    if recover_link_address(evidence) != int(answers["link_address"], 0):
        raise HarnessError("G3.2 load-bias address recovery is wrong")
    if answers["external_call_path"] != "call-relocation->PLT->GOT":
        raise HarnessError("G3.2 PLT/GOT call path is wrong")
    if answers["dwarf_role"] != "link-address-to-source":
        raise HarnessError("G3.2 DWARF role is wrong")
    print("PASS lab=G3.2 target=aarch64 load-bias/build-id/DWARF/PLT-GOT")


def check_g33(zig: Path, root: Path, build: Path, profile: InputProfile) -> None:
    source = source_file(root, "c_to_ir_to_machine.c")
    ir = build / "g33.ll"
    asm = build / "g33.s"
    cross = [*zig_cc(zig), "-target", "thumb-freestanding-eabi", *ZIG_ARM_FLAGS]
    _ = run([*cross, "-O2", "-S", "-emit-llvm", str(source), "-o", str(ir)], ir)
    _ = run(
        [*cross, "-O2", "-DG03_ORACLE=1", "-S", str(source), "-o", str(asm)],
        asm,
    )
    ir_text = ir.read_text(encoding="utf-8")
    if "target triple = \"thumb" not in ir_text or "define" not in ir_text:
        raise HarnessError("G3.3 LLVM IR target or function is missing")
    input_set = load_input_set(FIXTURE_ROOT, profile)
    driver = build / "g33-driver.c"
    _ = driver.write_text(render_driver(input_set), encoding="utf-8")
    observed: list[str] = []
    for optimization in ("O0", "O2"):
        executable = build / f"g33-{optimization}{'.exe' if os.name == 'nt' else ''}"
        host_link = (
            [
                "-target", "x86_64-windows-gnu", "-fno-sanitize=all", "-nostdlib",
                "-Wl,--entry,mainCRTStartup", "-lkernel32",
            ]
            if os.name == "nt"
            else []
        )
        _ = run(
            [
                *zig_cc(zig),
                *host_link,
                "-std=c17",
                f"-{optimization}",
                str(source),
                str(driver),
                "-o",
                str(executable),
            ],
            executable,
        )
        _ = run([str(executable)])
        case_ids = ",".join(case.case_id for case in input_set.defined)
        observed.append(f"{optimization}:[{case_ids}]")
    print(
        f"PASS lab=G3.3 profile={profile} defined-inputs={len(input_set.defined)} "
        + f"excluded-ub={','.join(input_set.excluded_ub)} "
        + f"executed={' '.join(observed)} ir=LLVM machine=thumb"
    )


def check_g34(zig: Path, root: Path, build: Path, profile: InputProfile) -> None:
    print(check_comparison(zig, root, build, FIXTURE_ROOT, profile))


def check_g35(root: Path) -> None:
    _ = verify_issue_answers(root)
    print("PASS lab=G3.5 controls=positive+negative decision=READY_FOR_PEER_REVIEW upstream=false")


def main() -> int:
    try:
        requested = os.environ.get("G03_LAB_ID", "G3.ALL")
        profile: InputProfile = "B" if requested.endswith(".RETEST") else "A"
        selection = requested.removesuffix(".RETEST")
        root = resolve_submission(
            os.environ.get("G03_SUBMISSION_ROOT"),
            os.environ.get("G03_TRUSTED_LOCAL_EXECUTION"),
            REFERENCE_ROOT,
        )
        print(
            f"TOOLCHAIN python={platform.python_version()} zig=0.15.2 "
            + f"clang={PINNED_CLANG_VERSION} target-contract=per-lab"
        )
        with tempfile.TemporaryDirectory(prefix=".g03-", dir=REPO_ROOT) as temporary:
            build = Path(temporary)
            zig = resolve_zig()
            checks = {
                "G3.1": lambda: check_g31(zig, root, build),
                "G3.2": lambda: check_g32(zig, root, build),
                "G3.3": lambda: check_g33(zig, root, build, profile),
                "G3.4": lambda: check_g34(zig, root, build, profile),
                "G3.5": lambda: check_g35(root),
            }
            selected = tuple(checks) if selection in {"G3", "G3.ALL"} else (selection,)
            for lab_id in selected:
                if lab_id not in checks:
                    raise HarnessError(f"unknown G03_LAB_ID: {selection}")
                checks[lab_id]()
    except (
        AnswerError,
        AddressEvidenceError,
        ComparisonError,
        DefinedInputError,
        ElfCheckError,
        HarnessError,
        OSError,
        subprocess.SubprocessError,
        SubmissionError,
        ToolchainError,
    ) as error:
        print(f"G3 harness: FAIL: {error}", file=sys.stderr)
        return 1
    print("G3 harness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
