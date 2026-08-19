#!/usr/bin/env python3
"""Validate a G10.1 typed responsibility graph and its evidence links."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_LOCK_RELATIVE = "labs/g10_1_release_map/r25-11-document-lock.json"
TRUSTED_REVIEWERS_RELATIVE = "labs/g10_1_release_map/trusted-reviewers.json"
REVIEW_POLICY_RELATIVE = "labs/g10_1_release_map/review-policy.json"
REVIEW_POLICY_SIGNATURE_RELATIVES = (
    "labs/g10_1_release_map/review-policy.authority-a.sshsig",
    "labs/g10_1_release_map/review-policy.authority-b.sshsig",
)
SOURCE_LOCK = REPO_ROOT / SOURCE_LOCK_RELATIVE
TRUSTED_REVIEWERS = REPO_ROOT / TRUSTED_REVIEWERS_RELATIVE
REVIEW_POLICY = REPO_ROOT / REVIEW_POLICY_RELATIVE
MAPPING_STATUSES = ("Mapped", "Partial", "Missing", "Out of scope")
ROLE_MODEL = {
    "Service Interface": ("design-artifact", "design-time"),
    "Generated Proxy": ("generated-artifact", "generation-time"),
    "Generated Skeleton": ("generated-artifact", "generation-time"),
    "Service Instance Deployment": ("deployment-artifact", "deployment-time"),
    "Communication Binding": ("binding-artifact", "deployment-time"),
    "Runtime Proxy": ("runtime-role", "runtime"),
    "Runtime Skeleton": ("runtime-role", "runtime"),
    "Executable": ("deployment-artifact", "deployment-time"),
    "Process": ("runtime-role", "runtime"),
    "Function Group State": ("runtime-state", "runtime"),
    "Health Supervision": ("runtime-observation", "runtime"),
}
EDGE_RELATIONS = {
    "generates",
    "configures",
    "loads-as",
    "binds",
    "instantiates",
    "governs-lifecycle",
    "is-supervised-by",
    "communicates-with",
}
REQUIRED_ROLE_EDGES = {
    ("Service Interface", "generates", "Generated Proxy"),
    ("Service Interface", "generates", "Generated Skeleton"),
    ("Service Instance Deployment", "configures", "Communication Binding"),
    ("Generated Proxy", "loads-as", "Runtime Proxy"),
    ("Generated Skeleton", "loads-as", "Runtime Skeleton"),
    ("Communication Binding", "binds", "Runtime Proxy"),
    ("Communication Binding", "binds", "Runtime Skeleton"),
    ("Executable", "instantiates", "Process"),
    ("Function Group State", "governs-lifecycle", "Process"),
    ("Process", "is-supervised-by", "Health Supervision"),
    ("Runtime Proxy", "communicates-with", "Runtime Skeleton"),
}
LIFECYCLE_OWNERS = {
    "State Management",
    "Execution Management",
    "Platform Health Management",
    "Application",
    "Update and Configuration Management",
    "Local policy component",
}
FORBIDDEN_CLAIMS = (
    re.compile(r"\bAUTOSAR[- ]?(?:R25-11[- ]?)?(?:compliant|conformant)\b", re.IGNORECASE),
    re.compile(r"\bofficial AUTOSAR implementation\b", re.IGNORECASE),
    re.compile(r"\bara::com implementation\b", re.IGNORECASE),
    re.compile(r"\bproduction[- ]ready\b", re.IGNORECASE),
    re.compile(r"\b(?:complete|full|fully)[- ]+(?:AUTOSAR|implementation)\b", re.IGNORECASE),
    re.compile(r"\b(?:certified|certification[- ]ready)\b", re.IGNORECASE),
    re.compile(r"\b(?:compatible with|meets|implements)\s+(?:the\s+)?AUTOSAR\b", re.IGNORECASE),
    re.compile(r"\b(?:vehicle|road)[- ]ready\b", re.IGNORECASE),
    re.compile(r"\bproduction[- ]grade\b", re.IGNORECASE),
    re.compile(r"\b(?:series[- ](?:vehicle|production)|automotive[- ]grade)\b", re.IGNORECASE),
    re.compile(r"\bsuitable\s+for\s+(?:series|production|vehicle)[^.!?\n]*deployment\b", re.IGNORECASE),
    re.compile(r"\bdeployable\s+in\s+production\b", re.IGNORECASE),
    re.compile(r"\bready\s+for\s+series\s+production\b", re.IGNORECASE),
    re.compile(r"양산\s*(?:적용|배포|사용)?\s*(?:가능|준비|완료)?", re.IGNORECASE),
    re.compile(r"AUTOSAR\s*(?:적합|준수|호환)\s*(?:구현|제품)?", re.IGNORECASE),
    re.compile(r"차량\s*(?:적용|배포)\s*(?:가능|준비|완료)", re.IGNORECASE),
    re.compile(r"(?:제품급|상용\s*(?:배포|적용)\s*가능)", re.IGNORECASE),
    re.compile(r"\bfit\s+for\s+(?:deployment|use)\s+in\s+(?:customer\s+)?vehicles?\b", re.IGNORECASE),
    re.compile(r"\b(?:customer[- ]?vehicle|OEM|release[- ](?:ready|quality))\b", re.IGNORECASE),
    re.compile(r"\bvehicle\s+software\s+(?:level|quality)\b", re.IGNORECASE),
    re.compile(r"(?:OEM\s*)?고객(?:에게|사|용)?[^.!?\n]{0,24}(?:출시|납품|배포)\s*(?:가능|준비|완료)?", re.IGNORECASE),
    re.compile(r"차량\s*소프트웨어\s*수준", re.IGNORECASE),
    re.compile(r"(?:출시|납품|실차\s*적용|고객\s*배포)\s*(?:가능|준비|완료)", re.IGNORECASE),
)
PLACEHOLDER = re.compile(r"(?:\bTODO\b|\bTBD\b|<[^>]+>|확인 필요|미작성)", re.IGNORECASE)
NODE_ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
FULL_SHA256 = re.compile(r"^[0-9a-f]{64}$")
FULL_SHA512 = re.compile(r"^[0-9a-f]{128}$")
FULL_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
SSH_FINGERPRINT = re.compile(r"^SHA256:[A-Za-z0-9+/]{43}$")
REVIEWER_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._@-]{2,63}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_DIRECTORY = REPO_ROOT / "sources/autosar-r25-11"
REVIEW_DIRECTORY = REPO_ROOT / "evidence/reviews/g10.1"
REVIEW_SUBJECT_FIELDS = (
    "schema_version",
    "profile",
    "release",
    "claim_scope",
    "conformance_claim",
    "production_status",
    "submitter_id",
    "submitter_principal_id",
    "submitter_affiliation",
    "source_ledger",
    "nodes",
    "edges",
    "selected_binding",
    "lifecycle_scenarios",
    "summary",
)
CLAIM_TYPES = {"observed-local-behavior", "document-mapping", "known-gap"}
REVIEW_NAMESPACE = "adaptive-vehicle-platform-lab-g10.1"
RELEASE_POLICY_NAMESPACE = "adaptive-vehicle-platform-lab-g10.1-release-policy-v1"
RELEASE_AUTHORITIES = (
    (
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOM2fphXMi2WVt+OIPq5uOZ1ESIcb4Yfdy24w1lg/foo",
        "SHA256:jybHC9K5GuTflPOELZ+llMZ66hSThNySAHxOaEmghaU",
    ),
    (
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPLu4C4kubaeMJ8IZcVTDq013bzRI8Hi+N9GuE2RuZpk",
        "SHA256:M0pe4DkwbD2zwdlwIzZPcniSxQ1NoenTYcr7ibOi7vg",
    ),
)
NODE_FIELDS = {
    "id",
    "semantic_role",
    "node_type",
    "phase",
    "subject",
    "boundary",
    "configuration_source",
    "failure_observation",
    "mapping_status",
    "implementation_origin",
    "limitations",
    "citation_ids",
    "local_evidence",
    "claim_type",
    "observed_behavior",
    "excluded_conformance",
}
DOCUMENT_FIELDS = {
    "schema_version",
    "profile",
    "release",
    "claim_scope",
    "conformance_claim",
    "production_status",
    "submitter_id",
    "submitter_principal_id",
    "submitter_affiliation",
    "source_ledger",
    "nodes",
    "edges",
    "selected_binding",
    "lifecycle_scenarios",
    "summary",
    "review",
}


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    message: str


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def _meaningful(value: Any, minimum: int = 8) -> bool:
    if not isinstance(value, str) or not value.strip() or PLACEHOLDER.search(value):
        return False
    compact = re.sub(r"[^0-9A-Za-z가-힣]+", "", value)
    return len(compact) >= minimum and len(set(compact.lower())) >= 4


def _repo_path(value: str) -> Path | None:
    path = (REPO_ROOT / value).resolve()
    return path if path.is_relative_to(REPO_ROOT) else None


def _source_lock(payload: bytes) -> dict[str, dict[str, Any]]:
    lock = json.loads(payload)
    if lock.get("schema_version") != 2 or not isinstance(lock.get("documents"), list):
        raise ValueError("source lock has an invalid schema")
    return {entry["document_id"]: entry for entry in lock["documents"]}


def _trusted_reviewers(payload: bytes) -> dict[str, dict[str, Any]]:
    registry = json.loads(payload)
    if registry.get("schema_version") != 2 or registry.get("namespace") != REVIEW_NAMESPACE:
        raise ValueError("trusted reviewer registry has an invalid header")
    reviewers = registry.get("reviewers")
    if not isinstance(reviewers, list):
        raise ValueError("trusted reviewer registry needs a reviewers list")
    result: dict[str, dict[str, Any]] = {}
    for reviewer in reviewers:
        if not isinstance(reviewer, dict):
            raise ValueError("trusted reviewer entry must be an object")
        reviewer_id = reviewer.get("reviewer_id")
        if not isinstance(reviewer_id, str) or not REVIEWER_ID.fullmatch(reviewer_id):
            raise ValueError("trusted reviewer entry needs reviewer_id")
        if reviewer_id in result:
            raise ValueError("trusted reviewer IDs must be unique")
        required_text = ("principal_id", "affiliation", "public_key", "fingerprint", "identity_verified_on")
        if any(not isinstance(reviewer.get(field), str) or not reviewer[field] for field in required_text):
            raise ValueError("trusted reviewer identity metadata is incomplete")
        if not isinstance(reviewer.get("review_scopes"), list) or "G10.1" not in reviewer["review_scopes"]:
            raise ValueError("trusted reviewer has no G10.1 scope")
        if reviewer.get("status") != "Active":
            raise ValueError("trusted reviewer must be active")
        result[reviewer_id] = reviewer
    return result


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _review_subject_hash(document: dict[str, Any]) -> str:
    return _canonical_hash({field: document.get(field) for field in REVIEW_SUBJECT_FIELDS})


def _public_key_fingerprint(public_key: str) -> str | None:
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8") as key_file:
        key_file.write(public_key.rstrip() + "\n")
        key_file.flush()
        result = subprocess.run(
            ["ssh-keygen", "-lf", key_file.name, "-E", "sha256"],
            check=False,
            capture_output=True,
            text=True,
        )
    if result.returncode != 0:
        return None
    fields = result.stdout.split()
    return fields[1] if len(fields) >= 2 and SSH_FINGERPRINT.fullmatch(fields[1]) else None


def _verify_signature(
    payload: bytes,
    signature: bytes,
    identity: str,
    namespace: str,
    public_key: str,
) -> bool:
    with tempfile.TemporaryDirectory(prefix="g10-signature-") as temporary_directory:
        directory = Path(temporary_directory)
        allowed_signers = directory / "allowed_signers"
        signature_path = directory / "signature"
        allowed_signers.write_text(
            f'{identity} namespaces="{namespace}" {public_key.rstrip()}\n',
            encoding="utf-8",
        )
        signature_path.write_bytes(signature)
        result = subprocess.run(
            [
                "ssh-keygen",
                "-Y",
                "verify",
                "-f",
                str(allowed_signers),
                "-I",
                identity,
                "-n",
                namespace,
                "-s",
                str(signature_path),
            ],
            input=payload,
            check=False,
            capture_output=True,
        )
    return result.returncode == 0


def _git_blob(commit: str, relative_path: str) -> bytes | None:
    if not FULL_GIT_SHA.fullmatch(commit):
        return None
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else None


def _trust_bytes(commit: str | None, relative_path: str) -> bytes:
    if commit is None:
        return (REPO_ROOT / relative_path).read_bytes()
    payload = _git_blob(commit, relative_path)
    if payload is None:
        raise ValueError(f"trust file is absent from subject commit: {relative_path}")
    return payload


def _load_attested_trust(
    commit: str | None,
    findings: list[Finding],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, str]]:
    try:
        policy_payload = _trust_bytes(commit, REVIEW_POLICY_RELATIVE)
        signature_payloads = [
            _trust_bytes(commit, relative_path)
            for relative_path in REVIEW_POLICY_SIGNATURE_RELATIVES
        ]
        source_lock_payload = _trust_bytes(commit, SOURCE_LOCK_RELATIVE)
        reviewer_registry_payload = _trust_bytes(commit, TRUSTED_REVIEWERS_RELATIVE)
        policy = json.loads(policy_payload)
        anchor_fingerprints = [
            _public_key_fingerprint(public_key)
            for public_key, _ in RELEASE_AUTHORITIES
        ]
        expected_fingerprints = [fingerprint for _, fingerprint in RELEASE_AUTHORITIES]
        source_policy = policy.get("source_lock", {})
        reviewer_policy = policy.get("reviewer_registry", {})
        checks = (
            anchor_fingerprints == expected_fingerprints,
            policy.get("schema_version") == 1,
            policy.get("namespace") == RELEASE_POLICY_NAMESPACE,
            policy.get("authority_fingerprints") == expected_fingerprints,
            policy.get("signature_threshold") == len(RELEASE_AUTHORITIES) == 2,
            source_policy.get("path") == SOURCE_LOCK_RELATIVE,
            source_policy.get("sha256") == hashlib.sha256(source_lock_payload).hexdigest(),
            reviewer_policy.get("path") == TRUSTED_REVIEWERS_RELATIVE,
            reviewer_policy.get("sha256") == hashlib.sha256(reviewer_registry_payload).hexdigest(),
            all(
                _verify_signature(
                    policy_payload,
                    signature_payload,
                    "release-authority",
                    RELEASE_POLICY_NAMESPACE,
                    public_key,
                )
                for signature_payload, (public_key, _) in zip(signature_payloads, RELEASE_AUTHORITIES)
            ),
        )
        if not all(checks):
            raise ValueError("release policy signature or bound hashes do not match")
        source_lock = _source_lock(source_lock_payload)
        reviewers = _trusted_reviewers(reviewer_registry_payload)
    except (OSError, json.JSONDecodeError, ValueError):
        findings.append(Finding("E_TRUST_POLICY", "release authority policy is unavailable, unsigned, or inconsistent"))
        return {}, {}, {}
    return source_lock, reviewers, {
        "source_lock_sha256": hashlib.sha256(source_lock_payload).hexdigest(),
        "reviewer_registry_sha256": hashlib.sha256(reviewer_registry_payload).hexdigest(),
        "review_policy_sha256": hashlib.sha256(policy_payload).hexdigest(),
    }


def _validate_source_file(
    source: dict[str, Any],
    locked: dict[str, Any],
    index: int,
    findings: list[Finding],
) -> None:
    relative_path = source.get("source_file_path")
    if not isinstance(relative_path, str) or not relative_path:
        findings.append(Finding("E_SOURCE_PATH", f"source {index} needs source_file_path"))
        return
    path = _repo_path(relative_path)
    if (
        path is None
        or not path.is_relative_to(SOURCE_DIRECTORY)
        or path.name != locked.get("filename")
    ):
        findings.append(Finding("E_SOURCE_PATH", f"source {index} path does not match the document lock"))
        return
    if not path.is_file():
        findings.append(Finding("E_SOURCE_PATH", f"source {index} PDF is unavailable: {relative_path}"))
        return
    payload = path.read_bytes()
    if not payload.startswith(b"%PDF-"):
        findings.append(Finding("E_SOURCE_PATH", f"source {index} file has no PDF header"))
    expected_hash = source.get("source_file_sha256")
    if not isinstance(expected_hash, str) or not FULL_SHA256.fullmatch(expected_hash):
        findings.append(Finding("E_SOURCE_HASH", f"source {index} needs the downloaded PDF SHA-256"))
    elif hashlib.sha256(payload).hexdigest() != expected_hash:
        findings.append(Finding("E_SOURCE_HASH", f"source {index} PDF hash drifted"))
    official_sha512 = locked.get("official_sha512")
    if not isinstance(official_sha512, str) or not FULL_SHA512.fullmatch(official_sha512):
        findings.append(
            Finding(
                "E_SOURCE_TRUST",
                f"source {index} has no independently pinned AUTOSAR SHA-512 digest",
            )
        )
    elif hashlib.sha512(payload).hexdigest() != official_sha512:
        findings.append(Finding("E_SOURCE_TRUST", f"source {index} differs from the pinned AUTOSAR digest"))


def _validate_review_manifest(
    review: dict[str, Any],
    document: dict[str, Any],
    citation_ids: set[str],
    node_ids: set[str],
    profile: str,
    trusted_reviewers: dict[str, dict[str, Any]],
    trust_hashes: dict[str, str],
    input_path: Path | None,
    findings: list[Finding],
) -> None:
    reviewer_id = review.get("reviewer_id")
    submitter_id = document.get("submitter_id")
    if not isinstance(reviewer_id, str) or not REVIEWER_ID.fullmatch(reviewer_id):
        findings.append(Finding("E_REVIEW", "Reviewed status needs reviewer_id"))
    if not _meaningful(submitter_id, 4) or reviewer_id == submitter_id:
        findings.append(Finding("E_REVIEW_TRUST", "reviewer and submitter must be distinct identities"))
    subject_commit = review.get("subject_commit")
    reviewer_fingerprint = review.get("reviewer_key_fingerprint")
    subject_path = review.get("subject_path")
    if not isinstance(subject_commit, str) or not FULL_GIT_SHA.fullmatch(subject_commit):
        findings.append(Finding("E_REVIEW_TRUST", "Reviewed status needs a full subject commit SHA"))
    elif profile == "submission" and subprocess.run(
        ["git", "cat-file", "-e", f"{subject_commit}^{{commit}}"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    ).returncode != 0:
        findings.append(Finding("E_REVIEW_TRUST", "review subject commit is unavailable in this repository"))
    if not isinstance(reviewer_fingerprint, str) or not SSH_FINGERPRINT.fullmatch(reviewer_fingerprint):
        findings.append(Finding("E_REVIEW_TRUST", "Reviewed status needs a SHA-256 reviewer key fingerprint"))
    if not isinstance(subject_path, str) or not subject_path or _repo_path(subject_path) is None:
        findings.append(Finding("E_REVIEW_TRUST", "Reviewed status needs a repository-relative subject_path"))
    relative_path = review.get("review_manifest_path")
    expected_hash = review.get("review_manifest_sha256")
    if not isinstance(relative_path, str) or not relative_path:
        findings.append(Finding("E_REVIEW", "Reviewed status needs review_manifest_path"))
        return
    path = _repo_path(relative_path)
    if path is None or not path.is_file():
        findings.append(Finding("E_REVIEW", "review manifest file is unavailable"))
        return
    if profile == "submission" and not path.is_relative_to(REVIEW_DIRECTORY):
        findings.append(Finding("E_REVIEW", "submission review manifest must be stored under evidence/reviews/g10.1"))
    payload = path.read_bytes()
    if not isinstance(expected_hash, str) or not FULL_SHA256.fullmatch(expected_hash):
        findings.append(Finding("E_REVIEW", "Reviewed status needs review manifest SHA-256"))
    elif hashlib.sha256(payload).hexdigest() != expected_hash:
        findings.append(Finding("E_REVIEW", "review manifest hash drifted"))
    try:
        manifest = json.loads(payload)
    except json.JSONDecodeError:
        findings.append(Finding("E_REVIEW", "review manifest is not valid JSON"))
        return
    if not isinstance(manifest, dict):
        findings.append(Finding("E_REVIEW", "review manifest must be an object"))
        return
    expected_evidence_hashes = sorted(
        {
            item.get("sha256")
            for node in document.get("nodes", [])
            if isinstance(node, dict)
            for item in node.get("local_evidence", [])
            if isinstance(item, dict) and isinstance(item.get("sha256"), str)
        }
    )
    manifest_date = manifest.get("reviewed_on")
    checks = [
        manifest.get("schema_version") == 1,
        manifest.get("lab_id") == "G10.1",
        manifest.get("decision") == "Approved",
        manifest.get("reviewer_id") == reviewer_id,
        manifest.get("submitter_id") == submitter_id,
        manifest.get("subject_commit") == subject_commit,
        manifest.get("subject_path") == subject_path,
        manifest.get("reviewer_key_fingerprint") == reviewer_fingerprint,
        isinstance(manifest_date, str) and bool(ISO_DATE.fullmatch(manifest_date)),
        manifest.get("claim_scope") == "concept-aligned local prototype",
        set(manifest.get("reviewed_citation_ids", [])) == citation_ids,
        set(manifest.get("reviewed_node_ids", [])) == node_ids,
        manifest.get("source_ledger_sha256") == _canonical_hash(document.get("source_ledger")),
        manifest.get("review_subject_sha256") == _review_subject_hash(document),
        manifest.get("local_evidence_sha256s") == expected_evidence_hashes,
        manifest.get("limitations_acknowledged") is True,
        _meaningful(manifest.get("review_notes"), 12),
    ]
    if profile == "submission":
        checks.extend(
            (
                manifest.get("source_lock_sha256") == trust_hashes.get("source_lock_sha256"),
                manifest.get("reviewer_registry_sha256") == trust_hashes.get("reviewer_registry_sha256"),
                manifest.get("review_policy_sha256") == trust_hashes.get("review_policy_sha256"),
            )
        )
    else:
        checks.append(manifest.get("source_lock_sha256") == hashlib.sha256(SOURCE_LOCK.read_bytes()).hexdigest())
    if not all(checks):
        findings.append(Finding("E_REVIEW", "review manifest does not bind every claim, citation, limitation, and evidence hash"))
    if set(review.get("reviewed_citation_ids", [])) != citation_ids:
        findings.append(Finding("E_REVIEW", "reviewed citation set must cover the source ledger"))

    if profile != "submission":
        return

    if isinstance(subject_commit, str) and FULL_GIT_SHA.fullmatch(subject_commit) and isinstance(subject_path, str):
        committed_payload = _git_blob(subject_commit, subject_path)
        try:
            committed_document = json.loads(committed_payload) if committed_payload is not None else None
        except json.JSONDecodeError:
            committed_document = None
        if not isinstance(committed_document, dict) or _review_subject_hash(committed_document) != _review_subject_hash(document):
            findings.append(Finding("E_REVIEW_TRUST", "subject commit does not contain the reviewed submission at subject_path"))
        if input_path is None:
            findings.append(Finding("E_REVIEW_TRUST", "Reviewed submission validation needs the input file path"))
        else:
            resolved_input = input_path.resolve()
            expected_input = _repo_path(subject_path)
            if expected_input is None or resolved_input != expected_input:
                findings.append(Finding("E_REVIEW_TRUST", "validated input path differs from the signed subject_path"))

    signature_relative = review.get("review_signature_path")
    signature_path = _repo_path(signature_relative) if isinstance(signature_relative, str) else None
    if (
        signature_path is None
        or not signature_path.is_file()
        or not signature_path.is_relative_to(REVIEW_DIRECTORY)
    ):
        findings.append(Finding("E_REVIEW_TRUST", "submission review needs a detached signature under evidence/reviews/g10.1"))
        return
    trusted = trusted_reviewers.get(str(reviewer_id))
    if not isinstance(trusted, dict):
        findings.append(Finding("E_REVIEW_TRUST", "reviewer is absent from the trusted reviewer registry"))
        return
    public_key = trusted.get("public_key")
    trusted_fingerprint = trusted.get("fingerprint")
    if (
        not isinstance(public_key, str)
        or not isinstance(trusted_fingerprint, str)
        or trusted_fingerprint != reviewer_fingerprint
        or _public_key_fingerprint(public_key) != trusted_fingerprint
    ):
        findings.append(Finding("E_REVIEW_TRUST", "reviewer key does not match the trusted registry"))
        return
    submitter_principal_id = document.get("submitter_principal_id")
    submitter_affiliation = document.get("submitter_affiliation")
    reviewer_principal_id = trusted.get("principal_id")
    reviewer_affiliation = trusted.get("affiliation")
    independence_checks = (
        _meaningful(submitter_principal_id, 4),
        _meaningful(submitter_affiliation, 3),
        reviewer_principal_id != submitter_principal_id,
        reviewer_affiliation != submitter_affiliation,
        manifest.get("submitter_principal_id") == submitter_principal_id,
        manifest.get("submitter_affiliation") == submitter_affiliation,
        manifest.get("reviewer_principal_id") == reviewer_principal_id,
        manifest.get("reviewer_affiliation") == reviewer_affiliation,
        manifest.get("independence_confirmed") is True,
        manifest.get("conflict_of_interest") == "None declared",
    )
    if not all(independence_checks):
        findings.append(Finding("E_REVIEW_TRUST", "authority-attested reviewer identity or independence metadata does not match"))
    if not _verify_signature(
        payload,
        signature_path.read_bytes(),
        str(reviewer_id),
        REVIEW_NAMESPACE,
        public_key,
    ):
        findings.append(Finding("E_REVIEW_TRUST", "detached review signature verification failed"))


def _validate_evidence(
    node: dict[str, Any],
    index: int,
    profile: str,
    subject_commit: str | None,
    findings: list[Finding],
) -> None:
    evidence = node.get("local_evidence")
    status = node.get("mapping_status")
    if status in {"Mapped", "Partial"} and (not isinstance(evidence, list) or not evidence):
        findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} needs local evidence for {status}"))
        return
    if not isinstance(evidence, list):
        return

    for item_index, item in enumerate(evidence, start=1):
        if not isinstance(item, dict):
            findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence {item_index} must be an object"))
            continue
        relative_path = item.get("path")
        expected_hash = item.get("sha256")
        if not isinstance(relative_path, str) or not relative_path or not isinstance(expected_hash, str) or not FULL_SHA256.fullmatch(expected_hash):
            findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence {item_index} needs path and SHA-256"))
            continue
        if profile == "submission":
            path = _repo_path(relative_path)
            if subject_commit is not None:
                payload = _git_blob(subject_commit, relative_path)
                if payload is None:
                    findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence is absent from the subject commit: {relative_path}"))
                    continue
            elif path is None or not path.is_file():
                findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence path is unavailable: {relative_path}"))
                continue
            else:
                payload = path.read_bytes()
            if hashlib.sha256(payload).hexdigest() != expected_hash:
                findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence hash drifted: {relative_path}"))


def _validate(document: dict[str, Any], profile: str, input_path: Path | None = None) -> list[Finding]:
    findings: list[Finding] = []

    unknown_document_fields = sorted(set(document) - DOCUMENT_FIELDS)
    if unknown_document_fields:
        findings.append(Finding("E_SCHEMA", f"document has unstructured fields: {', '.join(unknown_document_fields)}"))
    if document.get("schema_version") != 3:
        findings.append(Finding("E_SCHEMA", "schema_version must be 3"))
    if document.get("profile") != profile:
        findings.append(Finding("E_PROFILE_DOWNGRADE", f"document profile must remain {profile}"))
    if document.get("release") != "R25-11":
        findings.append(Finding("E_RELEASE", "release must be R25-11"))
    if document.get("claim_scope") != "concept-aligned local prototype":
        findings.append(Finding("E_SCOPE_CLAIM", "claim_scope must remain 'concept-aligned local prototype'"))
    if document.get("conformance_claim") is not False:
        findings.append(Finding("E_SCOPE_CLAIM", "conformance_claim must remain false"))
    if document.get("production_status") != "educational-prototype":
        findings.append(Finding("E_SCOPE_CLAIM", "production_status must remain educational-prototype"))
    if profile == "submission" and any(
        not _meaningful(document.get(field), minimum)
        for field, minimum in (
            ("submitter_id", 4),
            ("submitter_principal_id", 4),
            ("submitter_affiliation", 3),
        )
    ):
        findings.append(Finding("E_SUBMITTER", "submission needs stable submitter identity and affiliation fields"))

    for text in _strings(document):
        if any(pattern.search(text) for pattern in FORBIDDEN_CLAIMS):
            findings.append(Finding("E_SCOPE_CLAIM", f"unsupported conformance claim: {text!r}"))
            break

    ledger = document.get("source_ledger")
    if not isinstance(ledger, list) or not ledger:
        findings.append(Finding("E_SOURCE_LEDGER", "source_ledger must contain at least one citation"))
        ledger = []
    review = document.get("review")
    subject_commit: str | None = None
    if (
        profile == "submission"
        and isinstance(review, dict)
        and review.get("status") == "Reviewed"
        and isinstance(review.get("subject_commit"), str)
        and FULL_GIT_SHA.fullmatch(review["subject_commit"])
    ):
        subject_commit = review["subject_commit"]
    source_lock: dict[str, dict[str, Any]] = {}
    trusted_reviewers: dict[str, dict[str, Any]] = {}
    trust_hashes: dict[str, str] = {}
    if profile == "submission":
        source_lock, trusted_reviewers, trust_hashes = _load_attested_trust(subject_commit, findings)
    required_documents_by_role: dict[str, set[str]] = {role: set() for role in ROLE_MODEL}
    for document_id, entry in source_lock.items():
        for role in entry.get("required_semantic_roles", []):
            if role in required_documents_by_role:
                required_documents_by_role[role].add(document_id)
    citation_ids: set[str] = set()
    citation_documents: dict[str, str] = {}
    for index, source in enumerate(ledger, start=1):
        if not isinstance(source, dict):
            findings.append(Finding("E_SOURCE_LEDGER", f"source {index} must be an object"))
            continue
        citation_id = source.get("citation_id")
        if not _meaningful(citation_id, 4) or citation_id in citation_ids:
            findings.append(Finding("E_SOURCE_LEDGER", f"source {index} needs a unique citation_id"))
        else:
            citation_ids.add(citation_id)
            if isinstance(source.get("document_id"), str):
                citation_documents[citation_id] = source["document_id"]

        if profile == "submission":
            document_id = source.get("document_id")
            locked = source_lock.get(document_id)
            if source.get("source_kind") != "official":
                findings.append(Finding("E_SOURCE_KIND", f"source {index} must be official"))
            if source.get("release") != "R25-11":
                findings.append(Finding("E_RELEASE", f"source {index} must be pinned to R25-11"))
            if source.get("access_status") != "Direct":
                findings.append(Finding("E_SOURCE_ACCESS", f"source {index} has no direct-reading record"))
            if locked is None:
                findings.append(Finding("E_CITATION_ID", f"source {index} document ID is outside the R25-11 lock"))
            else:
                if source.get("source_url") != locked.get("source_url"):
                    findings.append(Finding("E_SOURCE_URL", f"source {index} URL differs from the R25-11 lock"))
                if source.get("document_revision") != locked.get("document_revision"):
                    findings.append(Finding("E_SOURCE_REVISION", f"source {index} revision differs from the R25-11 lock"))
                _validate_source_file(source, locked, index, findings)
            if not _meaningful(source.get("section_title"), 8):
                findings.append(Finding("E_CITATION_LOCATOR", f"source {index} needs the exact section title"))
            locator = source.get("section_locator")
            if not _meaningful(locator, 3) or not re.search(r"(?:\d|SWS_|RS_)", str(locator)):
                findings.append(Finding("E_CITATION_LOCATOR", f"source {index} needs a section number or requirement ID"))
            accessed_on = source.get("accessed_on")
            if not isinstance(accessed_on, str) or not ISO_DATE.fullmatch(accessed_on):
                findings.append(Finding("E_CITATION_DATE", f"source {index} accessed_on must use YYYY-MM-DD"))

    nodes = document.get("nodes")
    if not isinstance(nodes, list) or len(nodes) < len(ROLE_MODEL):
        findings.append(Finding("E_GRAPH_COVERAGE", f"graph needs at least {len(ROLE_MODEL)} typed nodes"))
        nodes = []

    node_ids: set[str] = set()
    observed_roles: Counter[str] = Counter()
    observed_behaviors: list[str] = []
    evidence_path_roles: dict[str, set[str]] = {}
    if nodes:
        for index, node in enumerate(nodes, start=1):
            if not isinstance(node, dict):
                findings.append(Finding("E_NODE_FIELD", f"node {index} must be an object"))
                continue
            unknown_fields = sorted(set(node) - NODE_FIELDS)
            if unknown_fields:
                findings.append(Finding("E_NODE_FIELD", f"node {index} has unstructured fields: {', '.join(unknown_fields)}"))
            node_id = node.get("id")
            if not isinstance(node_id, str) or not NODE_ID.fullmatch(node_id) or node_id in node_ids:
                findings.append(Finding("E_NODE_ID", f"node {index} needs a unique lower-kebab-case id"))
            else:
                node_ids.add(node_id)

            role = node.get("semantic_role")
            if role not in ROLE_MODEL:
                findings.append(Finding("E_GRAPH_COVERAGE", f"node {index} has an unknown semantic role"))
            else:
                observed_roles[role] += 1
                expected_type, expected_phase = ROLE_MODEL[role]
                if node.get("node_type") != expected_type or node.get("phase") != expected_phase:
                    findings.append(Finding("E_PHASE", f"node {index} type/phase does not match {role}"))

            for field in (
                "subject",
                "boundary",
                "observed_behavior",
                "excluded_conformance",
                "configuration_source",
                "failure_observation",
            ):
                if not _meaningful(node.get(field), 8):
                    findings.append(Finding("E_NODE_FIELD", f"node {index} needs a concrete {field}"))
            if isinstance(node.get("observed_behavior"), str):
                observed_behaviors.append(node["observed_behavior"])

            status = node.get("mapping_status")
            if status not in MAPPING_STATUSES:
                findings.append(Finding("E_MAPPING_STATUS", f"node {index} has an unknown mapping status"))
            claim_type = node.get("claim_type")
            if claim_type not in CLAIM_TYPES:
                findings.append(Finding("E_SCOPE_CLAIM", f"node {index} has an unknown claim_type"))
            elif status in {"Mapped", "Partial"} and claim_type == "known-gap":
                findings.append(Finding("E_SCOPE_CLAIM", f"node {index} maps evidence while declaring only a known gap"))
            elif status in {"Missing", "Out of scope"} and claim_type == "observed-local-behavior":
                findings.append(Finding("E_SCOPE_CLAIM", f"node {index} claims observed behavior without mapped evidence"))
            if node.get("implementation_origin") != "local-prototype":
                findings.append(Finding("E_IMPLEMENTATION_ORIGIN", f"node {index} must identify local-prototype origin"))
            limitations = node.get("limitations")
            if not isinstance(limitations, list) or not limitations or not all(_meaningful(item, 10) for item in limitations):
                findings.append(Finding("E_NODE_FIELD", f"node {index} needs concrete limitations"))
            node_citations = node.get("citation_ids")
            if not isinstance(node_citations, list) or not node_citations:
                findings.append(Finding("E_CITATION_REF", f"node {index} needs at least one citation"))
            elif citation_ids:
                unknown = sorted(set(node_citations) - citation_ids)
                if unknown:
                    findings.append(Finding("E_CITATION_REF", f"node {index} cites unknown IDs: {', '.join(unknown)}"))
                if profile == "submission" and role in ROLE_MODEL:
                    cited_documents = {
                        citation_documents[citation]
                        for citation in node_citations
                        if citation in citation_documents
                    }
                    required_documents = required_documents_by_role[role]
                    if not required_documents.issubset(cited_documents):
                        missing_documents = ", ".join(sorted(required_documents - cited_documents))
                        findings.append(
                            Finding(
                                "E_CITATION_ROLE",
                                f"node {index} is missing role-specific documents: {missing_documents}",
                            )
                        )
            _validate_evidence(node, index, profile, subject_commit, findings)
            if status in {"Mapped", "Partial"} and isinstance(node.get("local_evidence"), list):
                for item in node["local_evidence"]:
                    if isinstance(item, dict) and isinstance(item.get("path"), str):
                        evidence_path_roles.setdefault(item["path"], set()).add(str(role))

        missing_or_duplicate = sorted(role for role in ROLE_MODEL if observed_roles[role] != 1)
        if missing_or_duplicate:
            findings.append(Finding("E_GRAPH_COVERAGE", f"required semantic roles must occur once: {', '.join(missing_or_duplicate)}"))
        if len(set(observed_behaviors)) != len(observed_behaviors):
            findings.append(Finding("E_NODE_FIELD", "node observed_behavior values must be distinct"))
        mapped_count = sum(
            1
            for node in nodes
            if isinstance(node, dict) and node.get("mapping_status") in {"Mapped", "Partial"}
        )
        if mapped_count and len(evidence_path_roles) < min(4, mapped_count):
            findings.append(
                Finding("E_LOCAL_EVIDENCE_DIVERSITY", "mapped roles need at least four distinct local evidence paths")
            )
        if any(len(roles) > 3 for roles in evidence_path_roles.values()):
            findings.append(
                Finding("E_LOCAL_EVIDENCE_DIVERSITY", "one local evidence path is reused across too many semantic roles")
            )

    edges = document.get("edges")
    if not isinstance(edges, list) or not edges:
        findings.append(Finding("E_EDGE_REF", "graph needs typed edges"))
        edges = []
    node_roles = {
        node.get("id"): node.get("semantic_role")
        for node in nodes
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    seen_edges: set[tuple[str, str, str]] = set()
    observed_role_edges: set[tuple[str, str, str]] = set()
    edge_references_valid = bool(edges)
    role_model_valid = all(observed_roles[role] == 1 for role in ROLE_MODEL)
    for index, edge in enumerate(edges, start=1):
        if not isinstance(edge, dict):
            findings.append(Finding("E_EDGE_REF", f"edge {index} must be an object"))
            edge_references_valid = False
            continue
        edge_key = (str(edge.get("from")), str(edge.get("relation")), str(edge.get("to")))
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids or edge.get("relation") not in EDGE_RELATIONS:
            findings.append(Finding("E_EDGE_REF", f"edge {index} has an unknown node or relation"))
            edge_references_valid = False
        elif edge_key in seen_edges:
            findings.append(Finding("E_EDGE_REF", f"edge {index} duplicates an earlier edge"))
            edge_references_valid = False
        elif role_model_valid:
            role_edge = (
                str(node_roles.get(edge["from"])),
                str(edge["relation"]),
                str(node_roles.get(edge["to"])),
            )
            if edge["from"] == edge["to"] or role_edge not in REQUIRED_ROLE_EDGES:
                findings.append(Finding("E_EDGE_SEMANTICS", f"edge {index} violates the role/relation contract"))
            else:
                observed_role_edges.add(role_edge)
        seen_edges.add(edge_key)
    if edge_references_valid and role_model_valid:
        missing_role_edges = REQUIRED_ROLE_EDGES - observed_role_edges
        if missing_role_edges:
            findings.append(
                Finding(
                    "E_GRAPH_CONNECTIVITY",
                    f"graph is missing {len(missing_role_edges)} required role edge(s)",
                )
            )

    binding = document.get("selected_binding")
    if not isinstance(binding, dict):
        findings.append(Finding("E_BINDING", "selected_binding must be an object"))
    else:
        binding_node = binding.get("node_id")
        binding_kind = binding.get("kind")
        binding_roles = {
            node.get("id"): node.get("semantic_role")
            for node in nodes
            if isinstance(node, dict)
        }
        if binding_kind not in {"SOME/IP", "DDS", "local-loopback"} or binding_roles.get(binding_node) != "Communication Binding":
            findings.append(Finding("E_BINDING", "selected binding must reference the Communication Binding node"))

    scenarios = document.get("lifecycle_scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        findings.append(Finding("E_OWNER_BOUNDARY", "at least one lifecycle scenario is required"))
        scenarios = []
    for index, scenario in enumerate(scenarios, start=1):
        if not isinstance(scenario, dict):
            findings.append(Finding("E_OWNER_BOUNDARY", f"scenario {index} must be an object"))
            continue
        for field in ("scenario", "scope", "requested_target", "recovery_report"):
            if not _meaningful(scenario.get(field), 8):
                findings.append(Finding("E_OWNER_BOUNDARY", f"scenario {index} needs a concrete {field}"))
        owner_fields = ("trigger_reporter", "policy_decision_owner", "transition_executor", "recovery_reporter")
        if any(scenario.get(field) not in LIFECYCLE_OWNERS for field in owner_fields):
            findings.append(Finding("E_OWNER_BOUNDARY", f"scenario {index} has an unknown responsibility owner"))
        if scenario.get("policy_decision_owner") == scenario.get("transition_executor"):
            findings.append(Finding("E_OWNER_BOUNDARY", f"scenario {index} merges policy decision and transition execution"))
        scenario_citations = scenario.get("citation_ids")
        if not isinstance(scenario_citations, list) or not scenario_citations or set(scenario_citations) - citation_ids:
            findings.append(Finding("E_CITATION_REF", f"scenario {index} has an invalid citation set"))

    if nodes:
        counts = Counter(node.get("mapping_status") for node in nodes if isinstance(node, dict))
        expected_summary = {status: counts.get(status, 0) for status in MAPPING_STATUSES}
        if document.get("summary") != expected_summary:
            findings.append(Finding("E_SUMMARY", "summary does not match node mapping statuses"))
        if counts.get("Mapped", 0) + counts.get("Partial", 0) == 0:
            findings.append(Finding("E_MAPPING_INCOMPLETE", "at least one node must be mapped to local evidence"))

    review = document.get("review")
    if not isinstance(review, dict) or review.get("status") not in {"Pending", "Reviewed"}:
        findings.append(Finding("E_REVIEW", "review status must be Pending or Reviewed"))
    elif review.get("status") == "Reviewed":
        _validate_review_manifest(
            review,
            document,
            citation_ids,
            node_ids,
            profile,
            trusted_reviewers,
            trust_hashes,
            input_path,
            findings,
        )
    elif any(
        review.get(field) not in (None, "", [])
        for field in (
            "reviewer_id",
            "reviewer_key_fingerprint",
            "subject_commit",
            "subject_path",
            "review_manifest_path",
            "review_manifest_sha256",
            "review_signature_path",
            "reviewed_citation_ids",
        )
    ):
        findings.append(Finding("E_REVIEW", "Pending review fields must remain empty"))

    return sorted(set(findings))


def validate_harness(document: dict[str, Any]) -> list[Finding]:
    """Validate the repository-owned synthetic fixture."""
    return _validate(document, "harness")


def validate_submission(document: dict[str, Any], input_path: Path | None = None) -> list[Finding]:
    """Validate a learner submission with direct sources and local file hashes."""
    return _validate(document, "submission", input_path)


def pass_line(document: dict[str, Any], input_path: Path | None = None) -> str:
    profile = document.get("profile")
    if profile == "harness":
        findings = validate_harness(document)
    elif profile == "submission":
        findings = validate_submission(document, input_path)
    else:
        findings = [Finding("E_PROFILE_DOWNGRADE", "document profile is unknown")]
    if findings:
        codes = ",".join(sorted({finding.code for finding in findings}))
        raise ValueError(f"cannot emit a pass line for invalid evidence: {codes}")
    summary = document["summary"]
    counts = ",".join(f"{status}:{summary[status]}" for status in MAPPING_STATUSES)
    review = document.get("review", {})
    reviewed = review.get("status") == "Reviewed"
    if reviewed and profile == "submission":
        prefix = "REVIEWED_PASS"
    elif reviewed:
        prefix = "HARNESS_REVIEW_BINDING_PASS"
    else:
        prefix = "STRUCTURE_PASS"
    trust_detail = ""
    if reviewed:
        trust_detail = (
            f" reviewer_key={review.get('reviewer_key_fingerprint')}"
            f" subject_commit={review.get('subject_commit')}"
        )
    return (
        f"{prefix} G10.1-MAP profile={profile} nodes={len(document['nodes'])} "
        f"edges={len(document['edges'])} citations={len(document['source_ledger'])} "
        f"statuses={counts} review={review['status']}{trust_detail}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()

    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL G10.1-MAP\nE_INPUT: {exc}")
        return 2
    if not isinstance(document, dict):
        print("FAIL G10.1-MAP\nE_INPUT: top-level JSON value must be an object")
        return 2

    findings = validate_submission(document, args.input)
    if findings:
        print("FAIL G10.1-MAP")
        for finding in findings:
            print(f"{finding.code}: {finding.message}")
        return 1

    print(pass_line(document, args.input))
    return 0


if __name__ == "__main__":
    sys.exit(main())
