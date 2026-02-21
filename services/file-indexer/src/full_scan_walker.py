from __future__ import annotations

from pathlib import Path


def walk_files(workspace_path: str) -> list[Path]:
    root = Path(workspace_path)
    if not root.exists() or not root.is_dir():
        return []
    return [path for path in root.rglob("*") if path.is_file()]

