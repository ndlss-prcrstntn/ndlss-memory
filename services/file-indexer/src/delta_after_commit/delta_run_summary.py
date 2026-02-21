from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DeltaRunSummary:
    run_id: str
    status: str
    requested_mode: str
    effective_mode: str
    base_ref: str
    target_ref: str
    added_files: int
    modified_files: int
    deleted_files: int
    renamed_files: int
    indexed_files: int
    removed_records: int
    skipped_files: int
    failed_files: int
    started_at: str
    finished_at: str
    reason_breakdown: list[dict[str, Any]]
    fallback_reason_code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "runId": self.run_id,
            "status": self.status,
            "requestedMode": self.requested_mode,
            "effectiveMode": self.effective_mode,
            "baseRef": self.base_ref,
            "targetRef": self.target_ref,
            "addedFiles": self.added_files,
            "modifiedFiles": self.modified_files,
            "deletedFiles": self.deleted_files,
            "renamedFiles": self.renamed_files,
            "indexedFiles": self.indexed_files,
            "removedRecords": self.removed_records,
            "skippedFiles": self.skipped_files,
            "failedFiles": self.failed_files,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "reasonBreakdown": self.reason_breakdown,
        }
        if self.fallback_reason_code:
            payload["fallbackReasonCode"] = self.fallback_reason_code
        return payload


@dataclass
class DeltaRunSummaryAccumulator:
    run_id: str
    base_ref: str
    target_ref: str
    requested_mode: str = "delta-after-commit"
    effective_mode: str = "delta-after-commit"
    fallback_reason_code: str | None = None
    started_at: str = field(default_factory=_now_iso)
    added_files: int = 0
    modified_files: int = 0
    deleted_files: int = 0
    renamed_files: int = 0
    indexed_files: int = 0
    removed_records: int = 0
    skipped_files: int = 0
    failed_files: int = 0
    reason_breakdown: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def on_change(self, change_type: str) -> None:
        if change_type == "added":
            self.added_files += 1
        elif change_type == "modified":
            self.modified_files += 1
        elif change_type == "deleted":
            self.deleted_files += 1
        elif change_type == "renamed":
            self.renamed_files += 1

    def on_indexed(self, code: str = "INDEXED") -> None:
        self.indexed_files += 1
        self.reason_breakdown[code] += 1

    def on_removed(self, code: str = "DELETED_RECORD") -> None:
        self.removed_records += 1
        self.reason_breakdown[code] += 1

    def on_skipped(self, code: str) -> None:
        self.skipped_files += 1
        self.reason_breakdown[code] += 1

    def on_failed(self, code: str) -> None:
        self.failed_files += 1
        self.reason_breakdown[code] += 1

    def set_fallback(self, reason_code: str) -> None:
        self.effective_mode = "full-scan-fallback"
        self.fallback_reason_code = reason_code
        self.reason_breakdown[reason_code] += 1

    def absorb_fallback_sync(self, *, updated_chunks: int, skipped_chunks: int, deleted_chunks: int, failed_chunks: int) -> None:
        self.indexed_files += int(updated_chunks)
        self.skipped_files += int(skipped_chunks)
        self.removed_records += int(deleted_chunks)
        self.failed_files += int(failed_chunks)
        self.reason_breakdown["FULL_SCAN_FALLBACK_APPLIED"] += 1

    def finalize(self) -> DeltaRunSummary:
        if self.failed_files == 0:
            status = "completed"
        elif self.indexed_files > 0 or self.removed_records > 0:
            status = "partial"
        else:
            status = "failed"
        return DeltaRunSummary(
            run_id=self.run_id,
            status=status,
            requested_mode=self.requested_mode,
            effective_mode=self.effective_mode,
            base_ref=self.base_ref,
            target_ref=self.target_ref,
            added_files=self.added_files,
            modified_files=self.modified_files,
            deleted_files=self.deleted_files,
            renamed_files=self.renamed_files,
            indexed_files=self.indexed_files,
            removed_records=self.removed_records,
            skipped_files=self.skipped_files,
            failed_files=self.failed_files,
            started_at=self.started_at,
            finished_at=_now_iso(),
            reason_breakdown=[{"code": code, "count": count} for code, count in sorted(self.reason_breakdown.items())],
            fallback_reason_code=self.fallback_reason_code,
        )
