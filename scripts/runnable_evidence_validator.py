from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from scripts.runnable_evidence_replay import (
    LOCKED_TOOLCHAIN_ARGV_PREFIX,
    PINNED_G1_ARGV_PREFIX,
    PINNED_G1_MODULE,
    PINNED_G2_ARGV_PREFIX,
    PINNED_G2_MODULE,
    recorded_command_stdout,
    replay_environment,
    run_binary_replay,
    verify_output,
    verify_repository_check,
    verify_runtime,
)

SEALED_ROLE_PATHS = {
    "toolchain-lock": "toolchain/uv.lock",
    "toolchain-project": "toolchain/pyproject.toml",
}
from scripts.runnable_evidence_support import (
    FULL_SHA,
    REPO_ROOT,
    SHA256,
    archive_starter,
    digest,
    fail,
    git_bytes,
    repository_path,
    required_roles,
    run_git,
    translated_replay_argv,
    verify_sprint_lock,
)


def verify_artifacts(
    manifest: dict[str, Any],
    starter: str,
    active: bool,
) -> dict[str, dict[str, str]]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        fail("artifacts must be a list")
    by_role: dict[str, dict[str, str]] = {}
    paths: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            fail("artifact entry must be an object")
        role = artifact.get("role")
        relative_path = artifact.get("path")
        expected = artifact.get("sha256")
        if not isinstance(role, str) or not role or role in by_role:
            fail(f"artifact role is missing or duplicated: {role}")
        if not isinstance(relative_path, str) or not relative_path or relative_path in paths:
            fail(f"artifact path is missing or duplicated: {relative_path}")
        sealed_path = SEALED_ROLE_PATHS.get(role)
        if sealed_path is not None and relative_path != sealed_path:
            fail(f"{role} must use {sealed_path}")
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            fail(f"artifact sha256 is invalid: {relative_path}")
        if digest(git_bytes(starter, relative_path)) != expected:
            fail(f"starter artifact hash does not match manifest: {relative_path}")
        if active:
            current = repository_path(relative_path)
            if not current.is_file() or digest(current.read_bytes()) != expected:
                fail(f"active artifact hash drifted: {relative_path}")
        by_role[role] = artifact
        paths.add(relative_path)
    missing = required_roles(manifest["lab_id"], active) - set(by_role)
    if missing:
        fail(f"required artifact roles are missing: {', '.join(sorted(missing))}")
    return by_role


def verify_command_shape(
    command: dict[str, Any],
    artifacts: dict[str, dict[str, str]],
    schema_version: int = 2,
) -> tuple[list[str], dict[str, str]]:
    argv_value = command.get("argv")
    runner = artifacts["runner"]["path"]
    if not isinstance(argv_value, list) or not all(isinstance(item, str) for item in argv_value):
        fail("Runnable command argv must be a string list")
    argv = [item for item in argv_value if isinstance(item, str)]
    if schema_version in {3, 5} and runner != "labs/g01_safe_c/run_harness.py":
        fail(f"schema {schema_version} runner artifact path is not the G1 module")
    if schema_version in {4, 6} and runner != "labs/g02_embedded_cpp/run_harness.py":
        fail(f"schema {schema_version} runner artifact path is not the G2 module")
    if schema_version == 2:
        expected = ["python3", runner]
    elif schema_version == 3:
        expected = [*PINNED_G1_ARGV_PREFIX, PINNED_G1_MODULE]
    elif schema_version == 4:
        expected = [*PINNED_G2_ARGV_PREFIX, PINNED_G2_MODULE]
    elif schema_version == 5:
        expected = [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G1_MODULE]
    else:
        expected = [*LOCKED_TOOLCHAIN_ARGV_PREFIX, PINNED_G2_MODULE]
    if argv != expected:
        fail(f"Runnable command does not match schema {schema_version}'s pinned runner command")
    environment_value = command.get("environment")
    if not isinstance(environment_value, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in environment_value.items()
    ):
        fail("command environment must be a string map")
    environment = {
        key: value
        for key, value in environment_value.items()
        if isinstance(key, str) and isinstance(value, str)
    }
    if command.get("expected_exit") != 0 or command.get("observed_exit") != 0:
        fail("Runnable command needs a recorded successful exit")
    return argv, environment


