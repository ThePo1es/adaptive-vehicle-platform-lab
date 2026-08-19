#!/usr/bin/env python3
"""Validate a G10.1 typed responsibility graph and its evidence links."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_LOCK = REPO_ROOT / "labs/g10_1_release_map/r25-11-document-lock.json"
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
)
PLACEHOLDER = re.compile(r"(?:\bTODO\b|\bTBD\b|<[^>]+>|확인 필요|미작성)", re.IGNORECASE)
NODE_ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
FULL_SHA256 = re.compile(r"^[0-9a-f]{64}$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_DIRECTORY = REPO_ROOT / "sources/autosar-r25-11"
REVIEW_DIRECTORY = REPO_ROOT / "evidence/reviews/g10.1"
REVIEW_SUBJECT_FIELDS = (
    "schema_version",
    "release",
    "claim_scope",
    "conformance_claim",
    "production_status",
    "source_ledger",
    "nodes",
    "edges",
    "selected_binding",
    "lifecycle_scenarios",
    "summary",
)


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


def _source_lock() -> dict[str, dict[str, Any]]:
    lock = json.loads(SOURCE_LOCK.read_text(encoding="utf-8"))
    return {entry["document_id"]: entry for entry in lock["documents"]}


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _review_subject_hash(document: dict[str, Any]) -> str:
    return _canonical_hash({field: document.get(field) for field in REVIEW_SUBJECT_FIELDS})


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


def _validate_review_manifest(
    review: dict[str, Any],
    document: dict[str, Any],
    citation_ids: set[str],
    node_ids: set[str],
    profile: str,
    findings: list[Finding],
) -> None:
    reviewer_id = review.get("reviewer_id")
    if not _meaningful(reviewer_id, 4):
        findings.append(Finding("E_REVIEW", "Reviewed status needs reviewer_id"))
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
    checks = (
        manifest.get("schema_version") == 1,
        manifest.get("lab_id") == "G10.1",
        manifest.get("decision") == "Approved",
        manifest.get("reviewer_id") == reviewer_id,
        isinstance(manifest_date, str) and bool(ISO_DATE.fullmatch(manifest_date)),
        manifest.get("claim_scope") == "concept-aligned local prototype",
        set(manifest.get("reviewed_citation_ids", [])) == citation_ids,
        set(manifest.get("reviewed_node_ids", [])) == node_ids,
        manifest.get("source_ledger_sha256") == _canonical_hash(document.get("source_ledger")),
        manifest.get("review_subject_sha256") == _review_subject_hash(document),
        manifest.get("local_evidence_sha256s") == expected_evidence_hashes,
        manifest.get("limitations_acknowledged") is True,
        _meaningful(manifest.get("review_notes"), 12),
    )
    if not all(checks):
        findings.append(Finding("E_REVIEW", "review manifest does not bind every claim, citation, limitation, and evidence hash"))
    if set(review.get("reviewed_citation_ids", [])) != citation_ids:
        findings.append(Finding("E_REVIEW", "reviewed citation set must cover the source ledger"))


def _validate_evidence(
    node: dict[str, Any],
    index: int,
    profile: str,
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
            if path is None or not path.is_file():
                findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence path is unavailable: {relative_path}"))
            elif hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
                findings.append(Finding("E_LOCAL_EVIDENCE", f"node {index} evidence hash drifted: {relative_path}"))


def _validate(document: dict[str, Any], profile: str) -> list[Finding]:
    findings: list[Finding] = []

    if document.get("schema_version") != 2:
        findings.append(Finding("E_SCHEMA", "schema_version must be 2"))
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

    for text in _strings(document):
        if any(pattern.search(text) for pattern in FORBIDDEN_CLAIMS):
            findings.append(Finding("E_SCOPE_CLAIM", f"unsupported conformance claim: {text!r}"))
            break

    ledger = document.get("source_ledger")
    if not isinstance(ledger, list) or not ledger:
        findings.append(Finding("E_SOURCE_LEDGER", "source_ledger must contain at least one citation"))
        ledger = []
    source_lock = _source_lock() if profile == "submission" else {}
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
    claims: list[str] = []
    evidence_path_roles: dict[str, set[str]] = {}
    if nodes:
        for index, node in enumerate(nodes, start=1):
            if not isinstance(node, dict):
                findings.append(Finding("E_NODE_FIELD", f"node {index} must be an object"))
                continue
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

            for field in ("artifact", "claim", "local_component", "configuration_source", "failure_observation"):
                if not _meaningful(node.get(field), 8):
                    findings.append(Finding("E_NODE_FIELD", f"node {index} needs a concrete {field}"))
            if isinstance(node.get("claim"), str):
                claims.append(node["claim"])

            status = node.get("mapping_status")
            if status not in MAPPING_STATUSES:
                findings.append(Finding("E_MAPPING_STATUS", f"node {index} has an unknown mapping status"))
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
            _validate_evidence(node, index, profile, findings)
            if status in {"Mapped", "Partial"} and isinstance(node.get("local_evidence"), list):
                for item in node["local_evidence"]:
                    if isinstance(item, dict) and isinstance(item.get("path"), str):
                        evidence_path_roles.setdefault(item["path"], set()).add(str(role))

        missing_or_duplicate = sorted(role for role in ROLE_MODEL if observed_roles[role] != 1)
        if missing_or_duplicate:
            findings.append(Finding("E_GRAPH_COVERAGE", f"required semantic roles must occur once: {', '.join(missing_or_duplicate)}"))
        if len(set(claims)) != len(claims):
            findings.append(Finding("E_NODE_FIELD", "node claims must be distinct"))
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
        _validate_review_manifest(review, document, citation_ids, node_ids, profile, findings)
    elif any(
        review.get(field) not in (None, "", [])
        for field in ("reviewer_id", "review_manifest_path", "review_manifest_sha256", "reviewed_citation_ids")
    ):
        findings.append(Finding("E_REVIEW", "Pending review fields must remain empty"))

    return sorted(set(findings))


def validate_harness(document: dict[str, Any]) -> list[Finding]:
    """Validate the repository-owned synthetic fixture."""
    return _validate(document, "harness")


def validate_submission(document: dict[str, Any]) -> list[Finding]:
    """Validate a learner submission with direct sources and local file hashes."""
    return _validate(document, "submission")


def pass_line(document: dict[str, Any]) -> str:
    profile = document.get("profile")
    if profile == "harness":
        findings = validate_harness(document)
    elif profile == "submission":
        findings = validate_submission(document)
    else:
        findings = [Finding("E_PROFILE_DOWNGRADE", "document profile is unknown")]
    if findings:
        codes = ",".join(sorted({finding.code for finding in findings}))
        raise ValueError(f"cannot emit a pass line for invalid evidence: {codes}")
    summary = document["summary"]
    counts = ",".join(f"{status}:{summary[status]}" for status in MAPPING_STATUSES)
    prefix = "REVIEWED_PASS" if document.get("review", {}).get("status") == "Reviewed" else "STRUCTURE_PASS"
    return (
        f"{prefix} G10.1-MAP nodes={len(document['nodes'])} edges={len(document['edges'])} "
        f"citations={len(document['source_ledger'])} statuses={counts} review={document['review']['status']}"
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

    findings = validate_submission(document)
    if findings:
        print("FAIL G10.1-MAP")
        for finding in findings:
            print(f"{finding.code}: {finding.message}")
        return 1

    print(pass_line(document))
    return 0


if __name__ == "__main__":
    sys.exit(main())
