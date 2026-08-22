from __future__ import annotations

from pathlib import Path


class HarnessInputError(Exception):
    pass


def resolve_source_root(candidate: Path, repository_root: Path) -> Path:
    resolved = candidate.resolve()
    if not resolved.is_relative_to(repository_root) or not resolved.is_dir():
        raise HarnessInputError(
            f"submission root must be an existing repository directory: {candidate}"
        )
    return resolved


def require_trusted_submission(
    submission: str | None,
    trust: str | None,
    repository_root: Path,
    reference_root: Path,
) -> Path:
    if submission is None:
        return reference_root
    if trust != "1":
        raise HarnessInputError(
            "set G02_TRUSTED_LOCAL_EXECUTION=1 only for code you wrote or reviewed"
        )
    return resolve_source_root(Path(submission), repository_root)


def resolve_submission_source(source_root: Path, filename: str) -> Path:
    candidate = source_root / filename
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as error:
        raise HarnessInputError(f"submission source is missing: {candidate}") from error
    if candidate.is_symlink() or not resolved.is_relative_to(source_root) or not resolved.is_file():
        raise HarnessInputError(
            f"submission source must be a regular file inside its source root: {candidate}"
        )
    return resolved
