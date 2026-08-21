from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from scripts.runnable_evidence_replay import (
    LOCKED_TOOLCHAIN_ARGV_PREFIX,
    PINNED_G1_ARGV_PREFIX,
    PINNED_G1_MODULE,
    PINNED_G2_ARGV_PREFIX,
    PINNED_G2_MODULE,
    clean_verifier_environment,
    pinned_uv_version,
    repository_check_argv,
    run_binary_replay,
    verify_runtime,
)
from scripts.runnable_evidence_support import (
    REQUIRED_ROLES,
    canonical_output,
    digest,
    required_roles,
    translated_replay_argv,
)
from scripts.runnable_evidence_validator import (
    repository_check_identity,
    verify_artifacts,
    verify_command_shape,
    verify_retest_command_shape,
)


def test_inactive_manifest_requires_only_base_artifacts() -> None:
    assert required_roles("G1.1", False) == REQUIRED_ROLES


def test_active_g1_manifest_requires_replay_artifacts() -> None:
    roles = required_roles("G1.1", True)
    assert {"evidence-checker", "toolchain-lock", "toolchain-project", "unit-tests"} < roles


def test_active_g2_manifest_requires_cpp_replay_artifacts() -> None:
    roles = required_roles("G2.1", True)
    assert {
        "contract",
        "interface",
        "portfolio-build",
        "retest-fixture",
        "toolchain-lock",
        "toolchain-project",
    } < roles


def test_active_g2_abi_manifest_requires_c_and_elf_artifacts() -> None:
    roles = required_roles("G2.4", True)
    assert {
        "abi-corpus",
        "c-abi-header",
        "c-abi-validator",
        "consumer-main",
        "consumer-runner",
        "demo-c",
        "demo-cpp",
        "elf-inspector",
    } < roles


def test_active_g10_manifest_keeps_review_artifacts() -> None:
    roles = required_roles("G10.1", True)
    assert {
        "review-policy",
        "reviewer-registry",
        "source-lock",
        "toolchain-lock",
        "toolchain-project",
    } < roles


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


def test_historical_with_dependencies_replays_through_locked_toolchain() -> None:
    assert translated_replay_argv([*PINNED_G1_ARGV_PREFIX, PINNED_G1_MODULE]) == [
        *LOCKED_TOOLCHAIN_ARGV_PREFIX,
        PINNED_G1_MODULE,
    ]
    assert translated_replay_argv([*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE]) == [
        *LOCKED_TOOLCHAIN_ARGV_PREFIX,
        PINNED_G2_MODULE,
    ]


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


def test_schema_four_command_pins_cpp_and_elf_toolchains() -> None:
    command = {
        "argv": [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE],
        "environment": {"G02_LAB_ID": "G2.1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g02_embedded_cpp/run_harness.py"}}
    assert verify_command_shape(command, artifacts, 4) == (
        [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE],
        {"G02_LAB_ID": "G2.1"},
    )


def test_schema_five_command_uses_locked_g1_toolchain() -> None:
    command = {
        "argv": [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G1_MODULE],
        "environment": {"LAB_ID": "G1.1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g01_safe_c/run_harness.py"}}
    assert verify_command_shape(command, artifacts, 5) == (
        [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G1_MODULE],
        {"LAB_ID": "G1.1"},
    )


def test_schema_six_command_uses_locked_g2_toolchain() -> None:
    command = {
        "argv": [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G2_MODULE],
        "environment": {"G02_LAB_ID": "G2.1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g02_embedded_cpp/run_harness.py"}}
    assert verify_command_shape(command, artifacts, 6) == (
        [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G2_MODULE],
        {"G02_LAB_ID": "G2.1"},
    )


def test_sealed_toolchain_role_rejects_a_different_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    expected_file = tmp_path / "expected"
    expected_file.write_bytes(b"sealed")
    monkeypatch.setattr(
        "scripts.runnable_evidence_validator.required_roles",
        lambda _lab_id, _active: {"toolchain-lock", "toolchain-project"},
    )
    monkeypatch.setattr(
        "scripts.runnable_evidence_validator.git_bytes",
        lambda _starter, _path: b"sealed",
    )
    monkeypatch.setattr(
        "scripts.runnable_evidence_validator.repository_path",
        lambda _path: expected_file,
    )
    manifest = {
        "lab_id": "G1.1",
        "artifacts": [
            {
                "role": "toolchain-lock",
                "path": "fixtures/not-the-lock.txt",
                "sha256": digest(b"sealed"),
            },
            {
                "role": "toolchain-project",
                "path": "toolchain/pyproject.toml",
                "sha256": digest(b"sealed"),
            },
        ],
    }

    with pytest.raises(ValueError, match="toolchain-lock must use toolchain/uv.lock"):
        _ = verify_artifacts(manifest, "a" * 40, True)


