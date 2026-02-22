from __future__ import annotations

from pathlib import Path


def path_depth(root: Path, path: Path) -> int:
    relative = path.relative_to(root)
    return max(len(relative.parts) - 1, 0)


def walk_files(workspace_path: str) -> list[Path]:
    root = Path(workspace_path)
    if not root.exists() or not root.is_dir():
        return []
    files = [path for path in root.rglob("*") if path.is_file()]
    files.sort(key=lambda path: str(path.relative_to(root)).replace("\\", "/"))
    return files

