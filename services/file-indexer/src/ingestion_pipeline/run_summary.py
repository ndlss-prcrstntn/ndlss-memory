from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class IngestionRunSummary:
    run_id: str
    status: str
    total_files: int
    total_chunks: int
    embedded_chunks: int
    failed_chunks: int
    retry_count: int
    started_at: str
    finished_at: str
    metadata_coverage: dict[str, float]
    applied_limits: dict[str, int | None]
    skip_breakdown: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "status": self.status,
            "totalFiles": self.total_files,
            "totalChunks": self.total_chunks,
            "embeddedChunks": self.embedded_chunks,
            "failedChunks": self.failed_chunks,
            "retryCount": self.retry_count,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "metadataCoverage": self.metadata_coverage,
            "appliedLimits": self.applied_limits,
            "skipBreakdown": self.skip_breakdown,
        }


class SummaryAccumulator:
    REQUIRED_METADATA_FIELDS = ("path", "fileName", "fileType", "contentHash", "timestamp")

    def __init__(self, run_id: str, *, max_traversal_depth: int | None = None, max_files_per_run: int | None = None) -> None:
        self.run_id = run_id
        self.started_at = _now()
        self.total_files = 0
        self.total_chunks = 0
        self.embedded_chunks = 0
        self.failed_chunks = 0
        self.retry_count = 0
        self._metadata_totals = {field: 0 for field in self.REQUIRED_METADATA_FIELDS}
        self.max_traversal_depth = max_traversal_depth
        self.max_files_per_run = max_files_per_run
        self._skip_breakdown: dict[str, int] = {}

    def on_file(self) -> None:
        self.total_files += 1

    def on_chunk(self) -> None:
        self.total_chunks += 1

    def on_embedding_success(self, metadata: dict[str, Any]) -> None:
        self.embedded_chunks += 1
        for field in self.REQUIRED_METADATA_FIELDS:
            value = metadata.get(field)
            if value is not None and str(value).strip() != "":
                self._metadata_totals[field] += 1

    def on_embedding_failure(self) -> None:
        self.failed_chunks += 1

    def on_retry(self, retries_used: int) -> None:
        if retries_used > 0:
            self.retry_count += retries_used

    def on_skip(self, code: str) -> None:
        self._skip_breakdown[code] = self._skip_breakdown.get(code, 0) + 1

    def finalize(self) -> IngestionRunSummary:
        finished_at = _now()
        if self.total_chunks == 0 or self.failed_chunks == 0:
            status = "completed"
        elif self.embedded_chunks == 0:
            status = "failed"
        else:
            status = "partial"

        denominator = self.embedded_chunks if self.embedded_chunks > 0 else 1
        coverage = {field: round(self._metadata_totals[field] / denominator, 6) for field in self.REQUIRED_METADATA_FIELDS}
        return IngestionRunSummary(
            run_id=self.run_id,
            status=status,
            total_files=self.total_files,
            total_chunks=self.total_chunks,
            embedded_chunks=self.embedded_chunks,
            failed_chunks=self.failed_chunks,
            retry_count=self.retry_count,
            started_at=self.started_at.isoformat(),
            finished_at=finished_at.isoformat(),
            metadata_coverage=coverage,
            applied_limits={
                "maxTraversalDepth": self.max_traversal_depth,
                "maxFilesPerRun": self.max_files_per_run,
            },
            skip_breakdown=[{"code": code, "count": count} for code, count in sorted(self._skip_breakdown.items())],
        )

