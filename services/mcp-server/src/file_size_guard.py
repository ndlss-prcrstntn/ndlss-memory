from __future__ import annotations

from pathlib import Path


def is_file_too_large(path: Path, max_file_size_bytes: int) -> tuple[bool, int]:
    try:
        size = path.stat().st_size
    except OSError:
        return False, -1
    return size > max_file_size_bytes, size