def test_active_g2_retest_command_requires_lab_specific_b_input() -> None:
    command = {
        "argv": [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE],
        "environment": {
            "G02_LAB_ID": "G2.1.RETEST",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g02_embedded_cpp/run_harness.py"}}
    assert verify_retest_command_shape(command, artifacts, "G2.1") == (
        [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE],
        {"G02_LAB_ID": "G2.1.RETEST", "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_active_g1_locked_retest_requires_lab_specific_b_input() -> None:
    command = {
        "argv": [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G1_MODULE],
        "environment": {
            "G01_LAB_ID": "G1.1.RETEST",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g01_safe_c/run_harness.py"}}
    assert verify_retest_command_shape(command, artifacts, "G1.1", 5) == (
        [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G1_MODULE],
        {"G01_LAB_ID": "G1.1.RETEST", "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_active_g2_retest_command_rejects_a_input() -> None:
    command = {
        "argv": [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE],
        "environment": {"G02_LAB_ID": "G2.1", "PYTHONDONTWRITEBYTECODE": "1"},
        "expected_exit": 0,
        "observed_exit": 0,
    }
    artifacts = {"runner": {"path": "labs/g02_embedded_cpp/run_harness.py"}}
    with pytest.raises(ValueError, match="B input"):
        _ = verify_retest_command_shape(command, artifacts, "G2.1")


def test_uv_version_accepts_official_build_metadata() -> None:
    assert pinned_uv_version("uv 0.12.3")
    assert pinned_uv_version("uv 0.12.3 (507230998 2026-08-07 x86_64-pc-windows-msvc)")
    assert not pinned_uv_version("uv 0.12.4")


def test_replay_drops_parent_uv_environment_paths() -> None:
    assert clean_verifier_environment(
        {
            "PATH": "tools",
            "UV_PROJECT_ENVIRONMENT": "C:/parent/toolchain/.venv",
            "VIRTUAL_ENV": "C:/parent/toolchain/.venv",
        }
    ) == {"PATH": "tools"}


def test_runtime_probe_does_not_reuse_manifest_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    observed: list[dict[str, str]] = []
    observed_argv: list[list[str]] = []

    def probe(
        argv: list[str],
        *,
        cwd: Path,
        environment: dict[str, str],
        label: str,
    ) -> subprocess.CompletedProcess[str]:
        _ = cwd
        observed.append(environment)
        observed_argv.append(argv)
        if label == "Python version probe":
            return subprocess.CompletedProcess(
                argv,
                0,
                stdout="",
                stderr="Python 3.12.13\n",
            )
        return subprocess.CompletedProcess(argv, 0, stdout="uv 0.12.3\n", stderr="")

    monkeypatch.setenv("VIRTUAL_ENV", "C:/parent/toolchain/.venv")
    monkeypatch.setattr("scripts.runnable_evidence_replay.run_text_probe", probe)
    verify_runtime(
        tmp_path,
        {
            "schema_version": 3,
            "environment": {
                "python": "3.12.13",
                "uv": "0.12.3",
                "c_compiler": "zig",
                "c_compiler_version": "0.15.2",
                "c_runtime": "Zig 0.15.2 bundled libc",
                "target_contract": "native x86_64 hosted C17",
                "replay_targets": ["x86_64-unknown-windows-gnu"],
            },
        },
    )

    assert len(observed) == 2
    assert observed_argv[0] == [*LOCKED_TOOLCHAIN_ARGV_PREFIX[:-1], "--version"]
    assert all("VIRTUAL_ENV" not in environment for environment in observed)
    assert all(
        isinstance(key, str) and isinstance(value, str)
        for environment in observed
        for key, value in environment.items()
    )


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


def test_repository_check_identity_deduplicates_only_identical_replays() -> None:
    manifest = {
        "starter_commit": "a" * 40,
        "repository_check": {
            "stdout_sha256": "b" * 64,
            "stderr_sha256": "c" * 64,
        },
    }
    identity = repository_check_identity(manifest)
    changed: dict[str, object] = {
        "starter_commit": "a" * 40,
        "repository_check": {
            "stdout_sha256": "d" * 64,
            "stderr_sha256": "c" * 64,
        },
    }
    assert identity == ("a" * 40, "b" * 64, "c" * 64)
    assert repository_check_identity(changed) != identity


def test_binary_replay_converts_timeout_to_bounded_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def raise_timeout(*_args: object, **_kwargs: object) -> None:
        raise subprocess.TimeoutExpired(["example"], 180)

    monkeypatch.setattr("scripts.runnable_evidence_replay.subprocess.run", raise_timeout)
    with pytest.raises(ValueError, match="primary replay exceeded"):
        _ = run_binary_replay(
            ["example"],
            cwd=tmp_path,
            environment={},
            label="primary replay",
        )
