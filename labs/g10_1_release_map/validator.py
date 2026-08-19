#!/usr/bin/env python3
"""Validate the boundary map used by the G10.1 release-map lab."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


EXPECTED_STAGES = (
    ("Service Interface", "design-time"),
    ("Proxy/Skeleton", "generation-time"),
    ("Service Instance/Deployment", "deployment-time"),
    ("SOME/IP binding", "deployment-time"),
    ("Executable/Process", "deployment-to-runtime"),
    ("Function Group State", "runtime"),
    ("Health Supervision", "runtime"),
)
MAPPING_STATUSES = ("Mapped", "Partial", "Missing", "Out of scope")
EXPECTED_BOUNDARY = {
    "decision_owner": "State Management",
    "action_owner": "Execution Management",
    "observation_owner": "Platform Health Management",
}
FORBIDDEN_CLAIMS = (
    re.compile(r"\bAUTOSAR[- ]?(?:R25-11[- ]?)?(?:compliant|conformant)\b", re.IGNORECASE),
    re.compile(r"\bofficial AUTOSAR implementation\b", re.IGNORECASE),
    re.compile(r"\bara::com implementation\b", re.IGNORECASE),
)
PLACEHOLDER = re.compile(r"(?:\bTODO\b|\bTBD\b|<[^>]+>|확인 필요|미작성)", re.IGNORECASE)
OFFICIAL_SOURCE_PREFIX = "https://www.autosar.org/"
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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


def _present_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not PLACEHOLDER.search(value)


def validate(document: dict[str, Any], profile: str | None = None) -> list[Finding]:
    findings: list[Finding] = []

    if document.get("schema_version") != 1:
        findings.append(Finding("E_SCHEMA", "schema_version must be 1"))

    selected_profile = profile or document.get("profile")
    if selected_profile not in {"harness", "submission"}:
        findings.append(Finding("E_PROFILE", "profile must be harness or submission"))

    if document.get("release") != "R25-11":
        findings.append(Finding("E_RELEASE", "release must be R25-11"))

    if document.get("claim_scope") != "concept-aligned local prototype":
        findings.append(
            Finding(
                "E_SCOPE_CLAIM",
                "claim_scope must remain 'concept-aligned local prototype'",
            )
        )

    for text in _strings(document):
        if any(pattern.search(text) for pattern in FORBIDDEN_CLAIMS):
            findings.append(Finding("E_SCOPE_CLAIM", f"unsupported conformance claim: {text!r}"))
            break

    rows = document.get("rows")
    if not isinstance(rows, list) or len(rows) != len(EXPECTED_STAGES):
        findings.append(Finding("E_STAGE_COUNT", "rows must contain exactly seven stages"))
        rows = []

    if rows:
        observed_stages = [row.get("stage") if isinstance(row, dict) else None for row in rows]
        if observed_stages != [stage for stage, _ in EXPECTED_STAGES]:
            findings.append(Finding("E_STAGE_ORDER", "stage order does not match the G9→G10 responsibility path"))

        positions = [row.get("position") if isinstance(row, dict) else None for row in rows]
        if positions != list(range(1, len(EXPECTED_STAGES) + 1)):
            findings.append(Finding("E_STAGE_POSITION", "position values must be the ordered integers 1 through 7"))

        required_fields = (
            "artifact",
            "local_component",
            "runtime_actor",
            "configuration_source",
            "failure_observation",
            "implementation_origin",
        )
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                findings.append(Finding("E_ROW", f"row {index + 1} must be an object"))
                continue

            expected_phase = EXPECTED_STAGES[index][1]
            if row.get("artifact_phase") != expected_phase:
                findings.append(Finding("E_PHASE", f"row {index + 1} phase must be {expected_phase}"))

            for field in required_fields:
                if not _present_string(row.get(field)):
                    findings.append(Finding("E_ROW_FIELD", f"row {index + 1} has no concrete {field}"))

            for field in ("upstream", "downstream", "limitations", "citation_ids"):
                values = row.get(field)
                if not isinstance(values, list) or not values or not all(_present_string(value) for value in values):
                    findings.append(Finding("E_ROW_FIELD", f"row {index + 1} needs a concrete {field} list"))

            if row.get("implementation_origin") != "local-prototype":
                findings.append(
                    Finding(
                        "E_IMPLEMENTATION_ORIGIN",
                        f"row {index + 1} must identify the local-prototype origin",
                    )
                )

            if row.get("mapping_status") not in MAPPING_STATUSES:
                findings.append(Finding("E_MAPPING_STATUS", f"row {index + 1} has an unknown mapping status"))

            actor = row.get("runtime_actor")
            if expected_phase == "design-time" and actor != "none (design-time)":
                findings.append(Finding("E_ARTIFACT_RUNTIME", "a design-time artifact cannot be presented as a runtime actor"))
            if expected_phase == "runtime" and actor == "none (design-time)":
                findings.append(Finding("E_ARTIFACT_RUNTIME", f"row {index + 1} needs a runtime actor"))

    ledger = document.get("source_ledger")
    if not isinstance(ledger, list) or not ledger:
        findings.append(Finding("E_SOURCE_LEDGER", "source_ledger must contain at least one citation"))
        ledger = []

    citation_ids: set[str] = set()
    for index, source in enumerate(ledger):
        if not isinstance(source, dict):
            findings.append(Finding("E_SOURCE_LEDGER", f"source {index + 1} must be an object"))
            continue
        citation_id = source.get("citation_id")
        if not _present_string(citation_id) or citation_id in citation_ids:
            findings.append(Finding("E_SOURCE_LEDGER", f"source {index + 1} needs a unique citation_id"))
        else:
            citation_ids.add(citation_id)

        if selected_profile == "submission":
            if source.get("source_kind") != "official":
                findings.append(Finding("E_SOURCE_KIND", f"source {index + 1} must be an official AUTOSAR source"))
            if source.get("release") != "R25-11":
                findings.append(Finding("E_RELEASE", f"source {index + 1} must be pinned to R25-11"))
            if source.get("access_status") != "Direct":
                findings.append(Finding("E_SOURCE_ACCESS", f"source {index + 1} has not been read directly"))
            if not str(source.get("source_url", "")).startswith(OFFICIAL_SOURCE_PREFIX):
                findings.append(Finding("E_SOURCE_KIND", f"source {index + 1} URL is not on autosar.org"))
            if not str(source.get("document_id", "")).startswith("AUTOSAR_"):
                findings.append(Finding("E_CITATION_ID", f"source {index + 1} has no AUTOSAR document ID"))
            for field in ("section_title", "section_locator", "accessed_on"):
                if not _present_string(source.get(field)):
                    findings.append(Finding("E_CITATION_LOCATOR", f"source {index + 1} needs a concrete {field}"))
            accessed_on = source.get("accessed_on")
            if _present_string(accessed_on) and not ISO_DATE.fullmatch(accessed_on):
                findings.append(Finding("E_CITATION_DATE", f"source {index + 1} accessed_on must use YYYY-MM-DD"))

    if rows and citation_ids:
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            unknown = sorted(set(row.get("citation_ids", [])) - citation_ids)
            if unknown:
                findings.append(Finding("E_CITATION_REF", f"row {index + 1} cites unknown IDs: {', '.join(unknown)}"))

    if rows:
        observed_summary = Counter(row.get("mapping_status") for row in rows if isinstance(row, dict))
        expected_summary = {status: observed_summary.get(status, 0) for status in MAPPING_STATUSES}
        if document.get("summary") != expected_summary:
            findings.append(Finding("E_SUMMARY", "summary does not match the row mapping statuses"))

    boundary = document.get("lifecycle_boundary")
    if not isinstance(boundary, dict):
        findings.append(Finding("E_OWNER_BOUNDARY", "lifecycle_boundary must be an object"))
    else:
        if any(boundary.get(field) != owner for field, owner in EXPECTED_BOUNDARY.items()):
            findings.append(
                Finding(
                    "E_OWNER_BOUNDARY",
                    "the scenario must keep SM decision, EM action and PHM observation separate",
                )
            )
        counts = boundary.get("ownership_counts")
        if counts != {"decision": 1, "action": 1, "observation": 1}:
            findings.append(Finding("E_OWNER_COUNT", "each lifecycle role must have exactly one owner"))
        for field in ("scenario", "requested_target", "action", "observation"):
            if not _present_string(boundary.get(field)):
                findings.append(Finding("E_OWNER_BOUNDARY", f"lifecycle_boundary needs a concrete {field}"))

    return sorted(set(findings))


def pass_line(document: dict[str, Any]) -> str:
    summary = document["summary"]
    counts = ",".join(f"{status}:{summary[status]}" for status in MAPPING_STATUSES)
    return f"PASS G10.1-MAP rows={len(document['rows'])} citations={len(document['source_ledger'])} statuses={counts}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--profile", choices=("harness", "submission"))
    args = parser.parse_args()

    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL G10.1-MAP\nE_INPUT: {exc}")
        return 2

    if not isinstance(document, dict):
        print("FAIL G10.1-MAP\nE_INPUT: top-level JSON value must be an object")
        return 2

    findings = validate(document, args.profile)
    if findings:
        print("FAIL G10.1-MAP")
        for finding in findings:
            print(f"{finding.code}: {finding.message}")
        return 1

    print(pass_line(document))
    return 0


if __name__ == "__main__":
    sys.exit(main())
