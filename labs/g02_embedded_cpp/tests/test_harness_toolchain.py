from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from labs.g02_embedded_cpp.harness_toolchain import verify_hosted_cpp20


def test_hosted_cpp_compile_uses_the_compile_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_timeouts: list[float | None] = []

    def succeed(
        command: list[str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        value = kwargs.get("timeout")
        observed_timeouts.append(float(value) if isinstance(value, (int, float)) else None)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    verify_hosted_cpp20(Path("C:/tools/zig.exe"))

    assert observed_timeouts == [120.0, 10.0]
