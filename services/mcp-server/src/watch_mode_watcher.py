from __future__ import annotations

import fnmatch
import random
import time
from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Callable

from watch_mode_models import WatchEvent

_FileSnapshot = tuple[int, int]


def _split_csv(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _is_excluded(path: Path, patterns: list[str]) -> bool:
    normalized = str(path).replace("\\", "/")
    for pattern in patterns:
        current = pattern.strip()
        if not current:
            continue
        if fnmatch.fnmatch(normalized, current):
            return True
        if f"/{current}/" in f"/{normalized}/":
            return True
    return False


@dataclass
class WatchRetryPolicy:
    max_attempts: int = 5
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    jitter_ratio: float = 0.2

    def backoff_seconds(self, attempt: int) -> float:
        attempt = max(1, int(attempt))
        raw = min(self.max_delay_seconds, self.base_delay_seconds * (2 ** (attempt - 1)))
        jitter_bound = raw * self.jitter_ratio
        jitter = random.uniform(-jitter_bound, jitter_bound)
        return max(0.0, raw + jitter)


class PollingWorkspaceWatcher:
    def __init__(
        self,
        *,
        workspace_path: str,
        poll_interval_seconds: int = 5,
        max_events_per_cycle: int = 200,
        file_types_csv: str = ".md,.txt,.json,.yml,.yaml",
        exclude_patterns_csv: str = ".git,node_modules,dist,build",
        retry_policy: WatchRetryPolicy | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_path)
        self.poll_interval_seconds = max(1, int(poll_interval_seconds))
        self.max_events_per_cycle = max(1, int(max_events_per_cycle))
        self.supported_types = {value.lower() for value in _split_csv(file_types_csv)}
        self.exclude_patterns = _split_csv(exclude_patterns_csv)
        self.retry_policy = retry_policy or WatchRetryPolicy()
        self._previous_snapshot: dict[str, _FileSnapshot] = {}

    def initialize(self) -> None:
        self._previous_snapshot = self._scan_snapshot()

    def poll_once(self) -> list[WatchEvent]:
        current = self._scan_snapshot()
        events = self._diff_snapshots(self._previous_snapshot, current)
        self._previous_snapshot = current
        return events[: self.max_events_per_cycle]

    def reconcile(self, indexed_files: set[str]) -> list[WatchEvent]:
        current = self._scan_snapshot()
        current_files = set(current.keys())
        events: list[WatchEvent] = []
        for missing in sorted(indexed_files - current_files):
            events.append(WatchEvent(event_type="deleted", path=missing))
        for unknown in sorted(current_files - indexed_files):
            events.append(WatchEvent(event_type="updated", path=unknown))
        self._previous_snapshot = current
        return events[: self.max_events_per_cycle]

    def watch_loop(
        self,
        *,
        stop_event: Event,
        coalesce_window_seconds: int,
        reconcile_interval_seconds: int,
        on_events: Callable[[list[WatchEvent]], None],
        on_reconcile: Callable[[], list[WatchEvent]] | None = None,
        on_heartbeat: Callable[[], None] | None = None,
        on_retry: Callable[[Exception, int, float, bool], None] | None = None,
    ) -> None:
        buffer: list[WatchEvent] = []
        started = time.monotonic()
        last_flush = started
        last_reconcile = started
        consecutive_failures = 0
        initialized = False

        while not stop_event.is_set():
            if on_heartbeat:
                on_heartbeat()

            try:
                if not initialized:
                    self.initialize()
                    initialized = True
                events = self.poll_once()
                consecutive_failures = 0
                if events:
                    buffer.extend(events)

                now = time.monotonic()
                should_flush = bool(buffer) and (
                    (now - last_flush) >= max(1, int(coalesce_window_seconds))
                    or len(buffer) >= self.max_events_per_cycle
                )
                if should_flush:
                    on_events(buffer[: self.max_events_per_cycle])
                    buffer = buffer[self.max_events_per_cycle :]
                    last_flush = now

                if on_reconcile and (now - last_reconcile) >= max(1, int(reconcile_interval_seconds)):
                    reconcile_events = on_reconcile()
                    if reconcile_events:
                        on_events(reconcile_events[: self.max_events_per_cycle])
                    last_reconcile = now

                stop_event.wait(self.poll_interval_seconds)
            except Exception as exc:  # noqa: BLE001
                consecutive_failures += 1
                delay = self.retry_policy.backoff_seconds(consecutive_failures)
                exhausted = consecutive_failures >= self.retry_policy.max_attempts
                if on_retry:
                    on_retry(exc, consecutive_failures, delay, exhausted)
                if exhausted:
                    raise
                stop_event.wait(delay)

        if buffer:
            on_events(buffer[: self.max_events_per_cycle])

    def _scan_snapshot(self) -> dict[str, _FileSnapshot]:
        if not self.workspace_root.exists() or not self.workspace_root.is_dir():
            raise RuntimeError(f"Workspace path '{self.workspace_root}' is not accessible")

        snapshot: dict[str, _FileSnapshot] = {}
        for file_path in self.workspace_root.rglob("*"):
            if not file_path.is_file():
                continue
            relative = file_path.relative_to(self.workspace_root)
            if _is_excluded(relative, self.exclude_patterns):
                continue
            if self.supported_types and file_path.suffix.lower() not in self.supported_types:
                continue
            stat = file_path.stat()
            key = str(relative).replace("\\", "/")
            snapshot[key] = (int(stat.st_size), int(stat.st_mtime_ns))
        return snapshot

    @staticmethod
    def _diff_snapshots(previous: dict[str, _FileSnapshot], current: dict[str, _FileSnapshot]) -> list[WatchEvent]:
        events: list[WatchEvent] = []
        previous_paths = set(previous.keys())
        current_paths = set(current.keys())

        for path in sorted(current_paths - previous_paths):
            events.append(WatchEvent(event_type="created", path=path))
        for path in sorted(previous_paths - current_paths):
            events.append(WatchEvent(event_type="deleted", path=path))
        for path in sorted(previous_paths & current_paths):
            if previous[path] != current[path]:
                events.append(WatchEvent(event_type="updated", path=path))

        return events
