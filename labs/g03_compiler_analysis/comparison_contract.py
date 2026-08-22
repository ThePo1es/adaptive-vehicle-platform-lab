from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import override

TARGET = "cortex-m4/thumb/AAPCS32/soft-float"


@dataclass(frozen=True, slots=True)
class ComparisonError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class ComparisonCase:
    case_id: str
    gcc_target: str
    clang_target: str
    gcc_source_sha256: str
    clang_source_sha256: str
    gcc_input_sha256: str
    clang_input_sha256: str
    gcc_ir: str
    clang_ir: str
    lto_rank: str


def load_cases(path: Path) -> tuple[ComparisonCase, ...]:
    with path.open(encoding="utf-8", newline="") as stream:
        return tuple(ComparisonCase(**row) for row in csv.DictReader(stream, delimiter="\t"))


def require_fair(case: ComparisonCase) -> None:
    if case.gcc_target != TARGET or case.clang_target != TARGET:
        raise ComparisonError(f"{case.case_id}: target contract drift")
    if case.gcc_source_sha256 != case.clang_source_sha256:
        raise ComparisonError(f"{case.case_id}: source hash drift")
    if case.gcc_input_sha256 != case.clang_input_sha256:
        raise ComparisonError(f"{case.case_id}: input hash drift")
    if case.gcc_ir != "GIMPLE/RTL" or case.clang_ir != "LLVM IR":
        raise ComparisonError(f"{case.case_id}: intermediate representation mislabeled")
    if case.lto_rank != "not-compared":
        raise ComparisonError(f"{case.case_id}: cross-LTO ranking is forbidden")
