from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

ChangeType = Literal["added", "modified", "deleted", "renamed"]
DecisionType = Literal["index", "delete", "skip"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class GitChangeSet:
    change_id: str
    change_type: ChangeType
    path: str
    old_path: str | None = None
    raw_status: str | None = None
    detected_at: str = field(default_factory=_now_iso)


@dataclass(frozen=True)
class DeltaCandidateFile:
    run_id: str
    path: str
    source_change_type: ChangeType
    decision: DecisionType
    decision_reason_code: str
    filtered_out: bool = False
    old_path: str | None = None
