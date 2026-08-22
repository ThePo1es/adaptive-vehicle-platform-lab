from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import override


@dataclass(frozen=True, slots=True)
class AddressEvidence:
    binary_build_id: str
    debug_build_id: str
    load_bias: int
    runtime_address: int


@dataclass(frozen=True, slots=True)
class AddressEvidenceError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


def recover_link_address(evidence: AddressEvidence) -> int:
    if evidence.binary_build_id != evidence.debug_build_id:
        raise AddressEvidenceError("binary and debug build ID differ")
    if evidence.runtime_address < evidence.load_bias:
        raise AddressEvidenceError("runtime address is below load bias")
    return evidence.runtime_address - evidence.load_bias


@dataclass(frozen=True, slots=True)
class DifferentialCase:
    case_id: str
    defined: bool
    baseline: int
    optimized: int


@dataclass(frozen=True, slots=True)
class DifferentialResult:
    equivalent: bool
    checked: int
    excluded_ub: tuple[str, ...]
    mismatches: tuple[str, ...]


def compare_defined_cases(cases: tuple[DifferentialCase, ...]) -> DifferentialResult:
    defined = tuple(case for case in cases if case.defined)
    excluded = tuple(case.case_id for case in cases if not case.defined)
    mismatches = tuple(
        case.case_id for case in defined if case.baseline != case.optimized
    )
    return DifferentialResult(not mismatches, len(defined), excluded, mismatches)


@dataclass(frozen=True, slots=True)
class IssueCandidate:
    source_contract_defined: bool
    reproduced: bool
    reduced: bool
    expected_behavior_cited: bool
    duplicate_search_done: bool


class IssueDecision(StrEnum):
    READY_FOR_PEER_REVIEW = "READY_FOR_PEER_REVIEW"
    STOP_SOURCE_CONTRACT = "STOP_SOURCE_CONTRACT"
    STOP_REPRODUCTION = "STOP_REPRODUCTION"
    STOP_REDUCTION = "STOP_REDUCTION"
    STOP_EXPECTATION = "STOP_EXPECTATION"
    STOP_DUPLICATE_SEARCH = "STOP_DUPLICATE_SEARCH"


def decide_issue_report(candidate: IssueCandidate) -> IssueDecision:
    if not candidate.source_contract_defined:
        return IssueDecision.STOP_SOURCE_CONTRACT
    if not candidate.reproduced:
        return IssueDecision.STOP_REPRODUCTION
    if not candidate.reduced:
        return IssueDecision.STOP_REDUCTION
    if not candidate.expected_behavior_cited:
        return IssueDecision.STOP_EXPECTATION
    if not candidate.duplicate_search_done:
        return IssueDecision.STOP_DUPLICATE_SEARCH
    return IssueDecision.READY_FOR_PEER_REVIEW
