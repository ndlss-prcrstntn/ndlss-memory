from __future__ import annotations

import fnmatch
from pathlib import Path


def parse_exclude_patterns(patterns_csv: str) -> list[str]:
    return [item.strip() for item in patterns_csv.split(",") if item.strip()]


def is_excluded_path(path: Path, patterns: list[str]) -> bool:
    path_str = str(path).replace("\\", "/")
    for pattern in patterns:
        normalized = pattern.strip()
        if not normalized:
            continue
        if fnmatch.fnmatch(path_str, normalized) or f"/{normalized}/" in f"/{path_str}/":
            return True
    return False

