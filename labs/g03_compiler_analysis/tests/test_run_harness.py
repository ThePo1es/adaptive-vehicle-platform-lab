from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_g35_reference_when_run_through_cli() -> None:
    # Given: the checked-in positive-control issue analysis.
    environment = {**os.environ, "G03_LAB_ID": "G3.5"}

    # When: a learner invokes the real module entry point.
    result = subprocess.run(
        [sys.executable, "-m", "labs.g03_compiler_analysis.run_harness"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    # Then: the local peer-review decision passes without claiming submission.
    assert result.returncode == 0, result.stderr
    assert "upstream=false" in result.stdout
    assert "G3 harness: PASS" in result.stdout


def test_g35_starter_when_run_through_cli() -> None:
    # Given: the negative-control starter and explicit local execution consent.
    environment = {
        **os.environ,
        "G03_LAB_ID": "G3.5",
        "G03_SUBMISSION_ROOT": str(REPO_ROOT / "labs/g03_compiler_analysis/starter"),
        "G03_TRUSTED_LOCAL_EXECUTION": "1",
    }

    # When: the real module entry point evaluates it.
    result = subprocess.run(
        [sys.executable, "-m", "labs.g03_compiler_analysis.run_harness"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    # Then: the incomplete analysis is rejected.
    assert result.returncode == 1
    assert "not ready for local peer review" in result.stderr


@pytest.mark.parametrize(("lab_id", "profile"), [("G3.3", "A"), ("G3.3.RETEST", "B")])
def test_g33_executes_only_requested_public_profile(lab_id: str, profile: str) -> None:
    # Given: the normal or independent retest entry point.
    environment = {**os.environ, "G03_LAB_ID": lab_id}

    # When: the real learner function is compiled and executed at both levels.
    result = subprocess.run(
        [sys.executable, "-m", "labs.g03_compiler_analysis.run_harness"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )

    # Then: exactly the selected profile supplies the independent expected values.
    assert result.returncode == 0, result.stderr
    assert f"profile={profile}" in result.stdout
    assert ("zero-limit" in result.stdout) is (profile == "A")
    assert ("one-slot" in result.stdout) is (profile == "B")


def test_g34_missing_verified_archive_fails_closed(tmp_path: Path) -> None:
    # Given: an empty GNU cache rather than a PATH or root override.
    environment = {**os.environ, "G03_LAB_ID": "G3.4", "G03_GNU_CACHE": str(tmp_path)}

    # When: the comparison is requested explicitly.
    result = subprocess.run(
        [sys.executable, "-m", "labs.g03_compiler_analysis.run_harness"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )

    # Then: it is a hard failure and never reports an overall pass.
    assert result.returncode != 0
    assert "verified GNU archive is absent" in result.stderr
    assert "G3 harness: PASS" not in result.stdout


@pytest.mark.parametrize(
    ("lab_id", "mutant", "target"),
    [
        ("G3.1", "101_missing_call.c", "arm32_call_path.c"),
        ("G3.2", "201_hidden_symbol.c", "aarch64_error_recovery.c"),
        ("G3.3", "301_wrong_boundary.c", "c_to_ir_to_machine.c"),
        ("G3.3.RETEST", "302_bypass_function.c", "c_to_ir_to_machine.c"),
        ("G3.4", "401_missing_crc.c", "fair_compiler_comparison.c"),
        ("G3.5", "501_fake_upstream.answers", "compiler_issue_decision.answers"),
    ],
)
def test_required_mutant_when_run_through_cli(
    tmp_path: Path,
    lab_id: str,
    mutant: str,
    target: str,
) -> None:
    # Given: a reference submission with exactly one required defect injected.
    submission = tmp_path / "submission"
    lab_root = REPO_ROOT / "labs/g03_compiler_analysis"
    _ = shutil.copytree(lab_root / "reference", submission)
    _ = shutil.copy2(lab_root / "mutants" / mutant, submission / target)
    environment = {
        **os.environ,
        "G03_LAB_ID": lab_id,
        "G03_SUBMISSION_ROOT": str(submission),
        "G03_TRUSTED_LOCAL_EXECUTION": "1",
    }

    # When: the real public oracle evaluates the single mutant.
    result = subprocess.run(
        [sys.executable, "-m", "labs.g03_compiler_analysis.run_harness"],
        cwd=REPO_ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )

    # Then: every required mutant is killed.
    assert result.returncode == 1, result.stdout
    assert "G3 harness: FAIL" in result.stderr
