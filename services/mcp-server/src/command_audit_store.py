from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Lock
from uuid import uuid4

from command_execution_models import CommandAuditRecord


def _parse_iso(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


class CommandAuditStore:
    def __init__(self, *, audit_log_path: str, retention_days: int) -> None:
        self._path = Path(audit_log_path)
        self._retention_days = max(1, retention_days)
        self._lock = Lock()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.touch()

    def append(self, record: CommandAuditRecord) -> None:
        with self._lock:
            entry = {"auditId": uuid4().hex, **record.to_payload()}
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
            self._prune_locked()

    def list_records(self, *, limit: int, status: str | None = None) -> list[dict]:
        with self._lock:
            self._prune_locked()
            records: list[dict] = []
            for line in self._path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if status and item.get("status") != status:
                    continue
                records.append(item)
            records.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
            return records[:limit]

    def _prune_locked(self) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=self._retention_days)
        kept: list[str] = []
        for line in self._path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                ts = item.get("timestamp")
                if not ts:
                    continue
                if _parse_iso(str(ts)) >= cutoff:
                    kept.append(json.dumps(item, ensure_ascii=False))
            except (json.JSONDecodeError, ValueError):
                continue
        payload = "\n".join(kept)
        if payload:
            payload += "\n"
        self._path.write_text(payload, encoding="utf-8")

