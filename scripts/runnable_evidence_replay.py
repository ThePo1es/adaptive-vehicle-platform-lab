from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from scripts.runnable_evidence_support import (
    SHA256,
    canonical_output,
    digest,
    fail,
    repository_path,
)

PINNED_G1_ARGV_PREFIX = [
    "uv",
    "run",
    "--offline",
    "--python",
    "3.12.13",
    "--with",
    "ziglang==0.15.2",
    "python",
    "-m",
]
PINNED_G1_MODULE = "labs.g01_safe_c.run_harness"
PINNED_G2_ARGV_PREFIX = [
    "uv",
    "run",
    "--offline",
    "--python",
    "3.12.13",
    "--with",
    "ziglang==0.15.2",
    "--with",
    "pyelftools==0.32",
    "python",
    "-m",
]
PINNED_G2_MODULE = "labs.g02_embedded_cpp.run_harness"
WINDOWS_REPOSITORY_CHECK = "hash -p /usr/bin/bash bash; source scripts/check_repo.sh"


def repository_check_argv(
    platform_name: str,
    environment: Mapping[str, str],
) -> list[str]:
    if platform_name != "nt":
        return ["bash", "scripts/check_repo.sh"]
    configured = environment.get("GIT_BASH_EXE")
    if not configured:
        fail("GIT_BASH_EXE is required for Windows historical replay")
    executable = Path(configured)
    if not executable.is_file():
        fail(f"GIT_BASH_EXE is not a file: {configured}")
    return [str(executable), "-c", WINDOWS_REPOSITORY_CHECK]


def pinned_uv_version(value: str) -> bool:
    return re.fullmatch(r"uv 0\.12\.3(?: \(.+\))?", value) is not None


def replay_environment(manifest: dict[str, Any], base: dict[str, str]) -> dict[str, str]:
    environment = base.copy()
    lab_id = str(manifest.get("lab_id", ""))
    if manifest.get("schema_version") != 2 or not lab_id.startswith("G1."):
        return environment
    spec = importlib.util.find_spec("ziglang")
    if spec is None or spec.submodule_search_locations is None:
        fail("historical G1 replay requires ziglang==0.15.2 in the verifier environment")
    package_root = Path(next(iter(spec.submodule_search_locations)))
    compiler = package_root / ("zig.exe" if os.name == "nt" else "zig")
    if not compiler.is_file():
        fail("historical G1 replay could not locate the pinned Zig compiler")
    environment["CC"] = str(compiler)
    return environment


def verify_runtime(snapshot: Path, manifest: dict[str, Any]) -> None:
    expected = manifest.get("environment", {}).get("python")
    if not isinstance(expected, str):
        fail("manifest environment needs an exact Python version")
    schema_version = manifest["schema_version"]
    if schema_version == 2:
        version_command = [sys.executable, "--version"]
    elif schema_version == 3:
        version_command = [*PINNED_G1_ARGV_PREFIX[:-1], "--version"]
    else:
        version_command = [*PINNED_G2_ARGV_PREFIX[:-1], "--version"]
    version = subprocess.run(
        version_command,
        cwd=snapshot,
        check=False,
        capture_output=True,
        text=True,
    )
    observed = version.stdout.strip().removeprefix("Python ")
    if version.returncode != 0 or observed != expected:
        fail(f"Python version mismatch: expected {expected}, got {observed}")
    if schema_version == 3:
        environment = manifest.get("environment")
        required = {
            "uv": "0.12.3",
            "c_compiler": "zig",
            "c_compiler_version": "0.15.2",
            "c_runtime": "Zig 0.15.2 bundled libc",
            "target_contract": "native x86_64 hosted C17",
        }
        if not isinstance(environment, dict) or any(
            environment.get(key) != value for key, value in required.items()
        ):
            fail("schema 3 environment does not seal the G1 toolchain contract")
    elif schema_version == 4:
        environment = manifest.get("environment")
        required = {
            "uv": "0.12.3",
            "cpp_compiler": "zig-c++",
            "cpp_compiler_version": "0.15.2",
            "c_compiler": "zig-cc",
            "c_compiler_version": "0.15.2",
            "elf_reader": "pyelftools 0.32",
            "target_contract": "native x86_64 hosted C++20",
            "abi_targets": "thumb-freestanding-eabi,aarch64-freestanding-none",
        }
        if not isinstance(environment, dict) or any(
            environment.get(key) != value for key, value in required.items()
        ):
            fail("schema 4 environment does not seal the G2 C++ and ELF contract")
    if schema_version in {3, 4}:
        uv_version = subprocess.run(
            ["uv", "--version"],
            cwd=snapshot,
            check=False,
            capture_output=True,
            text=True,
        )
        if uv_version.returncode != 0 or not pinned_uv_version(uv_version.stdout.strip()):
            fail(f"uv version mismatch: {uv_version.stdout.strip()}")


