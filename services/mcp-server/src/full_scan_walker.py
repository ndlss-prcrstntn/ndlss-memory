from __future__ import annotations

import os
from pathlib import Path

from path_exclude_filter import is_excluded_path


def path_depth(root: Path, path: Path) -> int:
    relative = path.relative_to(root)
    return max(len(relative.parts) - 1, 0)


def walk_files_pruned(workspace_path: str, *, exclude_patterns: list[str] | None = None) -> list[Path]:
    root = Path(workspace_path)
    if not root.exists() or not root.is_dir():
        return []

    patterns = exclude_patterns or []
    files: list[Path] = []
    for current_root, dirnames, filenames in os.walk(root, topdown=True):
        current_path = Path(current_root)
        rel_dir = current_path.relative_to(root)
        dirnames[:] = [
            dirname
            for dirname in sorted(dirnames)
            if not is_excluded_path(rel_dir / dirname, patterns)
        ]
        for filename in sorted(filenames):
            files.append(current_path / filename)

    files.sort(key=lambda path: str(path.relative_to(root)).replace("\\", "/"))
    return files


def walk_files(workspace_path: str) -> list[Path]:
    root = Path(workspace_path)
    if not root.exists() or not root.is_dir():
        return []
    files = [path for path in root.rglob("*") if path.is_file()]
    files.sort(key=lambda path: str(path.relative_to(root)).replace("\\", "/"))
    return files

