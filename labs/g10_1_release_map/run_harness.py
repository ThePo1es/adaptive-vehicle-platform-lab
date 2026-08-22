#!/usr/bin/env python3
"""Replay the public positive and negative cases for the G10.1 validator."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

from validator import MAPPING_STATUSES, pass_line, validate_harness


REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "fixtures/g10/release-map-cases-v1.json"


def replace_at_pointer(document: dict[str, Any], pointer: str, value: Any) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    target: Any = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    leaf = parts[-1]
    if isinstance(target, list):
        target[int(leaf)] = value
    else:
        target[leaf] = value


def remove_at_pointer(document: dict[str, Any], pointer: str) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]]
    target: Any = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    leaf = parts[-1]
    if isinstance(target, list):
        del target[int(leaf)]
    else:
        del target[leaf]


def apply_operation(document: dict[str, Any], case: dict[str, Any]) -> None:
    operation = case["operation"]
    if operation == "replace":
        replace_at_pointer(document, case["path"], case["value"])
        return
    if operation == "remove":
        remove_at_pointer(document, case["path"])
        return
    if operation == "set-all-mapping-status":
        for node in document["nodes"]:
            node["mapping_status"] = case["value"]
            if case["value"] in {"Missing", "Out of scope"}:
                node["claim_type"] = "known-gap"
                node["observed_behavior"]["readiness"] = "not-observed"
        document["summary"] = {
            status: len(document["nodes"]) if status == case["value"] else 0
            for status in MAPPING_STATUSES
        }
        return
    if operation == "set-all-local-evidence":
        for node in document["nodes"]:
            node["local_evidence"] = copy.deepcopy(case["value"])
        return
    raise AssertionError(f"unknown fixture operation: {operation}")


def run() -> list[str]:
    case_set = json.loads(CASES.read_text(encoding="utf-8"))
    base = case_set["guided_submission"]
    findings = validate_harness(base)
    if findings:
        joined = ",".join(finding.code for finding in findings)
        raise AssertionError(f"guided case failed: {joined}")

    lines = [pass_line(base)]
    for case in case_set["negative_cases"]:
        mutated = copy.deepcopy(base)
        apply_operation(mutated, case)
        observed = sorted({finding.code for finding in validate_harness(mutated)})
        expected = sorted(case["expected_errors"])
        if observed != expected:
            raise AssertionError(f"{case['id']}: expected {expected}, observed {observed}")
        lines.append(
            f"PASS negative={case['id']} expected={','.join(expected)} observed={','.join(observed)}"
        )

    lines.append(f"G10.1 harness: PASS (1 valid, {len(case_set['negative_cases'])} negative cases)")
    return lines


def main() -> int:
    try:
        for line in run():
            print(line)
    except (AssertionError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"G10.1 harness: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
