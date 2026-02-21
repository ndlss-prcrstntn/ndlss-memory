from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from ingestion_pipeline.content_hash import build_text_hash


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class FileFingerprint:
    file_path: str
    content_hash: str
    previous_hash: str | None
    status: str
    detected_at: str

    @classmethod
    def from_content(cls, *, file_path: str, content: str, previous_hash: str | None) -> "FileFingerprint":
        current_hash = build_text_hash(content)
        if previous_hash is None:
            status = "new"
        elif previous_hash == current_hash:
            status = "unchanged"
        else:
            status = "changed"
        return cls(
            file_path=file_path,
            content_hash=current_hash,
            previous_hash=previous_hash,
            status=status,
            detected_at=_now_iso(),
        )

    @classmethod
    def deleted(cls, *, file_path: str, previous_hash: str | None) -> "FileFingerprint":
        return cls(
            file_path=file_path,
            content_hash="",
            previous_hash=previous_hash,
            status="deleted",
            detected_at=_now_iso(),
        )

