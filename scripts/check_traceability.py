#!/usr/bin/env python3
"""Validate requirement IDs and lifecycle-dependent traceability evidence."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROW_RE = re.compile(r"^\|\s*(REQ-(?:[A-Z]+-)+[0-9]{3})\s*\|", re.MULTILINE)


def ids_in(text: str) -> list[str]:
    return ROW_RE.findall(text)


def requirement_statuses(text: str) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"REQ-(?:[A-Z]+-)+[0-9]{3}", cells[0]):
            statuses[cells[0]] = cells[-1]
    return statuses


def trace_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"REQ-(?:[A-Z]+-)+[0-9]{3}", cells[0]):
            rows[cells[0]] = cells[1:]
    return rows


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    requirement_text = (root / "docs/requirements.md").read_text(encoding="utf-8")
    requirements = ids_in(requirement_text)
    statuses = requirement_statuses(requirement_text)
    trace_text = (root / "docs/traceability.md").read_text(encoding="utf-8")
    trace_table = trace_text.split("\n## Link format", maxsplit=1)[0]
    traced = ids_in(trace_table)

    failures: list[str] = []
    for label, values in (("requirements", requirements), ("traceability", traced)):
        duplicates = sorted(key for key, count in Counter(values).items() if count > 1)
        if duplicates:
            failures.append(f"duplicate {label} IDs: {', '.join(duplicates)}")

    missing = sorted(set(requirements) - set(traced))
    extra = sorted(set(traced) - set(requirements))
    if missing:
        failures.append(f"requirements missing from traceability: {', '.join(missing)}")
    if extra:
        failures.append(f"traceability IDs not declared as requirements: {', '.join(extra)}")

    rows = trace_rows(trace_table)
    placeholders = {"", "—", "Planned", "Not run"}
    valid_statuses = {"Draft", "Baselined", "Implemented", "Verified"}
    markdown_link = re.compile(r"\[[^\]]+\]\([^)]+\)")
    verified_result = re.compile(
        r"\bPass\s*@\s*(?:`?[0-9a-f]{40}`?|\[[^\]]+\]\(https?://[^)]+\)|https?://\S+)"
    )
    for requirement_id, status in statuses.items():
        row = rows.get(requirement_id, [])
        if len(row) != 5:
            failures.append(f"{requirement_id}: expected five traceability fields")
            continue
        design, implementation, verification, result, reviewer = row
        if status not in valid_statuses:
            failures.append(f"{requirement_id}: unknown lifecycle status {status!r}")
            continue
        if status == "Baselined":
            missing_links = [
                name
                for name, value in (("design", design), ("verification", verification))
                if value in placeholders or not markdown_link.search(value)
            ]
            if missing_links:
                failures.append(
                    f"{requirement_id}: Baselined requirement needs linked "
                    f"{', '.join(missing_links)}"
                )
        if status in {"Implemented", "Verified"}:
            missing_links = [
                name
                for name, value in (
                    ("design", design),
                    ("implementation", implementation),
                    ("verification", verification),
                )
                if value in placeholders or not markdown_link.search(value)
            ]
            if missing_links:
                failures.append(
                    f"{requirement_id}: {status} requirement has placeholder "
                    f"{', '.join(missing_links)}"
                )
        if status == "Verified":
            if not verified_result.search(result):
                failures.append(
                    f"{requirement_id}: Verified result needs Pass @ full commit SHA or CI URL"
                )
            if reviewer in placeholders:
                failures.append(f"{requirement_id}: Verified requirement needs a reviewer")

    if failures:
        print("Requirement traceability check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Requirement traceability: OK ({len(requirements)} IDs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
