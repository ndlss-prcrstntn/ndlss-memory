from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PathTransition:
    run_id: str
    old_path: str
    new_path: str
    transition_status: str
