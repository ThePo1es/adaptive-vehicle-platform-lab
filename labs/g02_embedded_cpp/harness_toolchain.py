from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Final, NamedTuple

PINNED_ZIG_VERSION: Final = "0.15.2"
COMPILER_TIMEOUT_SECONDS: Final = 120
TOOLCHAIN_PROBE_TIMEOUT_SECONDS: Final = 30


class ToolchainError(Exception):
    pass


class ToolchainIdentity(NamedTuple):
    version: str
    target: str


def compiler_prefix(compiler: Path) -> tuple[str, ...]:
    return (str(compiler), "c++")


def _zig_package_binary() -> Path | None:
    spec = importlib.util.find_spec("ziglang")
    if spec is None or spec.submodule_search_locations is None:
        return None
    package_root = Path(next(iter(spec.submodule_search_locations)))
    binary = package_root / ("zig.exe" if os.name == "nt" else "zig")
    return binary if binary.is_file() else None


def _identity(compiler: Path) -> ToolchainIdentity:
    version = subprocess.run(
        [str(compiler), "version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=TOOLCHAIN_PROBE_TIMEOUT_SECONDS,
    )
    observed_version = version.stdout.strip()
    if version.returncode != 0 or observed_version != PINNED_ZIG_VERSION:
        raise ToolchainError(
            f"Zig {PINNED_ZIG_VERSION} is required, found {observed_version or 'unknown'}"
        )
    target = subprocess.run(
        [*compiler_prefix(compiler), "-dumpmachine"],
        check=False,
        capture_output=True,
        text=True,
        timeout=TOOLCHAIN_PROBE_TIMEOUT_SECONDS,
    )
    observed_target = target.stdout.strip()
    if target.returncode != 0 or not observed_target.startswith("x86_64"):
        raise ToolchainError(f"native x86_64 C++ target is required, found {observed_target}")
    return ToolchainIdentity(observed_version, observed_target)


def verify_hosted_cpp20(compiler: Path) -> None:
    source = (
        "#include <atomic>\n#include <thread>\n"
        "int main(){std::atomic<int> v{0};std::thread t([&]{v=1;});t.join();return v!=1;}\n"
    )
    with tempfile.TemporaryDirectory(prefix="g02-toolchain-") as temporary:
        output = Path(temporary) / ("probe.exe" if os.name == "nt" else "probe")
        result = subprocess.run(
            [
                *compiler_prefix(compiler),
                "-std=c++20",
                "-x",
                "c++",
                "-",
                "-o",
                str(output),
            ],
            input=source,
            check=False,
            capture_output=True,
            text=True,
            timeout=COMPILER_TIMEOUT_SECONDS,
        )
        if result.returncode == 0:
            execution = subprocess.run(
                [str(output)],
                check=False,
                capture_output=True,
                timeout=10,
            )
            if execution.returncode == 0:
                return
    diagnostic = (result.stdout + result.stderr).strip().splitlines()
    detail = diagnostic[-1] if diagnostic else "probe execution failed"
    raise ToolchainError(f"hosted C++20 thread probe failed: {detail}")


def resolve_compiler() -> tuple[Path, ToolchainIdentity]:
    compiler = _zig_package_binary()
    if compiler is None:
        raise ToolchainError("ziglang==0.15.2 is not installed in the verifier environment")
    identity = _identity(compiler)
    verify_hosted_cpp20(compiler)
    return compiler, identity
