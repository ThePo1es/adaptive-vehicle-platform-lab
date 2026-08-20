from __future__ import annotations

import pytest

from scripts.runnable_evidence_support import (
    REQUIRED_ROLES,
    canonical_output,
    required_roles,
)
from scripts.runnable_evidence_validator import (
    PINNED_G1_ARGV_PREFIX,
    PINNED_G1_MODULE,
    verify_command_shape,
)


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


def test_text_evidence_has_platform_independent_newlines() -> None:
    assert canonical_output(b"first\r\nsecond\r\n") == b"first\nsecond\n"
