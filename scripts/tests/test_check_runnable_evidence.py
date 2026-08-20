from __future__ import annotations

from pathlib import Path

import pytest

from scripts.runnable_evidence_replay import (
    PINNED_G1_ARGV_PREFIX,
    PINNED_G1_MODULE,
    pinned_uv_version,
    repository_check_argv,
)
from scripts.runnable_evidence_support import (
    REQUIRED_ROLES,
    canonical_output,
    required_roles,
)
from scripts.runnable_evidence_validator import verify_command_shape


def test_inactive_manifest_requires_only_base_artifacts() -> None:
    assert required_roles("G1.1", False) == REQUIRED_ROLES


def test_active_g1_manifest_requires_replay_artifacts() -> None:
    roles = required_roles("G1.1", True)
    assert {"evidence-checker", "unit-tests"} < roles


def test_active_g10_manifest_keeps_review_artifacts() -> None:
    roles = required_roles("G10.1", True)
    assert {"review-policy", "reviewer-registry", "source-lock"} < roles


def test_unknown_active_lab_has_no_implicit_policy() -> None:
    with pytest.raises(ValueError, match="no active artifact policy"):
        _ = required_roles("G12.1", True)


def test_command_shape_requires_hashed_python_runner() -> None:
    command = {
        "argv": ["python3", "labs/example/run_harness.py"],
        "environment": {"LAB_ID": "G1.1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/example/run_harness.py"}}
    assert verify_command_shape(command, artifacts) == (
        ["python3", "labs/example/run_harness.py"],
        {"LAB_ID": "G1.1"},
    )


def test_schema_three_command_pins_uv_python_and_zig() -> None:
    command = {
        "argv": [*PINNED_G1_ARGV_PREFIX, PINNED_G1_MODULE],
        "environment": {"LAB_ID": "G1.1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g01_safe_c/run_harness.py"}}
    assert verify_command_shape(command, artifacts, 3) == (
        [*PINNED_G1_ARGV_PREFIX, PINNED_G1_MODULE],
        {"LAB_ID": "G1.1"},
    )


def test_uv_version_accepts_official_build_metadata() -> None:
    assert pinned_uv_version("uv 0.12.3")
    assert pinned_uv_version("uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)")
    assert not pinned_uv_version("uv 0.12.4")


def test_text_evidence_has_platform_independent_newlines() -> None:
    assert canonical_output(b"first\r\nsecond\r\n") == b"first\nsecond\n"


def test_windows_repository_check_uses_explicit_git_bash(tmp_path: Path) -> None:
    bash = tmp_path / "bash.exe"
    bash.touch()
    assert repository_check_argv("nt", {"GIT_BASH_EXE": str(bash)}) == [
        str(bash),
        "-c",
        "hash -p /usr/bin/bash bash; source scripts/check_repo.sh",
    ]


def test_windows_repository_check_rejects_missing_git_bash() -> None:
    with pytest.raises(ValueError, match="GIT_BASH_EXE"):
        _ = repository_check_argv("nt", {})


def test_posix_repository_check_keeps_recorded_command() -> None:
    assert repository_check_argv("posix", {}) == ["bash", "scripts/check_repo.sh"]
