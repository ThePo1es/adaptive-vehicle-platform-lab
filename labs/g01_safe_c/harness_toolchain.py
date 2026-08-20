from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Final, NamedTuple

PINNED_ZIG_VERSION: Final = "0.15.2"
MINIMUM_CLANG_MAJOR: Final = 18


class ToolchainError(Exception):
    pass


class ToolchainIdentity(NamedTuple):
    kind: str
    version: str
    target: str


def compiler_prefix(compiler: Path) -> tuple[str, ...]:
    if compiler.name.lower() in {"zig", "zig.exe"}:
        return (str(compiler), "cc")
    return (str(compiler),)


def _zig_package_binary() -> Path | None:
    spec = importlib.util.find_spec("ziglang")
    if spec is None or spec.submodule_search_locations is None:
        return None
    package_root = Path(next(iter(spec.submodule_search_locations)))
    binary = package_root / ("zig.exe" if os.name == "nt" else "zig")
    return binary if binary.is_file() else None


def _candidate(value: str | None) -> Path | None:
    if not value:
        return None
    discovered = shutil.which(value)
    return Path(discovered) if discovered else Path(value)


def _candidates() -> tuple[Path, ...]:
    raw = (
        _candidate(os.environ.get("CC")),
        _zig_package_binary(),
        _candidate("zig"),
        _candidate("clang"),
        Path("C:/Program Files/LLVM/bin/clang.exe"),
    )
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in raw:
        if candidate is None or not candidate.is_file():
            continue
        resolved = candidate.resolve()
        key = str(resolved).casefold()
        if key not in seen:
            unique.append(resolved)
            seen.add(key)
    return tuple(unique)


def _identity(compiler: Path) -> ToolchainIdentity:
    is_zig = compiler.name.lower() in {"zig", "zig.exe"}
    version_command = [str(compiler), "version"] if is_zig else [str(compiler), "--version"]
    version_result = subprocess.run(
        version_command,
        check=False,
        capture_output=True,
        text=True,
    )
    if version_result.returncode != 0:
        raise ToolchainError("version query failed")
    first_line = (version_result.stdout or version_result.stderr).splitlines()[0].strip()
    if is_zig:
        if first_line != PINNED_ZIG_VERSION:
            raise ToolchainError(
                f"Zig {PINNED_ZIG_VERSION} is required, found {first_line or 'unknown'}"
            )
        kind = "zig"
        version = first_line
    else:
        match = re.search(r"clang version (\d+)(?:\.([0-9.]+))?", first_line)
        if match is None or int(match.group(1)) < MINIMUM_CLANG_MAJOR:
            raise ToolchainError(f"Clang {MINIMUM_CLANG_MAJOR}+ is required, found {first_line}")
        kind = "clang"
        version = match.group(0).removeprefix("clang version ")
    target_result = subprocess.run(
        [*compiler_prefix(compiler), "-dumpmachine"],
        check=False,
        capture_output=True,
        text=True,
    )
    target = target_result.stdout.strip()
    if target_result.returncode != 0 or not target:
        raise ToolchainError("target query failed")
    return ToolchainIdentity(kind, version, target)


def _probe(compiler: Path) -> None:
    source = "#include <stdint.h>\n#include <stdio.h>\nint main(void){return puts(\"probe\") < 0;}\n"
    with tempfile.TemporaryDirectory(prefix="g01-toolchain-") as temporary:
        output = Path(temporary) / "probe"
        result = subprocess.run(
            [*compiler_prefix(compiler), "-std=c17", "-x", "c", "-", "-o", str(output)],
            input=source,
            check=False,
            capture_output=True,
            text=True,
        )
    if result.returncode != 0:
        diagnostic = (result.stdout + result.stderr).strip().splitlines()
        detail = diagnostic[-1] if diagnostic else "unknown compile failure"
        raise ToolchainError(f"hosted C17 probe failed: {detail}")


def resolve_compiler() -> tuple[Path, ToolchainIdentity]:
    failures: list[str] = []
    for compiler in _candidates():
        try:
            identity = _identity(compiler)
            _probe(compiler)
            return compiler, identity
        except (OSError, ToolchainError) as error:
            failures.append(f"{compiler}: {error}")
    detail = "; ".join(failures) if failures else "no candidate executable was found"
    raise ToolchainError(
        "no supported C toolchain passed the hosted-header probe; "
        "run with uv --with ziglang==0.15.2 or set CC. "
        f"Tried: {detail}"
    )
