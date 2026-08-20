from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from scripts.runnable_evidence_support import (
    FULL_SHA,
    REPO_ROOT,
    SHA256,
    archive_starter,
    canonical_output,
    digest,
    fail,
    git_bytes,
    repository_path,
    required_roles,
    translated_replay_argv,
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


PINNED_G1_ARGV_PREFIX = [
    "uv",
    "run",
    "--offline",
    "--python",
    "3.12.13",
    "--with",
    "ziglang==0.15.2",
    "python",
    "-m",
]
PINNED_G1_MODULE = "labs.g01_safe_c.run_harness"


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
    if schema_version == 3 and runner != "labs/g01_safe_c/run_harness.py":
        fail("schema 3 runner artifact path is not the G1 module")
    expected = (
        ["python3", runner]
        if schema_version == 2
        else [*PINNED_G1_ARGV_PREFIX, PINNED_G1_MODULE]
    )
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


def verify_runtime(snapshot: Path, manifest: dict[str, Any]) -> None:
    expected = manifest.get("environment", {}).get("python")
    if not isinstance(expected, str):
        fail("manifest environment needs an exact Python version")
    schema_version = manifest["schema_version"]
    version_command = (
        [sys.executable, "--version"]
        if schema_version == 2
        else [*PINNED_G1_ARGV_PREFIX[:-1], "--version"]
    )
    version = subprocess.run(
        version_command,
        cwd=snapshot,
        check=False,
        capture_output=True,
        text=True,
    )
    observed = version.stdout.strip().removeprefix("Python ")
    if version.returncode != 0 or observed != expected:
        fail(f"Python version mismatch: expected {expected}, got {observed}")
    if schema_version == 3:
        environment = manifest.get("environment")
        required = {
            "uv": "0.12.3",
            "c_compiler": "zig",
            "c_compiler_version": "0.15.2",
            "c_runtime": "Zig 0.15.2 bundled libc",
            "target_contract": "native x86_64 hosted C17",
        }
        if not isinstance(environment, dict) or any(
            environment.get(key) != value for key, value in required.items()
        ):
            fail("schema 3 environment does not seal the G1 toolchain contract")
        uv_version = subprocess.run(
            ["uv", "--version"],
            cwd=snapshot,
            check=False,
            capture_output=True,
            text=True,
        )
        if uv_version.returncode != 0 or uv_version.stdout.strip() != "uv 0.12.3":
            fail(f"uv version mismatch: {uv_version.stdout.strip()}")


def verify_output(
    result: subprocess.CompletedProcess[bytes],
    command: dict[str, Any],
    recorded_stdout: bytes,
) -> None:
    stdout_hash = command.get("stdout_sha256")
    stderr_hash = command.get("stderr_sha256")
    if not isinstance(stdout_hash, str) or not SHA256.fullmatch(stdout_hash):
        fail("stdout_sha256 is invalid")
    if not isinstance(stderr_hash, str) or not SHA256.fullmatch(stderr_hash):
        fail("stderr_sha256 is invalid")
    if result.returncode != command["expected_exit"]:
        fail(f"replay exit mismatch: expected {command['expected_exit']}, got {result.returncode}")
    stdout = canonical_output(result.stdout)
    stderr = canonical_output(result.stderr)
    if stdout != recorded_stdout or digest(stdout) != stdout_hash:
        fail("replay stdout does not match recorded evidence")
    if digest(stderr) != stderr_hash:
        fail("replay stderr does not match manifest")


def verify_sprint_lock(
    manifest: dict[str, Any],
    artifacts: dict[str, dict[str, str]],
) -> None:
    lab_id = manifest["lab_id"]
    match = re.fullmatch(r"G(\d+)\.(\d+)", lab_id)
    if match is None:
        fail(f"no Sprint lock parser is configured for {lab_id}")
    major, minor = match.groups()
    sprint_path = REPO_ROOT / f"gates/g{int(major):02d}/sprint-{major}.{minor}.md"
    if not sprint_path.is_file():
        fail(f"Sprint lock file is missing for {lab_id}")
    sprint = sprint_path.read_text(encoding="utf-8")
    starter = manifest["starter_commit"]
    fixture_hash = artifacts["fixture"]["sha256"]
    if starter not in sprint or fixture_hash not in sprint:
        fail("Sprint header does not match active starter and fixture hash")


def verify_repository_check(manifest: dict[str, Any], snapshot: Path) -> None:
    check = manifest.get("repository_check")
    if not isinstance(check, dict):
        fail("active manifest needs repository_check evidence")
    if check.get("argv") != ["bash", "scripts/check_repo.sh"]:
        fail("repository_check must invoke scripts/check_repo.sh")
    required_environment = {"SKIP_RUNNABLE_EVIDENCE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    if check.get("environment") != required_environment:
        fail("repository_check environment must disable only recursive evidence replay and bytecode")
    stdout_path = repository_path(check.get("stdout_path"))
    stderr_path = repository_path(check.get("stderr_path"))
    expected_stdout = stdout_path.read_bytes()
    expected_stderr = stderr_path.read_bytes()
    env = os.environ.copy()
    env.update(required_environment)
    result = subprocess.run(
        ["bash", "scripts/check_repo.sh"],
        cwd=snapshot,
        env=env,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0 or check.get("expected_exit") != 0 or check.get("observed_exit") != 0:
        fail("repository_check exit does not match a successful run")
    stdout = canonical_output(result.stdout)
    stderr = canonical_output(result.stderr)
    if stdout != expected_stdout or digest(stdout) != check.get("stdout_sha256"):
        fail("repository_check stdout does not match evidence")
    if stderr != expected_stderr or digest(stderr) != check.get("stderr_sha256"):
        fail("repository_check stderr does not match evidence")


def verify_manifest(path: Path, active: bool, indexed_lab_id: str | None = None) -> str:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    schema_version = manifest.get("schema_version")
    if schema_version not in {2, 3} or manifest.get("status") != "Runnable":
        fail(f"invalid manifest header: {path.relative_to(REPO_ROOT)}")
    if active and str(manifest.get("lab_id", "")).startswith("G1.") and schema_version != 3:
        fail("active G1 evidence must use the hermetic schema 3 toolchain contract")
    if active and manifest.get("lab_id") != indexed_lab_id:
        fail(f"active index lab ID {indexed_lab_id} does not match manifest lab ID {manifest.get('lab_id')}")
    starter = manifest.get("starter_commit")
    if not isinstance(starter, str) or not FULL_SHA.fullmatch(starter):
        fail("starter_commit must be a full lowercase SHA")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{starter}^{{commit}}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    ).returncode != 0:
        fail(f"starter commit is unavailable: {starter}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", starter, "HEAD"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    ).returncode != 0:
        fail(f"starter commit is not an ancestor of HEAD: {starter}")

    artifacts = verify_artifacts(manifest, starter, active)
    command = manifest.get("command")
    if not isinstance(command, dict):
        fail("command must be an object")
    argv, command_environment = verify_command_shape(command, artifacts, schema_version)
    stdout_path = repository_path(command.get("stdout_path"))
    recorded_stdout = stdout_path.read_bytes()
    if digest(recorded_stdout) != command.get("stdout_sha256"):
        fail("recorded stdout hash drifted")
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
        env = os.environ.copy()
        env.update(command_environment)
        replay = subprocess.run(
            translated_replay_argv(argv),
            cwd=snapshot,
            env=env,
            check=False,
            capture_output=True,
        )
        verify_output(replay, command, recorded_stdout)
        if active:
            verify_repository_check(manifest, snapshot)

    timing = manifest.get("timing")
    if not isinstance(timing, dict) or not isinstance(timing.get("harness"), dict):
        fail("timing must contain harness measurements")
    if not all(
        isinstance(timing["harness"].get(field), (int, float)) and timing["harness"][field] > 0
        for field in ("active_seconds", "wall_seconds")
    ):
        fail("harness timing is incomplete")
    learner_timing = manifest.get("learner_time_calibration")
    if not isinstance(learner_timing, dict) or learner_timing.get("status") != "Not run":
        fail("machine replay and learner-time calibration must remain separate")
    if active:
        verify_sprint_lock(manifest, artifacts)
    return f"{manifest['lab_id']}@{starter[:12]}"
