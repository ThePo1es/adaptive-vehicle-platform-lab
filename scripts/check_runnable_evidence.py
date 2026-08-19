#!/usr/bin/env python3
"""Replay Runnable manifests from archived starter commits and verify active locks."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = REPO_ROOT / "evidence/runnable"
INDEX_PATH = EVIDENCE_ROOT / "index.json"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
LAB_ID = re.compile(r"^G\d+\.\d+$")
REQUIRED_ROLES = {"fixture", "validator", "runner", "starter"}
ACTIVE_REQUIRED_ROLES = REQUIRED_ROLES | {
    "evidence-checker",
    "review-fixture",
    "reviewer-registry",
    "source-lock",
    "unit-tests",
}


def fail(message: str) -> None:
    raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repository_path(value: Any) -> Path:
    if not isinstance(value, str) or not value:
        fail("path must be a non-empty string")
    path = (REPO_ROOT / value).resolve()
    if not path.is_relative_to(REPO_ROOT):
        fail(f"path escapes repository: {value}")
    return path


def git_bytes(commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        fail(f"starter object is unavailable: {commit}:{relative_path}")
    return result.stdout


def archive_starter(commit: str, target: Path) -> None:
    archived = subprocess.run(
        ["git", "archive", "--format=tar", commit],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    if archived.returncode != 0:
        fail(f"git archive failed for starter {commit}")
    with tarfile.open(fileobj=io.BytesIO(archived.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                fail(f"unsafe path in git archive: {member.name}")
        archive.extractall(target, filter="data")


def active_manifest_paths() -> dict[str, str]:
    if not INDEX_PATH.exists():
        return {}
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    if index.get("schema_version") != 1 or not isinstance(index.get("active"), dict):
        fail("evidence/runnable/index.json has an invalid schema")
    active: dict[str, str] = {}
    for lab_id, value in index["active"].items():
        if not isinstance(lab_id, str) or not LAB_ID.fullmatch(lab_id):
            fail(f"active index has an invalid lab ID: {lab_id}")
        path = repository_path(value)
        if not path.is_file():
            fail(f"active Runnable manifest is missing: {value}")
        relative = str(path.relative_to(REPO_ROOT))
        expected_parent = EVIDENCE_ROOT / lab_id.lower()
        if path.parent != expected_parent:
            fail(f"active manifest path does not match {lab_id}: {value}")
        if relative in active:
            fail(f"one manifest is assigned to multiple lab IDs: {value}")
        active[relative] = lab_id
    return active


def runnable_gate_lab_ids() -> set[str]:
    runnable: set[str] = set()
    for path in sorted((REPO_ROOT / "gates").glob("g*/sprint-*.md")):
        text = path.read_text(encoding="utf-8")
        if "준비 상태: `Runnable`" not in text:
            continue
        heading = re.search(r"^# Sprint (\d+\.\d+)\b", text, re.MULTILINE)
        if heading is None:
            fail(f"Runnable Sprint has no parseable ID: {path.relative_to(REPO_ROOT)}")
        runnable.add(f"G{heading.group(1)}")
    return runnable


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
    required_roles = ACTIVE_REQUIRED_ROLES if active else REQUIRED_ROLES
    missing = required_roles - set(by_role)
    if missing:
        fail(f"required artifact roles are missing: {', '.join(sorted(missing))}")
    return by_role


def verify_command_shape(
    command: dict[str, Any],
    artifacts: dict[str, dict[str, str]],
) -> tuple[list[str], dict[str, str]]:
    argv = command.get("argv")
    runner = artifacts["runner"]["path"]
    if argv != ["python3", runner]:
        fail("Runnable command must invoke the hashed runner artifact with python3")
    environment = command.get("environment")
    if not isinstance(environment, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in environment.items()
    ):
        fail("command environment must be a string map")
    if command.get("expected_exit") != 0 or command.get("observed_exit") != 0:
        fail("Runnable command needs a recorded successful exit")
    return argv, environment


def verify_runtime(snapshot: Path, manifest: dict[str, Any]) -> None:
    expected = manifest.get("environment", {}).get("python")
    if not isinstance(expected, str):
        fail("manifest environment needs an exact Python version")
    version = subprocess.run(
        ["python3", "--version"],
        cwd=snapshot,
        check=False,
        capture_output=True,
        text=True,
    )
    observed = version.stdout.strip().removeprefix("Python ")
    if version.returncode != 0 or observed != expected:
        fail(f"Python version mismatch: expected {expected}, got {observed}")


def verify_output(
    result: subprocess.CompletedProcess[bytes],
    command: dict[str, Any],
    recorded_stdout: bytes,
) -> None:
    expected_stdout_hash = command.get("stdout_sha256")
    expected_stderr_hash = command.get("stderr_sha256")
    if not isinstance(expected_stdout_hash, str) or not SHA256.fullmatch(expected_stdout_hash):
        fail("stdout_sha256 is invalid")
    if not isinstance(expected_stderr_hash, str) or not SHA256.fullmatch(expected_stderr_hash):
        fail("stderr_sha256 is invalid")
    if result.returncode != command["expected_exit"]:
        fail(f"replay exit mismatch: expected {command['expected_exit']}, got {result.returncode}")
    if result.stdout != recorded_stdout or digest(result.stdout) != expected_stdout_hash:
        fail("replay stdout does not match recorded evidence")
    if digest(result.stderr) != expected_stderr_hash:
        fail("replay stderr does not match manifest")


def verify_sprint_lock(
    manifest: dict[str, Any],
    artifacts: dict[str, dict[str, str]],
) -> None:
    lab_id = manifest["lab_id"]
    if lab_id != "G10.1":
        fail(f"no Sprint lock parser is configured for {lab_id}")
    sprint = (REPO_ROOT / "gates/g10/sprint-10.1.md").read_text(encoding="utf-8")
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
    environment = check.get("environment")
    if environment != {"SKIP_RUNNABLE_EVIDENCE": "1", "PYTHONDONTWRITEBYTECODE": "1"}:
        fail("repository_check environment must disable only recursive evidence replay and bytecode")
    stdout_path = repository_path(check.get("stdout_path"))
    stderr_path = repository_path(check.get("stderr_path"))
    expected_stdout = stdout_path.read_bytes()
    expected_stderr = stderr_path.read_bytes()
    env = os.environ.copy()
    env.update(environment)
    result = subprocess.run(
        check["argv"],
        cwd=snapshot,
        env=env,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0 or check.get("expected_exit") != 0 or check.get("observed_exit") != 0:
        fail("repository_check exit does not match a successful run")
    if result.stdout != expected_stdout or digest(result.stdout) != check.get("stdout_sha256"):
        fail("repository_check stdout does not match evidence")
    if result.stderr != expected_stderr or digest(result.stderr) != check.get("stderr_sha256"):
        fail("repository_check stderr does not match evidence")


def verify_manifest(path: Path, active: bool, indexed_lab_id: str | None = None) -> str:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 2 or manifest.get("status") != "Runnable":
        fail(f"invalid manifest header: {path.relative_to(REPO_ROOT)}")
    if active and manifest.get("lab_id") != indexed_lab_id:
        fail(
            f"active index lab ID {indexed_lab_id} does not match manifest lab ID {manifest.get('lab_id')}"
        )
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
    argv, command_environment = verify_command_shape(command, artifacts)
    stdout_path = repository_path(command.get("stdout_path"))
    recorded_stdout = stdout_path.read_bytes()
    if digest(recorded_stdout) != command.get("stdout_sha256"):
        fail("recorded stdout hash drifted")

    snapshot_config = manifest.get("snapshot")
    if snapshot_config != {
        "method": "git archive",
        "network_required": False,
        "working_tree_files_used": False,
    }:
        fail("snapshot contract must require a network-free git archive")

    with tempfile.TemporaryDirectory(prefix="g10-runnable-") as temp_dir:
        snapshot = Path(temp_dir)
        archive_starter(starter, snapshot)
        verify_runtime(snapshot, manifest)
        env = os.environ.copy()
        env.update(command_environment)
        replay = subprocess.run(
            argv,
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


def main() -> int:
    try:
        active = active_manifest_paths()
        gate_runnable = runnable_gate_lab_ids()
        indexed_runnable = set(active.values())
        if indexed_runnable != gate_runnable:
            fail(
                "active index and Runnable Sprint headers differ: "
                f"index={sorted(indexed_runnable)}, gates={sorted(gate_runnable)}"
            )
        manifests = sorted(EVIDENCE_ROOT.glob("*/run-manifest*.json"))
        if not manifests:
            fail("no Runnable manifests found")
        verified = []
        for path in manifests:
            relative = str(path.relative_to(REPO_ROOT))
            verified.append(verify_manifest(path, relative in active, active.get(relative)))
        missing_active = set(active) - {str(path.relative_to(REPO_ROOT)) for path in manifests}
        if missing_active:
            fail(f"active manifests were not discovered: {', '.join(sorted(missing_active))}")
    except (OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
        print(f"Runnable evidence: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"Runnable evidence: OK ({len(verified)} manifest, {len(active)} active: {', '.join(verified)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
