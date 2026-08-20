from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Protocol, cast

import pytest

RUNNER_PATH = Path(__file__).parents[1] / "run_harness.py"


class SprintView(Protocol):
    lab_id: str


class RunnerModule(Protocol):
    HarnessInputError: type[Exception]

    def select_sprints(self, lab_id: str) -> tuple[SprintView, ...]: ...

    def resolve_source_root(self, candidate: Path) -> Path: ...

    def compiler_prefix(self, compiler: Path) -> tuple[str, ...]: ...


def load_runner() -> RunnerModule:
    spec = importlib.util.spec_from_file_location("g01_run_harness", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return cast(RunnerModule, cast(object, module))


def test_select_sprints_returns_one_when_lab_id_is_specific() -> None:
    runner = load_runner()
    selected = runner.select_sprints("G1.3")
    assert tuple(sprint.lab_id for sprint in selected) == ("G1.3",)


def test_select_sprints_returns_all_when_lab_id_is_chapter() -> None:
    runner = load_runner()
    selected = runner.select_sprints("G1.ALL")
    assert tuple(sprint.lab_id for sprint in selected) == (
        "G1.1",
        "G1.2",
        "G1.3",
        "G1.4",
        "G1.5",
    )


def test_select_sprints_rejects_unknown_lab_id() -> None:
    runner = load_runner()
    with pytest.raises(runner.HarnessInputError):
        _ = runner.select_sprints("G1.99")


def test_resolve_source_root_rejects_path_outside_repository(tmp_path: Path) -> None:
    runner = load_runner()
    with pytest.raises(runner.HarnessInputError):
        _ = runner.resolve_source_root(tmp_path)


def test_compiler_prefix_adds_cc_when_compiler_is_zig() -> None:
    runner = load_runner()
    prefix = runner.compiler_prefix(Path("C:/tools/zig.exe"))
    assert prefix == ("C:\\tools\\zig.exe", "cc")
