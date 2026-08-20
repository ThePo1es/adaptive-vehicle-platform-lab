# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = []
# ///
# ─── How to run ───
# uv run labs/g01_safe_c/run_harness.py

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Final, NamedTuple

REPO_ROOT: Final = Path(__file__).resolve().parents[2]
LAB_ROOT: Final = REPO_ROOT / "labs/g01_safe_c"
REFERENCE_ROOT: Final = LAB_ROOT / "reference"
INCLUDE_ROOT: Final = LAB_ROOT / "include"
FIXTURE_ROOT: Final = REPO_ROOT / "fixtures/g01"
TEST_ROOT: Final = LAB_ROOT / "tests"


class HarnessInputError(Exception):
    detail: str

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class HarnessExecutionError(Exception):
    detail: str

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


class SprintSpec(NamedTuple):
    lab_id: str
    sources: tuple[str, ...]
    test: str
    mutants: tuple[int, ...]
    compile_fail_test: str | None = None


class CompileRequest(NamedTuple):
    compiler: Path
    sprint: SprintSpec
    source_root: Path
    output: Path
    mutant: int


class SprintRun(NamedTuple):
    compiler: Path
    sprint: SprintSpec
    source_root: Path
    reference: bool


SPRINTS: Final = (
    SprintSpec("G1.1", ("codec.c",), "test_codec.c", (1, 2, 3, 4)),
    SprintSpec("G1.2", ("codec.c",), "test_representation.c", (20,)),
    SprintSpec("G1.3", ("storage.c",), "test_storage.c", (30, 31), "invalid_zero_capacity.c"),
    SprintSpec("G1.4", ("parser.c",), "test_parser.c", (40, 41, 42, 43)),
    SprintSpec("G1.5", ("storage.c", "driver.c"), "test_driver.c", (50, 51, 52)),
)


def select_sprints(lab_id: str) -> tuple[SprintSpec, ...]:
    if lab_id == "G1.ALL":
        return SPRINTS
    if lab_id == "G1.ENTRY":
        return (SPRINTS[0],)
    selected = tuple(sprint for sprint in SPRINTS if sprint.lab_id == lab_id)
    if not selected:
        raise HarnessInputError(f"unknown G01_LAB_ID: {lab_id}")
    return selected


def resolve_source_root(candidate: Path) -> Path:
    resolved = candidate.resolve()
    if not resolved.is_relative_to(REPO_ROOT) or not resolved.is_dir():
        raise HarnessInputError(f"submission root must be an existing repository directory: {candidate}")
    return resolved


def resolve_compiler() -> Path:
    configured = os.environ.get("CC")
    discovered = shutil.which("clang")
    candidates = tuple(
        path
        for path in (
            Path(configured) if configured else None,
            Path(discovered) if discovered else None,
            Path("C:/Program Files/LLVM/bin/clang.exe"),
        )
        if path is not None
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise HarnessInputError("Clang 18 or newer was not found; set CC to the compiler path")


def compiler_prefix(compiler: Path) -> tuple[str, ...]:
    if compiler.name.lower() == "zig.exe":
        return (str(compiler), "cc")
    return (str(compiler),)


def compile_binary(request: CompileRequest) -> None:
    sources = tuple(str(request.source_root / name) for name in request.sprint.sources)
    missing = tuple(path for path in sources if not Path(path).is_file())
    if missing:
        raise HarnessInputError(f"submission source is missing: {', '.join(missing)}")
    command = (
        *compiler_prefix(request.compiler),
        "-std=c17",
        "-O1",
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
        f"-DG01_MUTANT={request.mutant}",
        f"-I{INCLUDE_ROOT}",
        f"-I{FIXTURE_ROOT}",
        f"-I{TEST_ROOT}",
        *sources,
        str(TEST_ROOT / request.sprint.test),
        "-o",
        str(request.output),
    )
    result = subprocess.run(command, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        diagnostic = result.stdout + result.stderr
        raise HarnessExecutionError(
            f"compile failed for {request.sprint.lab_id} mutant={request.mutant}\n{diagnostic}"
        )


def run_binary(output: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["ASAN_OPTIONS"] = "detect_leaks=0:halt_on_error=1"
    environment["UBSAN_OPTIONS"] = "halt_on_error=1"
    return subprocess.run(
        (str(output),),
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )


def verify_compile_failure(compiler: Path, sprint: SprintSpec, build_root: Path) -> None:
    if sprint.compile_fail_test is None:
        return
    result = subprocess.run(
        (
            *compiler_prefix(compiler),
            "-std=c17",
            "-Werror",
            f"-I{INCLUDE_ROOT}",
            str(TEST_ROOT / sprint.compile_fail_test),
            "-o",
            str(build_root / "invalid-capacity"),
        ),
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        raise HarnessExecutionError(f"compile-fail contract was accepted for {sprint.lab_id}")
    print(f"PASS lab={sprint.lab_id} compile-fail=zero-capacity")


def run_sprint(request: SprintRun) -> None:
    with tempfile.TemporaryDirectory(prefix=f"{request.sprint.lab_id.lower()}-") as temporary:
        build_root = Path(temporary)
        output = build_root / "g01-test"
        compile_binary(
            CompileRequest(request.compiler, request.sprint, request.source_root, output, 0)
        )
        result = run_binary(output)
        if result.returncode != 0:
            raise HarnessExecutionError(
                f"test failed for {request.sprint.lab_id}\n{result.stdout}{result.stderr}"
            )
        print(f"PASS lab={request.sprint.lab_id} public-cases")
        if request.reference:
            for mutant in request.sprint.mutants:
                compile_binary(
                    CompileRequest(
                        request.compiler,
                        request.sprint,
                        request.source_root,
                        output,
                        mutant,
                    )
                )
                mutant_result = run_binary(output)
                if mutant_result.returncode == 0:
                    raise HarnessExecutionError(
                        f"required mutant survived for {request.sprint.lab_id}: {mutant}"
                    )
                print(f"PASS lab={request.sprint.lab_id} mutant={mutant} killed")
            verify_compile_failure(request.compiler, request.sprint, build_root)


def main() -> int:
    try:
        lab_id = os.environ.get("G01_LAB_ID", "G1.ALL")
        submission = os.environ.get("G01_SUBMISSION_ROOT")
        source_root = resolve_source_root(Path(submission) if submission else REFERENCE_ROOT)
        compiler = resolve_compiler()
        for sprint in select_sprints(lab_id):
            run_sprint(SprintRun(compiler, sprint, source_root, source_root == REFERENCE_ROOT))
    except (HarnessInputError, HarnessExecutionError, OSError) as error:
        print(f"G1 harness: FAIL: {error}", file=sys.stderr)
        return 1
    print("G1 harness: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