def verify_retest_command_shape(
    command: dict[str, Any],
    artifacts: dict[str, dict[str, str]],
    lab_id: str,
    schema_version: int = 4,
) -> tuple[list[str], dict[str, str]]:
    argv, environment = verify_command_shape(command, artifacts, schema_version)
    lab_variable = "G01_LAB_ID" if schema_version == 5 else "G02_LAB_ID"
    expected_environment = {
        lab_variable: f"{lab_id}.RETEST",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    if environment != expected_environment:
        fail(f"active retest command must select the B input for {lab_id}")
    return argv, environment


def repository_check_identity(manifest: dict[str, Any]) -> tuple[str, str, str]:
    check = manifest.get("repository_check")
    if not isinstance(check, dict):
        fail("active manifest needs repository_check evidence")
    starter = manifest.get("starter_commit")
    stdout_hash = check.get("stdout_sha256")
    stderr_hash = check.get("stderr_sha256")
    if not all(isinstance(value, str) for value in (starter, stdout_hash, stderr_hash)):
        fail("repository_check identity is incomplete")
    return str(starter), str(stdout_hash), str(stderr_hash)


def verify_manifest(
    path: Path,
    active: bool,
    indexed_lab_id: str | None = None,
    repository_checks: set[tuple[str, str, str]] | None = None,
) -> str:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    schema_version = manifest.get("schema_version")
    if schema_version not in {2, 3, 4, 5, 6} or manifest.get("status") != "Runnable":
        fail(f"invalid manifest header: {path.relative_to(REPO_ROOT)}")
    if active and str(manifest.get("lab_id", "")).startswith("G1.") and schema_version != 5:
        fail("active G1 evidence must use the hash-locked schema 5 toolchain contract")
    if active and str(manifest.get("lab_id", "")).startswith("G2.") and schema_version != 6:
        fail("active G2 evidence must use the hash-locked schema 6 toolchain contract")
    if active and manifest.get("lab_id") != indexed_lab_id:
        fail(f"active index lab ID {indexed_lab_id} does not match manifest lab ID {manifest.get('lab_id')}")
    starter = manifest.get("starter_commit")
    if not isinstance(starter, str) or not FULL_SHA.fullmatch(starter):
        fail("starter_commit must be a full lowercase SHA")
    if run_git(
        ["cat-file", "-e", f"{starter}^{{commit}}"],
        f"starter lookup for {starter}",
    ).returncode != 0:
        fail(f"starter commit is unavailable: {starter}")
    if run_git(
        ["merge-base", "--is-ancestor", starter, "HEAD"],
        f"starter ancestry check for {starter}",
    ).returncode != 0:
        fail(f"starter commit is not an ancestor of HEAD: {starter}")

    artifacts = verify_artifacts(manifest, starter, active)
    command = manifest.get("command")
    if not isinstance(command, dict):
        fail("command must be an object")
    argv, command_environment = verify_command_shape(command, artifacts, schema_version)
    command_stdout = recorded_command_stdout(command, "primary")
    retest: tuple[dict[str, Any], list[str], dict[str, str], bytes] | None = None
    if active and schema_version in {5, 6}:
        retest_value = manifest.get("retest_command")
        if not isinstance(retest_value, dict):
            fail("active G2 manifest needs recorded B input evidence")
        retest_argv, retest_environment = verify_retest_command_shape(
            retest_value, artifacts, str(manifest["lab_id"]), schema_version
        )
        retest = (
            retest_value,
            retest_argv,
            retest_environment,
            recorded_command_stdout(retest_value, "retest"),
        )
    if manifest.get("snapshot") != {
        "method": "git archive",
        "network_required": False,
        "working_tree_files_used": False,
    }:
        fail("snapshot contract must require a network-free git archive")

    with tempfile.TemporaryDirectory(prefix="runnable-") as temp_dir:
        snapshot = Path(temp_dir)
        archive_starter(starter, snapshot)
        verify_runtime(snapshot, manifest)
        env = replay_environment(manifest, os.environ.copy())
        env.update(command_environment)
        replay = run_binary_replay(
            translated_replay_argv(argv),
            cwd=snapshot,
            environment=env,
            label="primary replay",
        )
        verify_output(replay, command, command_stdout)
        if retest is not None:
            retest_command, retest_argv, retest_environment, retest_stdout = retest
            retest_env = replay_environment(manifest, os.environ.copy())
            retest_env.update(retest_environment)
            retest_replay = run_binary_replay(
                translated_replay_argv(retest_argv),
                cwd=snapshot,
                environment=retest_env,
                label="retest replay",
            )
            verify_output(retest_replay, retest_command, retest_stdout)
        if active:
            identity = repository_check_identity(manifest)
            if repository_checks is None or identity not in repository_checks:
                verify_repository_check(manifest, snapshot)
                if repository_checks is not None:
                    repository_checks.add(identity)

    timing = manifest.get("timing")
    if not isinstance(timing, dict) or not isinstance(timing.get("harness"), dict):
        fail("timing must contain harness measurements")
    if not all(
        isinstance(timing["harness"].get(field), (int, float)) and timing["harness"][field] > 0
        for field in ("active_seconds", "wall_seconds")
    ):
        fail("harness timing is incomplete")
    if active and schema_version in {5, 6}:
        retest_timing = timing.get("retest")
        if not isinstance(retest_timing, dict) or not all(
            isinstance(retest_timing.get(field), (int, float)) and retest_timing[field] > 0
            for field in ("active_seconds", "wall_seconds")
        ):
            fail("active G2 retest timing is incomplete")
    learner_timing = manifest.get("learner_time_calibration")
    if not isinstance(learner_timing, dict) or learner_timing.get("status") != "Not run":
        fail("machine replay and learner-time calibration must remain separate")
    if active:
        verify_sprint_lock(manifest, artifacts)
    return f"{manifest['lab_id']}@{starter[:12]}"
