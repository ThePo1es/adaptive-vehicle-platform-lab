from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from labs.g03_compiler_analysis.contracts import (
    AddressEvidence,
    AddressEvidenceError,
    DifferentialCase,
    IssueCandidate,
    compare_defined_cases,
    decide_issue_report,
    recover_link_address,
)
from labs.g03_compiler_analysis.toolchain import (
    GNU_ARCHIVES,
    ToolchainError,
    verify_gnu_archive,
)


def test_recover_link_address_when_build_id_and_load_bias_match() -> None:
    # Given: a PIE runtime address and its exact debug artifact identity.
    evidence = AddressEvidence("8a7d", "8a7d", 0x5555_0000, 0x5555_1234)

    # When: the address is converted back to the linked address.
    linked = recover_link_address(evidence)

    # Then: only the load bias is removed.
    assert linked == 0x1234


def test_recover_link_address_when_debug_build_id_is_wrong() -> None:
    # Given: a crash and a debug file from different builds.
    evidence = AddressEvidence("8a7d", "ffff", 0x4000, 0x4010)

    # When/Then: symbolization fails closed.
    with pytest.raises(AddressEvidenceError, match="build ID"):
        _ = recover_link_address(evidence)


def test_compare_defined_cases_when_ub_case_differs() -> None:
    # Given: equal defined results and a deliberately divergent UB observation.
    cases = (
        DifferentialCase("zero", True, 0, 0),
        DifferentialCase("max-signed-plus-one", False, -2147483648, 2147483647),
        DifferentialCase("boundary", True, 255, 255),
    )

    # When: equivalence is decided.
    result = compare_defined_cases(cases)

    # Then: UB is excluded rather than used as compiler-defect evidence.
    assert result.equivalent
    assert result.checked == 2
    assert result.excluded_ub == ("max-signed-plus-one",)


def test_compare_defined_cases_when_defined_result_differs() -> None:
    # Given: one defined input whose outputs disagree.
    cases = (DifferentialCase("boundary", True, 254, 255),)

    # When: equivalence is decided.
    result = compare_defined_cases(cases)

    # Then: the exact defined case is reported.
    assert not result.equivalent
    assert result.mismatches == ("boundary",)


def test_verify_gnu_archive_when_archive_hash_is_wrong(tmp_path: Path) -> None:
    # Given: a file named like the pinned archive but with untrusted contents.
    archive_name = next(iter(GNU_ARCHIVES))
    archive = tmp_path / archive_name
    _ = archive.write_bytes(b"not the official archive")
    observed = hashlib.sha256(archive.read_bytes()).hexdigest()

    # When/Then: the resolver refuses it and reports both hashes.
    with pytest.raises(ToolchainError, match=observed):
        _ = verify_gnu_archive(archive)


@pytest.mark.parametrize(
    ("candidate", "expected"),
    [
        (IssueCandidate(True, True, True, True, True), "READY_FOR_PEER_REVIEW"),
        (IssueCandidate(False, True, True, True, True), "STOP_SOURCE_CONTRACT"),
        (IssueCandidate(True, False, True, True, True), "STOP_REPRODUCTION"),
        (IssueCandidate(True, True, False, True, True), "STOP_REDUCTION"),
        (IssueCandidate(True, True, True, False, True), "STOP_EXPECTATION"),
        (IssueCandidate(True, True, True, True, False), "STOP_DUPLICATE_SEARCH"),
    ],
)
def test_decide_issue_report_with_positive_and_negative_controls(
    candidate: IssueCandidate,
    expected: str,
) -> None:
    # Given: one fully supported candidate or one missing prerequisite.
    # When: the local report gate is evaluated.
    decision = decide_issue_report(candidate)

    # Then: only the complete candidate reaches peer review.
    assert decision.value == expected
