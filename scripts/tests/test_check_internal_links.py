from pathlib import Path

from scripts.check_internal_links import ignored_markdown


def test_generated_dependency_and_build_documents_are_ignored(tmp_path: Path) -> None:
    ignored = [
        tmp_path / "toolchain/.venv/Lib/site-packages/package/README.md",
        tmp_path / "frontend/node_modules/package/README.md",
        tmp_path / "build/report/README.md",
        tmp_path / "build-debug/report/README.md",
        tmp_path / "cmake-build-release/report/README.md",
    ]

    assert all(ignored_markdown(path, tmp_path) for path in ignored)


def test_repository_document_remains_in_scope(tmp_path: Path) -> None:
    assert not ignored_markdown(tmp_path / "docs/README.md", tmp_path)
