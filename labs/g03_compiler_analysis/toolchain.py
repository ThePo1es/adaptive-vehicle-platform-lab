from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final, override

PINNED_ZIG_VERSION: Final = "0.15.2"
PINNED_CLANG_VERSION: Final = "20.1.2"
PINNED_GNU_RELEASE: Final = "14.3.Rel1"
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
    expected = GNU_ARCHIVES.get(archive.name)
    if expected is None:
        raise ToolchainError(f"unsupported GNU archive name: {archive.name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != expected:
        raise ToolchainError(
            f"GNU archive SHA-256 mismatch: observed={digest} expected={expected}"
        )
    return digest


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
    archive_value = os.environ.get("G03_GNU_ARCHIVE")
    root_value = os.environ.get("G03_GNU_ROOT")
    if archive_value is None or root_value is None:
        raise ToolchainError("G03_GNU_ARCHIVE and G03_GNU_ROOT are both required")
    archive = Path(archive_value).resolve()
    _ = verify_gnu_archive(archive)
    executable = "arm-none-eabi-gcc.exe" if os.name == "nt" else "arm-none-eabi-gcc"
    compiler = Path(root_value).resolve() / "bin" / executable
    if not compiler.is_file():
        raise ToolchainError(f"GNU compiler is missing: {compiler}")
    result = subprocess.run(
        [str(compiler), "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0 or "14.3.1" not in result.stdout.splitlines()[0]:
        raise ToolchainError(f"Arm GNU Toolchain {PINNED_GNU_RELEASE} is required")
    return GnuToolchain(compiler, archive)
