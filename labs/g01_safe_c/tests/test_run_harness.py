from __future__ import annotations

from pathlib import Path

import pytest

from labs.g01_safe_c import run_harness


def test_select_sprints_returns_one_when_lab_id_is_specific() -> None:
    runner = run_harness
    selected = runner.select_sprints("G1.3")
    assert tuple(sprint.lab_id for sprint in selected) == ("G1.3",)


def test_select_sprints_returns_all_when_lab_id_is_chapter() -> None:
    runner = run_harness
    selected = runner.select_sprints("G1.ALL")
    assert tuple(sprint.lab_id for sprint in selected) == (
        "G1.1",
        "G1.2",
        "G1.3",
        "G1.4",
        "G1.5",
    )


def test_select_sprints_rejects_unknown_lab_id() -> None:
    runner = run_harness
    with pytest.raises(runner.HarnessInputError):
        _ = runner.select_sprints("G1.99")


def test_parse_selection_marks_retest_case_set() -> None:
    runner = run_harness
    selected, retest = runner.parse_selection("G1.4.RETEST")
    assert tuple(sprint.lab_id for sprint in selected) == ("G1.4",)
    assert retest


def test_parse_selection_accepts_chapter_retest_alias() -> None:
    runner = run_harness
    selected, retest = runner.parse_selection("G1.RETEST")
    assert len(selected) == 5
    assert retest


def test_resolve_source_root_rejects_path_outside_repository(tmp_path: Path) -> None:
    runner = run_harness
    with pytest.raises(runner.HarnessInputError):
        _ = runner.resolve_source_root(tmp_path)


def test_compiler_prefix_adds_cc_when_compiler_is_zig() -> None:
    runner = run_harness
    compiler = Path("C:/tools/zig.exe")
    prefix = runner.compiler_prefix(compiler)
    assert prefix == (str(compiler), "cc")
