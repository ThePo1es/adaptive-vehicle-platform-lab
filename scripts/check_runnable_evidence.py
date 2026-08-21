#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import tarfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.runnable_evidence_support import (
    EVIDENCE_ROOT,
    REPO_ROOT,
    active_manifest_paths,
    fail,
    runnable_gate_lab_ids,
)
from scripts.runnable_evidence_validator import verify_manifest

HISTORICAL_REPLAY_WORKERS = 2


def verify_manifests(manifests: list[Path], active: dict[str, str]) -> list[str]:
    verified: dict[Path, str] = {}
    historical: list[Path] = []
    repository_checks: set[tuple[str, str, str]] = set()

    for path in manifests:
        relative = str(path.relative_to(REPO_ROOT))
        if relative in active:
            verified[path] = verify_manifest(
                path,
                True,
                active[relative],
                repository_checks,
            )
        else:
            historical.append(path)

    with ThreadPoolExecutor(
        max_workers=HISTORICAL_REPLAY_WORKERS,
        thread_name_prefix="runnable-evidence",
    ) as executor:
        futures = {
            executor.submit(verify_manifest, path, False, None, None): path
            for path in historical
        }
        for future in as_completed(futures):
            path = futures[future]
            verified[path] = future.result()

    return [verified[path] for path in manifests]


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
        verified = verify_manifests(manifests, active)
        discovered = {str(path.relative_to(REPO_ROOT)) for path in manifests}
        missing_active = set(active) - discovered
        if missing_active:
            fail(f"active manifests were not discovered: {', '.join(sorted(missing_active))}")
    except (OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
        print(f"Runnable evidence: FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"Runnable evidence: OK ({len(verified)} manifest, {len(active)} active: {', '.join(verified)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
