from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

from .comparison_contract import ComparisonError, load_cases, require_fair
from .defined_inputs import InputProfile
from .elf_checks import ElfExpectation, text_size, verify_elf
from .gnu_provision import compiler_environment
from .submission import source_file
from .toolchain import resolve_gnu

ARM_FLAGS = ("-mthumb", "-mfloat-abi=soft", "-ffreestanding", "-fno-builtin")


def _run(command: list[str], output: Path, environment: dict[str, str] | None = None) -> None:
    process_environment = os.environ.copy() if environment is None else environment.copy()
    cache = output.parent / "zig-cache"
    process_environment["ZIG_GLOBAL_CACHE_DIR"] = str(cache / "global")
    process_environment["ZIG_LOCAL_CACHE_DIR"] = str(cache / "local")
    result = subprocess.run(
        command,
        env=process_environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise ComparisonError("command failed: " + " ".join(command) + "\n" + result.stderr)
    if not output.is_file():
        raise ComparisonError(f"compiler did not create {output}")


def _reject_profile(fixtures: Path) -> str:
    cases = load_cases(fixtures / "comparison-b.tsv")
    rejected: list[str] = []
    for case in cases:
        try:
            require_fair(case)
        except ComparisonError:
            rejected.append(case.case_id)
    if len(rejected) != len(cases):
        raise ComparisonError("G3.4 mismatch profile accepted an unfair comparison")
    return f"PASS lab=G3.4 profile=B rejected={','.join(rejected)}"


def check_comparison(
    zig: Path,
    submission: Path,
    build: Path,
    fixtures: Path,
    profile: InputProfile,
) -> str:
    if profile == "B":
        return _reject_profile(fixtures)
    cases = load_cases(fixtures / "comparison-a.tsv")
    if len(cases) != 1:
        raise ComparisonError("G3.4 profile A must contain one comparable contract")
    require_fair(cases[0])
    source = source_file(submission, "fair_compiler_comparison.c")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    input_hash = hashlib.sha256((fixtures / "comparison-input.txt").read_bytes()).hexdigest()
    if input_hash != cases[0].gcc_input_sha256:
        raise ComparisonError("G3.4 comparison input hash differs from profile A")
    gnu = resolve_gnu()
    sizes: list[str] = []
    expectation = ElfExpectation("EM_ARM", (".text",), ("crc_step",))
    for optimization in ("O0", "O2", "Os"):
        clang_obj = build / f"g34-clang-{optimization}.o"
        gcc_obj = build / f"g34-gcc-{optimization}.o"
        common = ["-std=c17", *ARM_FLAGS, f"-{optimization}", "-c", str(source)]
        _run([str(zig), "cc", "-target", "thumb-freestanding-eabi", "-mcpu=cortex_m4", *common, "-o", str(clang_obj)], clang_obj)
        _run([str(gnu.compiler), "-mcpu=cortex-m4", *common, "-o", str(gcc_obj)], gcc_obj, compiler_environment())
        verify_elf(clang_obj, expectation)
        verify_elf(gcc_obj, expectation)
        sizes.append(f"{optimization}:clang={text_size(clang_obj)},gcc={text_size(gcc_obj)}")
    clang_ir = build / "g34-clang-O2.ll"
    _run([str(zig), "cc", "-target", "thumb-freestanding-eabi", "-mcpu=cortex_m4", "-std=c17", *ARM_FLAGS, "-O2", "-S", "-emit-llvm", str(source), "-o", str(clang_ir)], clang_ir)
    dump_obj = build / "g34-dump.o"
    _run([str(gnu.compiler), "-mcpu=cortex-m4", "-std=c17", *ARM_FLAGS, "-O2", "-fdump-tree-gimple", "-fdump-rtl-expand", "-c", str(source), "-o", str(dump_obj)], dump_obj, compiler_environment())
    if not tuple(build.glob("*.gimple")) or not tuple(build.glob("*.expand")):
        raise ComparisonError("G3.4 GCC GIMPLE or RTL dump is missing")
    return (
        f"PASS lab=G3.4 source_sha256={source_hash} input_sha256={input_hash} "
        + "target=cortex-m4/thumb/AAPCS32/soft-float "
        + f"profiles={' '.join(sizes)} clang_ir=LLVM gcc_ir=GIMPLE/RTL lto=not-compared"
    )
