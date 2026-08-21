# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["pyelftools==0.32"]
# ///
# ─── How to run ───
# uv run --with ziglang==0.15.2 --with pyelftools==0.32 python -m labs.g03_compiler_analysis.run_harness

from __future__ import annotations

import csv
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final

from .answers import AnswerError, parse_answers, verify_issue_answers
from .contracts import (
    AddressEvidence,
    AddressEvidenceError,
    DifferentialCase,
    compare_defined_cases,
    recover_link_address,
)
from .elf_checks import ElfCheckError, ElfExpectation, text_size, verify_elf
from .submission import SubmissionError, resolve_submission, source_file
from .toolchain import (
    PINNED_CLANG_VERSION,
    ToolchainError,
    resolve_gnu,
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
GNU_ARM_FLAGS: Final = ("-mcpu=cortex-m4", *ARM_CONTRACT_FLAGS)


class HarnessError(Exception):
    pass


def run(command: list[str], output: Path | None = None) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    if output is not None:
        cache = output.parent / "zig-cache"
        environment["ZIG_GLOBAL_CACHE_DIR"] = str(cache / "global")
        environment["ZIG_LOCAL_CACHE_DIR"] = str(cache / "local")
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
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


def check_g33(zig: Path, root: Path, build: Path) -> None:
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
    cases: list[DifferentialCase] = []
    for fixture in (FIXTURE_ROOT / "input-a.tsv", FIXTURE_ROOT / "input-b.tsv"):
        with fixture.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                cases.append(
                    DifferentialCase(
                        row["case"],
                        row["defined"] == "true",
                        int(row["baseline"]),
                        int(row["optimized"]),
                    )
                )
    differential = compare_defined_cases(tuple(cases))
    if not differential.equivalent or differential.checked != 4:
        raise HarnessError(f"G3.3 defined-input differential failed: {differential}")
    if len(differential.excluded_ub) != 2:
        raise HarnessError("G3.3 UB observations were not excluded")
    print("PASS lab=G3.3 defined-inputs=4 ub-observations=2-excluded ir=LLVM machine=thumb")


def check_g34(zig: Path, root: Path, build: Path) -> None:
    source = source_file(root, "fair_compiler_comparison.c")
    clang_obj = build / "g34-clang.o"
    _ = run(
        [
            *zig_cc(zig),
            "-target",
            "thumb-freestanding-eabi",
            *ZIG_ARM_FLAGS,
            "-O2",
            "-c",
            str(source),
            "-o",
            str(clang_obj),
        ],
        clang_obj,
    )
    verify_elf(clang_obj, ElfExpectation("EM_ARM", (".text",), ("crc_step",)))
    try:
        gnu = resolve_gnu()
    except ToolchainError as error:
        print(f"PROVISIONAL lab=G3.4 reason={error}")
        return
    gnu_obj = build / "g34-gcc.o"
    _ = run(
        [str(gnu.compiler), *GNU_ARM_FLAGS, "-O2", "-c", str(source), "-o", str(gnu_obj)],
        gnu_obj,
    )
    verify_elf(gnu_obj, ElfExpectation("EM_ARM", (".text",), ("crc_step",)))
    print(f"PASS lab=G3.4 clang_text={text_size(clang_obj)} gcc_text={text_size(gnu_obj)}")


def check_g35(root: Path) -> None:
    _ = verify_issue_answers(root)
    print("PASS lab=G3.5 controls=positive+negative decision=READY_FOR_PEER_REVIEW upstream=false")


def main() -> int:
    try:
        selection = os.environ.get("G03_LAB_ID", "G3.ALL").removesuffix(".RETEST")
        root = resolve_submission(
            os.environ.get("G03_SUBMISSION_ROOT"),
            os.environ.get("G03_TRUSTED_LOCAL_EXECUTION"),
            REFERENCE_ROOT,
        )
        print(
            f"TOOLCHAIN python={platform.python_version()} zig=0.15.2 "
            + f"clang={PINNED_CLANG_VERSION} target-contract=per-lab"
        )
        with tempfile.TemporaryDirectory(prefix="g03-") as temporary:
            build = Path(temporary)
            zig = resolve_zig()
            checks = {
                "G3.1": lambda: check_g31(zig, root, build),
                "G3.2": lambda: check_g32(zig, root, build),
                "G3.3": lambda: check_g33(zig, root, build),
                "G3.4": lambda: check_g34(zig, root, build),
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
        ElfCheckError,
        HarnessError,
        OSError,
        SubmissionError,
        ToolchainError,
    ) as error:
        print(f"G3 harness: FAIL: {error}", file=sys.stderr)
        return 1
    print("G3 harness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
