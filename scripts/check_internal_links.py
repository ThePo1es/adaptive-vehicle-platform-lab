#!/usr/bin/env python3
"""Validate local Markdown links without making network requests."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SCHEMES = {"http", "https", "mailto", "tel", "data"}


def destination(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")]
    return value.split(maxsplit=1)[0]


def mask_fenced_code(text: str) -> str:
    """Keep line positions while hiding links inside fenced code blocks."""
    output: list[str] = []
    active_fence: str | None = None

    for line in text.splitlines(keepends=True):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if active_fence is None:
                active_fence = token[0]
            elif token[0] == active_fence:
                active_fence = None
            output.append("\n" if line.endswith("\n") else "")
        elif active_fence is None:
            output.append(line)
        else:
            output.append("\n" if line.endswith("\n") else "")

    return "".join(output)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    failures: list[str] = []

    for markdown in sorted(root.rglob("*.md")):
        if ".git" in markdown.parts:
            continue

        text = markdown.read_text(encoding="utf-8")
        searchable_text = mask_fenced_code(text)
        for match in LINK_RE.finditer(searchable_text):
            raw = destination(match.group(1))
            if not raw or raw.startswith("#"):
                continue

            parsed = urlsplit(raw)
            if parsed.scheme.lower() in SCHEMES or parsed.netloc:
                continue

            local_path = unquote(parsed.path)
            if not local_path:
                continue

            if local_path.startswith("/"):
                candidate = root / local_path.lstrip("/")
            else:
                candidate = markdown.parent / local_path

            if not candidate.exists():
                line = text.count("\n", 0, match.start()) + 1
                failures.append(
                    f"{markdown.relative_to(root)}:{line}: missing target {raw!r}"
                )

    if failures:
        print("Internal Markdown link check failed:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1

    print("Internal Markdown links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
