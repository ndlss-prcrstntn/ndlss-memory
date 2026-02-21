from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ChunkSyncResult:
    chunk_id: str
    operation: str
    reason_code: str
    message: str | None = None
    processed_at: str = _now_iso()

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunkId": self.chunk_id,
            "operation": self.operation,
            "reasonCode": self.reason_code,
            "message": self.message,
            "processedAt": self.processed_at,
        }

