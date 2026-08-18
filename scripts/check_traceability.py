#!/usr/bin/env python3
"""Ensure every declared requirement has exactly one traceability row."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROW_RE = re.compile(r"^\|\s*(REQ-[A-Z]+-[0-9]{3})\s*\|", re.MULTILINE)


def ids_in(text: str) -> list[str]:
    return ROW_RE.findall(text)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    requirements = ids_in((root / "docs/requirements.md").read_text(encoding="utf-8"))
    trace_text = (root / "docs/traceability.md").read_text(encoding="utf-8")
    trace_table = trace_text.split("\n## 링크 형식 예시", maxsplit=1)[0]
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

    if failures:
        print("Requirement traceability check failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Requirement traceability: OK ({len(requirements)} IDs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
