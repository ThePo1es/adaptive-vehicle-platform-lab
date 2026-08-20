from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Any, NoReturn

REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = REPO_ROOT / "evidence/runnable"
INDEX_PATH = EVIDENCE_ROOT / "index.json"
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
LAB_ID = re.compile(r"^G\d+\.\d+$")
REQUIRED_ROLES = {"fixture", "validator", "runner", "starter"}
REPLAY_ROLES = {"evidence-checker", "evidence-support", "evidence-validator"}
G1_ACTIVE_REQUIRED_ROLES = REQUIRED_ROLES | REPLAY_ROLES | {
    "retest-fixture",
    "toolchain-resolver",
    "unit-tests",
}
G10_ACTIVE_REQUIRED_ROLES = REQUIRED_ROLES | REPLAY_ROLES | {
    "review-fixture",
    "review-policy",
    "review-policy-signature-a",
    "review-policy-signature-b",
    "reviewer-registry",
    "source-lock",
    "unit-tests",
}


def fail(message: str) -> NoReturn:
    raise ValueError(message)


def required_roles(lab_id: str, active: bool) -> set[str]:
    if not active:
        return REQUIRED_ROLES
    if lab_id.startswith("G1."):
        return G1_ACTIVE_REQUIRED_ROLES
    if lab_id == "G10.1":
        return G10_ACTIVE_REQUIRED_ROLES
    fail(f"no active artifact policy is configured for {lab_id}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_output(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


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
        if path.parent != EVIDENCE_ROOT / lab_id.lower():
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
            heading = re.search(r"관리 코드: G(\d+\.\d+)\b", text)
        if heading is None:
            fail(f"Runnable Sprint has no parseable ID: {path.relative_to(REPO_ROOT)}")
        runnable.add(f"G{heading.group(1)}")
    return runnable


def translated_replay_argv(argv: list[str]) -> list[str]:
    return [sys.executable, *argv[1:]] if argv[0] == "python3" else argv
