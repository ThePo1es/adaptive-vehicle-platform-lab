#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import sys
import tarfile
from collections.abc import Mapping
from pathlib import Path

from scripts.runnable_evidence_support import (
    EVIDENCE_ROOT,
    REPO_ROOT,
    active_manifest_paths,
    fail,
    runnable_gate_lab_ids,
)
from scripts.runnable_evidence_validator import verify_manifest

SHARD_COUNT_VARIABLE = "RUNNABLE_EVIDENCE_SHARD_COUNT"
SHARD_INDEX_VARIABLE = "RUNNABLE_EVIDENCE_SHARD_INDEX"


def replay_shard(environment: Mapping[str, str]) -> tuple[int, int]:
    raw_count = environment.get(SHARD_COUNT_VARIABLE, "1")
    raw_index = environment.get(SHARD_INDEX_VARIABLE, "0")
    try:
        count = int(raw_count)
        index = int(raw_index)
    except ValueError:
        fail("replay shard count and index must be integers")
    if count < 1:
        fail("replay shard count must be positive")
    if index < 0 or index >= count:
        fail("replay shard index must be between 0 and count - 1")
    return count, index


def selected_manifest_paths(
    manifests: list[Path],
    active: dict[str, str],
    shard_count: int,
    shard_index: int,
) -> list[Path]:
    selected: list[Path] = []
    historical_index = 0
    for path in manifests:
        relative = str(path.relative_to(REPO_ROOT))
        if relative in active:
            if shard_index == 0:
                selected.append(path)
            continue
        if historical_index % shard_count == shard_index:
            selected.append(path)
        historical_index += 1
    return selected


def verify_manifests(
    manifests: list[Path],
    active: dict[str, str],
    shard_count: int,
    shard_index: int,
) -> list[str]:
    verified: list[str] = []
    repository_checks: set[tuple[str, str, str]] = set()
    for path in selected_manifest_paths(manifests, active, shard_count, shard_index):
        relative = str(path.relative_to(REPO_ROOT))
        is_active = relative in active
        verified.append(
            verify_manifest(
                path,
                is_active,
                active.get(relative),
                repository_checks if is_active else None,
            )
        )
    return verified


def main() -> int:
    try:
        active = active_manifest_paths()
        gate_runnable = runnable_gate_lab_ids()
        indexed_runnable = set(active.values())
        if indexed_runnable != gate_runnable:
            detail = f"index={sorted(indexed_runnable)}, gates={sorted(gate_runnable)}"
            fail(f"active index and Runnable Sprint headers differ: {detail}")
        manifests = sorted(EVIDENCE_ROOT.glob("*/run-manifest*.json"))
        if not manifests:
            fail("no Runnable manifests found")
        shard_count, shard_index = replay_shard(os.environ)
        verified = verify_manifests(manifests, active, shard_count, shard_index)
        discovered = {str(path.relative_to(REPO_ROOT)) for path in manifests}
        missing_active = set(active) - discovered
        if missing_active:
            fail(f"active manifests were not discovered: {', '.join(sorted(missing_active))}")
    except (OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
        print(f"Runnable evidence: FAIL: {exc}", file=sys.stderr)
        return 1
    active_count = len(active) if shard_index == 0 else 0
    summary = "Runnable evidence: OK "
    summary += f"(shard {shard_index + 1}/{shard_count}, {len(verified)} manifest, "
    summary += f"{active_count} active: {', '.join(verified)})"
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