def verify_output(
    result: subprocess.CompletedProcess[bytes],
    command: dict[str, Any],
    recorded_stdout: bytes,
) -> None:
    stdout_hash = command.get("stdout_sha256")
    stderr_hash = command.get("stderr_sha256")
    if not isinstance(stdout_hash, str) or not SHA256.fullmatch(stdout_hash):
        fail("stdout_sha256 is invalid")
    if not isinstance(stderr_hash, str) or not SHA256.fullmatch(stderr_hash):
        fail("stderr_sha256 is invalid")
    if result.returncode != command["expected_exit"]:
        fail(f"replay exit mismatch: expected {command['expected_exit']}, got {result.returncode}")
    stdout = canonical_output(result.stdout)
    stderr = canonical_output(result.stderr)
    if stdout != recorded_stdout or digest(stdout) != stdout_hash:
        fail("replay stdout does not match recorded evidence")
    if digest(stderr) != stderr_hash:
        fail("replay stderr does not match manifest")


def recorded_command_stdout(command: dict[str, Any], label: str) -> bytes:
    output = repository_path(command.get("stdout_path")).read_bytes()
    if digest(output) != command.get("stdout_sha256"):
        fail(f"recorded {label} stdout hash drifted")
    return output


def verify_repository_check(manifest: dict[str, Any], snapshot: Path) -> None:
    check = manifest.get("repository_check")
    if not isinstance(check, dict):
        fail("active manifest needs repository_check evidence")
    if check.get("argv") != ["bash", "scripts/check_repo.sh"]:
        fail("repository_check must invoke scripts/check_repo.sh")
    required_environment = {"SKIP_RUNNABLE_EVIDENCE": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    if check.get("environment") != required_environment:
        fail("repository_check environment must disable only recursive evidence replay and bytecode")
    stdout_path = repository_path(check.get("stdout_path"))
    stderr_path = repository_path(check.get("stderr_path"))
    expected_stdout = stdout_path.read_bytes()
    expected_stderr = stderr_path.read_bytes()
    environment = os.environ.copy()
    environment.update(required_environment)
    result = subprocess.run(
        repository_check_argv(os.name, environment),
        cwd=snapshot,
        env=environment,
        check=False,
        capture_output=True,
    )
    if check.get("expected_exit") != 0 or check.get("observed_exit") != 0:
        fail("repository_check manifest does not record a successful run")
    if result.returncode != 0:
        stdout = result.stdout.decode("utf-8", errors="replace")[-1200:]
        stderr = result.stderr.decode("utf-8", errors="replace")[-1200:]
        details = f"stdout tail={stdout!r}; stderr tail={stderr!r}"
        fail(f"repository_check failed with exit {result.returncode}; {details}")
    stdout = canonical_output(result.stdout)
    stderr = canonical_output(result.stderr)
    if stdout != expected_stdout or digest(stdout) != check.get("stdout_sha256"):
        fail("repository_check stdout does not match evidence")
    if stderr != expected_stderr or digest(stderr) != check.get("stderr_sha256"):
        fail("repository_check stderr does not match evidence")
