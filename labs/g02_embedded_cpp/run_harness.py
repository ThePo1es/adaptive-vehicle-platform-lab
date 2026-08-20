# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["pyelftools==0.32"]
# ///
# ─── How to run ───
# uv run --with ziglang==0.15.2 labs/g02_embedded_cpp/run_harness.py

from __future__ import annotations

import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final, NamedTuple

from .elf_contract import (
    AbiVerification,
    ElfContractError,
    verify_abi_contract,
)
from .harness_toolchain import ToolchainError, compiler_prefix, resolve_compiler

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
LAB_ROOT: Final = REPO_ROOT / "labs/g02_embedded_cpp"
REFERENCE_ROOT: Final = LAB_ROOT / "reference"
INCLUDE_ROOT: Final = LAB_ROOT / "include"
FIXTURE_ROOT: Final = REPO_ROOT / "fixtures/g02"
TEST_ROOT: Final = LAB_ROOT / "tests"
FREESTANDING_ROOT: Final = LAB_ROOT / "freestanding"


class HarnessInputError(Exception):
    pass


class HarnessExecutionError(Exception):
    pass


class SprintSpec(NamedTuple):
    lab_id: str
    source: str
    test: str
    mutants: tuple[int, ...]
    exceptions: bool
    abi_analysis: bool = False


class CompileRequest(NamedTuple):
    compiler: Path
    sprint: SprintSpec
    source_root: Path
    output: Path
    mutant: int
    optimization: int
    retest: bool


class SprintRun(NamedTuple):
    compiler: Path
    sprint: SprintSpec
    source_root: Path
    reference: bool
    retest: bool


SPRINTS: Final = (
    SprintSpec("G2.1", "lifetime.cpp", "test_lifetime.cpp", (101, 102), True),
    SprintSpec("G2.2", "runtime.cpp", "test_runtime.cpp", (201, 202, 203), False),
    SprintSpec("G2.3", "queue.cpp", "test_queue.cpp", (301, 302), False),
    SprintSpec("G2.4", "abi.cpp", "test_abi.cpp", (401, 402, 403), False, True),
)


def select_sprints(lab_id: str) -> tuple[SprintSpec, ...]:
    if lab_id in {"G2.ALL", "G2.ENTRY"}:
        return SPRINTS if lab_id == "G2.ALL" else (SPRINTS[0],)
    selected = tuple(sprint for sprint in SPRINTS if sprint.lab_id == lab_id)
    if not selected:
        raise HarnessInputError(f"unknown G02_LAB_ID: {lab_id}")
    return selected


def parse_selection(lab_id: str) -> tuple[tuple[SprintSpec, ...], bool]:
    retest = lab_id.endswith(".RETEST")
    base = lab_id.removesuffix(".RETEST") if retest else lab_id
    if base == "G2":
        base = "G2.ALL"
    return select_sprints(base), retest


def resolve_source_root(candidate: Path) -> Path:
    resolved = candidate.resolve()
    if not resolved.is_relative_to(REPO_ROOT) or not resolved.is_dir():
        raise HarnessInputError(
            f"submission root must be an existing repository directory: {candidate}"
        )
    return resolved


def compile_binary(request: CompileRequest) -> None:
    source = request.source_root / request.sprint.source
    if not source.is_file():
        raise HarnessInputError(f"submission source is missing: {source}")
    command = [
        *compiler_prefix(request.compiler),
        "-std=c++20",
        f"-O{request.optimization}",
        "-g",
        "-Wall",
        "-Wextra",
        "-Wpedantic",
        "-Wconversion",
        "-Wsign-conversion",
        "-Wshadow",
        "-Werror",
        "-fsanitize=address,undefined",
        "-fno-omit-frame-pointer",
        f"-DG02_MUTANT={request.mutant}",
        f"-DG02_RETEST={int(request.retest)}",
        "-DG02_TESTING=1",
        f"-I{INCLUDE_ROOT}",
        f"-I{FIXTURE_ROOT}",
        f"-I{TEST_ROOT}",
    ]
    if not request.sprint.exceptions:
        command.extend(("-fno-exceptions", "-fno-rtti"))
    command.extend(
        (str(source), str(TEST_ROOT / request.sprint.test), "-o", str(request.output))
    )
    result = subprocess.run(command, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise HarnessExecutionError(
            f"compile failed for {request.sprint.lab_id} mutant={request.mutant}\n"
            + f"{result.stdout}{result.stderr}"
        )


def run_binary(output: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["ASAN_OPTIONS"] = "detect_leaks=0:halt_on_error=1"
    environment["UBSAN_OPTIONS"] = "halt_on_error=1"
    return subprocess.run(
        [str(output)],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )


def run_sprint(request: SprintRun) -> None:
    with tempfile.TemporaryDirectory(prefix=f"{request.sprint.lab_id.lower()}-") as temporary:
        build_root = Path(temporary)
        output = build_root / ("g02-test.exe" if os.name == "nt" else "g02-test")
        for optimization in (0, 2):
            compile_binary(
                CompileRequest(
                    request.compiler,
                    request.sprint,
                    request.source_root,
                    output,
                    0,
                    optimization,
                    request.retest,
                )
            )
            result = run_binary(output)
            if result.returncode != 0:
                raise HarnessExecutionError(
                    f"test failed for {request.sprint.lab_id} optimization={optimization}\n"
                    + f"{result.stdout}{result.stderr}"
                )
            case_set = "B" if request.retest else "A"
            print(
                f"PASS lab={request.sprint.lab_id} cases={case_set} "
                + f"optimization={optimization}"
            )
        if request.reference and not request.retest:
            for mutant in request.sprint.mutants:
                compile_binary(
                    CompileRequest(
                        request.compiler,
                        request.sprint,
                        request.source_root,
                        output,
                        mutant,
                        2,
                        False,
                    )
                )
                try:
                    mutant_result = run_binary(output)
                except subprocess.TimeoutExpired:
                    print(
                        f"PASS lab={request.sprint.lab_id} mutant={mutant} killed=timeout"
                    )
                    continue
                if mutant_result.returncode == 0:
                    raise HarnessExecutionError(
                        f"required mutant survived for {request.sprint.lab_id}: {mutant}"
                    )
                print(f"PASS lab={request.sprint.lab_id} mutant={mutant} killed")
            if request.sprint.abi_analysis:
                verify_abi_contract(
                    AbiVerification(
                        request.compiler,
                        INCLUDE_ROOT,
                        TEST_ROOT,
                        FREESTANDING_ROOT,
                        build_root,
                    )
                )


def main() -> int:
    try:
        selected, retest = parse_selection(os.environ.get("G02_LAB_ID", "G2.ALL"))
        submission = os.environ.get("G02_SUBMISSION_ROOT")
        source_root = resolve_source_root(Path(submission) if submission else REFERENCE_ROOT)
        compiler, identity = resolve_compiler()
        print(
            f"TOOLCHAIN python={platform.python_version()} compiler=zig-c++ "
            + f"version={identity.version} target_contract=native-x86_64-hosted-c++20"
        )
        for sprint in selected:
            run_sprint(
                SprintRun(
                    compiler,
                    sprint,
                    source_root,
                    source_root == REFERENCE_ROOT,
                    retest,
                )
            )
    except (
        ElfContractError,
        HarnessExecutionError,
        HarnessInputError,
        OSError,
        ToolchainError,
        subprocess.TimeoutExpired,
    ) as error:
        print(f"G2 harness: FAIL: {error}", file=sys.stderr)
        return 1
    print("G2 harness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
