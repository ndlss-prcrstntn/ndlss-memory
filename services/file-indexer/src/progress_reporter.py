from __future__ import annotations

import json
import time
from datetime import datetime, timezone


class ProgressReporter:
    def __init__(self, interval_seconds: int = 15) -> None:
        self.interval_seconds = max(1, interval_seconds)
        self._last_emit = 0.0

    def emit(self, payload: dict) -> None:
        now = time.time()
        if (now - self._last_emit) < self.interval_seconds:
            return
        self._last_emit = now
        line = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "full_scan_progress",
            **payload,
        }
        print(json.dumps(line, ensure_ascii=False), flush=True)

    def force_emit(self, payload: dict) -> None:
        self._last_emit = 0.0
        self.emit(payload)

