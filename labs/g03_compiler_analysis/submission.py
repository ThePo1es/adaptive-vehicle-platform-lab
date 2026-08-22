from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import override


@dataclass(frozen=True, slots=True)
class SubmissionError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


def resolve_submission(candidate: str | None, trusted: str | None, reference: Path) -> Path:
    if candidate is None:
        return reference
    if trusted != "1":
        raise SubmissionError("G03_TRUSTED_LOCAL_EXECUTION=1 is required")
    root = Path(candidate).resolve()
    if not root.is_dir():
        raise SubmissionError(f"submission directory is missing: {root}")
    return root


def source_file(root: Path, name: str) -> Path:
    source = root / name
    if source.is_symlink() or not source.is_file() or source.resolve().parent != root:
        raise SubmissionError(f"submission file must be a direct regular file: {name}")
    return source
