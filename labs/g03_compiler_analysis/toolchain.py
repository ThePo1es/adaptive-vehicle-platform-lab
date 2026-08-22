from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final, override

from .gnu_provision import (
    ProvisionError,
    compiler_environment,
    provision,
    read_entry,
    verify_archive,
)

PINNED_ZIG_VERSION: Final = "0.15.2"
PINNED_CLANG_VERSION: Final = "20.1.2"
PINNED_GNU_RELEASE: Final = "14.3.Rel1"
REPO_ROOT: Final = Path(__file__).resolve().parents[2]
MANIFEST_PATH: Final = REPO_ROOT / "toolchain/g03-arm-gnu.json"
GNU_ARCHIVES: Final = {
    "arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi.tar.xz": (
        "8f6903f8ceb084d9227b9ef991490413014d991874a1e34074443c2a72b14dbd"
    ),
    "arm-gnu-toolchain-14.3.rel1-mingw-w64-x86_64-arm-none-eabi.zip": (
        "864c0c8815857d68a1bbba2e5e2782255bb922845c71c97636004a3d74f60986"
    ),
}


@dataclass(frozen=True, slots=True)
class ToolchainError(Exception):
    reason: str

    @override
    def __str__(self) -> str:
        return self.reason


@dataclass(frozen=True, slots=True)
class GnuToolchain:
    compiler: Path
    archive: Path


def verify_gnu_archive(archive: Path) -> str:
    try:
        return verify_archive(archive, read_entry(MANIFEST_PATH))
    except ProvisionError as error:
        raise ToolchainError(str(error)) from error


def resolve_zig() -> Path:
    spec = importlib.util.find_spec("ziglang")
    if spec is None or spec.submodule_search_locations is None:
        raise ToolchainError("ziglang==0.15.2 is not installed")
    root = Path(next(iter(spec.submodule_search_locations)))
    binary = root / ("zig.exe" if os.name == "nt" else "zig")
    if not binary.is_file():
        raise ToolchainError(f"Zig binary is missing: {binary}")
    result = subprocess.run(
        [str(binary), "version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0 or result.stdout.strip() != PINNED_ZIG_VERSION:
        raise ToolchainError(f"Zig {PINNED_ZIG_VERSION} is required")
    return binary


def resolve_gnu() -> GnuToolchain:
    cache = Path(os.environ.get("G03_GNU_CACHE", REPO_ROOT / ".cache/g03-arm-gnu"))
    try:
        resolved = provision(MANIFEST_PATH, cache.resolve(), download=False)
    except (OSError, ProvisionError, subprocess.SubprocessError) as error:
        raise ToolchainError(str(error)) from error
    return GnuToolchain(resolved.compiler, resolved.archive)


def provision_main() -> int:
    cache = Path(os.environ.get("G03_GNU_CACHE", REPO_ROOT / ".cache/g03-arm-gnu"))
    try:
        resolved = provision(MANIFEST_PATH, cache.resolve(), download="--download" in sys.argv)
    except (OSError, ProvisionError, subprocess.SubprocessError) as error:
        print(f"G3 GNU provision: FAIL: {error}", file=sys.stderr)
        return 1
    version = subprocess.run(
        [str(resolved.compiler), "--version"],
        env=compiler_environment(),
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()[0]
    print(f"archive={resolved.archive}")
    print(f"sha256={resolved.digest}")
    print(f"dumpmachine={resolved.machine}")
    print(f"dumpfullversion={resolved.version}")
    print(f"version={version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(provision_main())
