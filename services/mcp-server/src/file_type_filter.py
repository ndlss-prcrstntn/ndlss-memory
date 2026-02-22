from __future__ import annotations

from pathlib import Path


def parse_supported_types(types_csv: str) -> set[str]:
    items = [item.strip().lower() for item in types_csv.split(",") if item.strip()]
    return {item if item.startswith(".") else f".{item}" for item in items}


def is_supported_file(path: Path, supported_types: set[str]) -> bool:
    return path.suffix.lower() in supported_types

