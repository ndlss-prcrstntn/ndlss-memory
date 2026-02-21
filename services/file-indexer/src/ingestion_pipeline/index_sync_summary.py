from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class IndexSyncSummary:
    run_id: str
    status: str
    total_files: int
    updated_chunks: int
    skipped_chunks: int
    deleted_chunks: int
    failed_chunks: int
    started_at: str
    finished_at: str
    reason_breakdown: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "status": self.status,
            "totalFiles": self.total_files,
            "updatedChunks": self.updated_chunks,
            "skippedChunks": self.skipped_chunks,
            "deletedChunks": self.deleted_chunks,
            "failedChunks": self.failed_chunks,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "reasonBreakdown": self.reason_breakdown,
        }


class IndexSyncSummaryAccumulator:
    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.started_at = _now_iso()
        self.total_files = 0
        self.updated_chunks = 0
        self.skipped_chunks = 0
        self.deleted_chunks = 0
        self.failed_chunks = 0
        self._reasons: dict[str, int] = {}

    def on_file(self) -> None:
        self.total_files += 1

    def on_updated(self, reason_code: str) -> None:
        self.updated_chunks += 1
        self._reasons[reason_code] = self._reasons.get(reason_code, 0) + 1

    def on_skipped(self, reason_code: str) -> None:
        self.skipped_chunks += 1
        self._reasons[reason_code] = self._reasons.get(reason_code, 0) + 1

    def on_deleted(self, reason_code: str) -> None:
        self.deleted_chunks += 1
        self._reasons[reason_code] = self._reasons.get(reason_code, 0) + 1

    def on_failed(self, reason_code: str) -> None:
        self.failed_chunks += 1
        self._reasons[reason_code] = self._reasons.get(reason_code, 0) + 1

    def finalize(self) -> IndexSyncSummary:
        if self.failed_chunks == 0:
            status = "completed"
        elif self.updated_chunks + self.skipped_chunks + self.deleted_chunks == 0:
            status = "failed"
        else:
            status = "partial"
        reason_breakdown = [{"code": code, "count": count} for code, count in sorted(self._reasons.items())]
        return IndexSyncSummary(
            run_id=self.run_id,
            status=status,
            total_files=self.total_files,
            updated_chunks=self.updated_chunks,
            skipped_chunks=self.skipped_chunks,
            deleted_chunks=self.deleted_chunks,
            failed_chunks=self.failed_chunks,
            started_at=self.started_at,
            finished_at=_now_iso(),
            reason_breakdown=reason_breakdown,
        )

