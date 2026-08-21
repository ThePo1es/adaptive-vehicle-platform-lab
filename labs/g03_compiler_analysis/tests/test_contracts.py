from __future__ import annotations

import hashlib
import json
import os
import platform
import zipfile
from pathlib import Path

import pytest

from labs.g03_compiler_analysis.comparison_contract import (
    ComparisonError,
    load_cases,
    require_fair,
)
from labs.g03_compiler_analysis.contracts import (
    AddressEvidence,
    AddressEvidenceError,
    DifferentialCase,
    IssueCandidate,
    compare_defined_cases,
    decide_issue_report,
    recover_link_address,
)
from labs.g03_compiler_analysis.gnu_provision import (
    ProvisionError,
    provision,
    read_entry,
)
from labs.g03_compiler_analysis.toolchain import (
    MANIFEST_PATH,
    ToolchainError,
    verify_gnu_archive,
)

REPO_ROOT = Path(__file__).resolve().parents[3]


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
    archive_name = read_entry(MANIFEST_PATH)["filename"]
    archive = tmp_path / archive_name
    _ = archive.write_bytes(b"not the official archive")
    observed = hashlib.sha256(archive.read_bytes()).hexdigest()

    # When/Then: the resolver refuses it and reports both hashes.
    with pytest.raises(ToolchainError, match=observed):
        _ = verify_gnu_archive(archive)


def test_provision_rejects_archive_traversal(tmp_path: Path) -> None:
    # Given: a hash-matching archive whose member escapes the extraction root.
    source_archive = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(source_archive, "w") as bundle:
        bundle.writestr("../escape", "bad")
    digest = hashlib.sha256(source_archive.read_bytes()).hexdigest()
    archive = tmp_path / "cache" / digest / "unsafe.zip"
    archive.parent.mkdir(parents=True)
    source_archive.replace(archive)
    host = f"{'windows' if os.name == 'nt' else 'linux'}-{platform.machine().lower()}"
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"release": "test", "platforms": {host: {
        "url": "https://invalid.example/unsafe.zip", "filename": "unsafe.zip",
        "sha256": digest, "dumpmachine": "arm-none-eabi", "dumpfullversion": "14.3.1",
    }}}), encoding="utf-8")

    # When/Then: extraction fails before a path can escape.
    with pytest.raises(ProvisionError, match="unsafe GNU archive member"):
        _ = provision(manifest, tmp_path / "cache", download=False)


def test_comparison_profile_b_rejects_every_unfair_case() -> None:
    # Given: target, source/input, label, and cross-LTO drift controls.
    cases = load_cases(REPO_ROOT / "fixtures/g03/comparison-b.tsv")

    # When/Then: no mismatch can enter the comparison table.
    assert len(cases) == 4
    for case in cases:
        with pytest.raises(ComparisonError):
            require_fair(case)


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
