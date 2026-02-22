from __future__ import annotations

from dataclasses import replace
from threading import Lock
from typing import Iterable

from watch_mode_models import IncrementalIndexResult, WatchEvent, WatchRunStateSnapshot, now_iso


class WatchModeState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._snapshot = WatchRunStateSnapshot(state="stopped")
        self._queue: list[WatchEvent] = []
        self._last_summary: dict | None = None

    def start(self, workspace_path: str) -> WatchRunStateSnapshot:
        with self._lock:
            self._snapshot = WatchRunStateSnapshot(
                state="starting",
                workspace_path=workspace_path,
            )
            self._queue = []
            self._last_summary = None
            return replace(self._snapshot)

    def stop(self) -> WatchRunStateSnapshot:
        with self._lock:
            self._snapshot.state = "stopped"
            self._snapshot.last_heartbeat_at = now_iso()
            return replace(self._snapshot)

    def set_state(self, state: str) -> WatchRunStateSnapshot:
        with self._lock:
            self._snapshot.state = state  # type: ignore[assignment]
            self._snapshot.last_heartbeat_at = now_iso()
            return replace(self._snapshot)

    def heartbeat(self) -> WatchRunStateSnapshot:
        with self._lock:
            self._snapshot.last_heartbeat_at = now_iso()
            return replace(self._snapshot)

    def set_backoff(self, seconds: float) -> None:
        with self._lock:
            self._snapshot.backoff_seconds = max(0.0, float(seconds))
            self._snapshot.last_heartbeat_at = now_iso()

    def record_retry(self, *, error_code: str, error_message: str, recoverable: bool) -> WatchRunStateSnapshot:
        with self._lock:
            self._snapshot.retry_count += 1
            self._snapshot.last_error_code = error_code
            self._snapshot.last_error_message = error_message
            self._snapshot.state = "recovering" if recoverable else "failed"
            self._snapshot.last_heartbeat_at = now_iso()
            return replace(self._snapshot)

    def clear_error(self) -> None:
        with self._lock:
            self._snapshot.last_error_code = None
            self._snapshot.last_error_message = None
            self._snapshot.backoff_seconds = 0.0

    def enqueue_events(self, events: Iterable[WatchEvent]) -> int:
        with self._lock:
            added = 0
            for event in events:
                event.status = "queued"
                self._queue.append(event)
                added += 1
            if added:
                self._snapshot.queue_depth = len(self._queue)
                self._snapshot.last_event_at = now_iso()
            return added

    def dequeue_events(self, max_items: int) -> list[WatchEvent]:
        with self._lock:
            if max_items <= 0 or not self._queue:
                return []
            slice_count = min(max_items, len(self._queue))
            batch = self._queue[:slice_count]
            self._queue = self._queue[slice_count:]
            self._snapshot.queue_depth = len(self._queue)
            return batch

    def mark_processed(self, processed: int, failed: int) -> None:
        with self._lock:
            self._snapshot.processed_events += max(0, processed)
            self._snapshot.failed_events += max(0, failed)
            self._snapshot.last_event_at = now_iso()

    def set_last_summary(self, summary: IncrementalIndexResult | dict | None) -> None:
        with self._lock:
            if summary is None:
                self._last_summary = None
                return
            if isinstance(summary, IncrementalIndexResult):
                self._last_summary = summary.to_payload()
            else:
                self._last_summary = dict(summary)

    def get_last_summary(self) -> dict | None:
        with self._lock:
            return None if self._last_summary is None else dict(self._last_summary)

    def get_status(self) -> dict:
        with self._lock:
            return self._snapshot.to_payload()


STATE = WatchModeState()
