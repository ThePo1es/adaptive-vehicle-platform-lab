from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from labs.g02_embedded_cpp import run_harness
from labs.g02_embedded_cpp.harness_toolchain import compiler_prefix
from labs.g02_embedded_cpp.submission import (
    HarnessInputError,
    require_trusted_submission,
    resolve_submission_source,
)


def test_select_sprints_returns_requested_lab() -> None:
    selected = run_harness.select_sprints("G2.3")
    assert tuple(sprint.lab_id for sprint in selected) == ("G2.3",)


def test_select_sprints_returns_whole_chapter() -> None:
    selected = run_harness.select_sprints("G2.ALL")
    assert tuple(sprint.lab_id for sprint in selected) == (
        "G2.1",
        "G2.2",
        "G2.3",
        "G2.4",
    )


def test_parse_selection_marks_retest_input_set() -> None:
    selected, retest = run_harness.parse_selection("G2.RETEST")
    assert len(selected) == 4
    assert retest


def test_select_sprints_rejects_unknown_lab() -> None:
    with pytest.raises(HarnessInputError):
        _ = run_harness.select_sprints("G2.99")


def test_submission_root_must_remain_inside_repository(tmp_path: Path) -> None:
    with pytest.raises(HarnessInputError):
        _ = run_harness.resolve_source_root(tmp_path)


def test_submission_requires_an_explicit_local_trust_decision() -> None:
    with pytest.raises(HarnessInputError, match="G02_TRUSTED_LOCAL_EXECUTION"):
        _ = require_trusted_submission(
            "study/g02/src",
            None,
            run_harness.REPO_ROOT,
            run_harness.REFERENCE_ROOT,
        )


def test_submission_source_rejects_symlink_escape(tmp_path: Path) -> None:
    source_root = tmp_path / "submission"
    source_root.mkdir()
    outside = tmp_path / "outside.cpp"
    _ = outside.write_text("int outside;\n", encoding="utf-8")
    link = source_root / "runtime.cpp"
    try:
        _ = link.symlink_to(outside)
    except OSError:
        pytest.skip("this Windows account cannot create symbolic links")
    with pytest.raises(HarnessInputError, match="must be a regular file"):
        _ = resolve_submission_source(source_root, "runtime.cpp")


def test_cpp_driver_uses_zig_cxx_subcommand() -> None:
    compiler = Path("C:/tools/zig.exe")
    assert compiler_prefix(compiler) == (str(compiler), "c++")


def test_submission_compile_has_a_deadline(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source = tmp_path / "lifetime.cpp"
    _ = source.write_text("int main() { return 0; }\n", encoding="utf-8")
    observed_timeout: list[float | None] = []

    def timeout(*_args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        value = kwargs.get("timeout")
        timeout_seconds = float(value) if isinstance(value, (int, float)) else 0.0
        observed_timeout.append(timeout_seconds)
        raise subprocess.TimeoutExpired("zig c++", timeout_seconds)

    monkeypatch.setattr(subprocess, "run", timeout)
    request = run_harness.CompileRequest(
        Path("C:/tools/zig.exe"),
        run_harness.SPRINTS[0],
        tmp_path,
        tmp_path / "test.exe",
        0,
        2,
        False,
    )

    with pytest.raises(run_harness.HarnessExecutionError, match="compile exceeded 120 seconds"):
        run_harness.compile_binary(request)

    assert observed_timeout == [120]
