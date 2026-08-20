from __future__ import annotations

from pathlib import Path

import pytest

from labs.g02_embedded_cpp import run_harness
from labs.g02_embedded_cpp.harness_toolchain import compiler_prefix


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
    with pytest.raises(run_harness.HarnessInputError):
        _ = run_harness.select_sprints("G2.99")


def test_submission_root_must_remain_inside_repository(tmp_path: Path) -> None:
    with pytest.raises(run_harness.HarnessInputError):
        _ = run_harness.resolve_source_root(tmp_path)


def test_cpp_driver_uses_zig_cxx_subcommand() -> None:
    compiler = Path("C:/tools/zig.exe")
    assert compiler_prefix(compiler) == (str(compiler), "c++")
