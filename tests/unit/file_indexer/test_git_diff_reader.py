from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from delta_after_commit.git_diff_reader import read_git_change_set


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _init_repo(repo: Path) -> None:
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "tests@example.local"], repo)
    _run(["git", "config", "user.name", "Tests"], repo)


def test_read_git_change_set_added_and_modified(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)

    (repo / "docs").mkdir()
    (repo / "docs" / "a.md").write_text("hello\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-m", "base"], repo)

    (repo / "docs" / "a.md").write_text("hello world\n", encoding="utf-8")
    (repo / "docs" / "b.md").write_text("new\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-m", "update"], repo)

    changes = read_git_change_set(
        workspace_path=str(repo),
        base_ref="HEAD~1",
        target_ref="HEAD",
        include_renames=True,
    )

    types = {item.change_type for item in changes}
    paths = {item.path for item in changes}
    assert "added" in types
    assert "modified" in types
    assert "docs/a.md" in paths
    assert "docs/b.md" in paths


def test_read_git_change_set_rename(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)

    (repo / "docs").mkdir()
    (repo / "docs" / "old.md").write_text("hello\n", encoding="utf-8")
    _run(["git", "add", "."], repo)
    _run(["git", "commit", "-m", "base"], repo)

    _run(["git", "mv", "docs/old.md", "docs/new.md"], repo)
    _run(["git", "commit", "-m", "rename"], repo)

    changes = read_git_change_set(
        workspace_path=str(repo),
        base_ref="HEAD~1",
        target_ref="HEAD",
        include_renames=True,
    )

    renamed = [item for item in changes if item.change_type == "renamed"]
    assert renamed
    assert renamed[0].old_path == "docs/old.md"
    assert renamed[0].path == "docs/new.md"
