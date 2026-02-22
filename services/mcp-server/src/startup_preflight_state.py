from __future__ import annotations

from threading import Lock
from typing import Any


class StartupPreflightState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._readiness_summary: dict[str, Any] | None = None
        self._failure_report: dict[str, Any] | None = None

    def mark_ready(self, summary: dict[str, Any]) -> None:
        with self._lock:
            self._readiness_summary = summary
            self._failure_report = None

    def mark_failed(self, report: dict[str, Any]) -> None:
        with self._lock:
            self._failure_report = report
            self._readiness_summary = None

    def get_readiness_summary(self) -> dict[str, Any] | None:
        with self._lock:
            if self._readiness_summary is None:
                return None
            return dict(self._readiness_summary)

    def get_failure_report(self) -> dict[str, Any] | None:
        with self._lock:
            if self._failure_report is None:
                return None
            return dict(self._failure_report)

    def reset(self) -> None:
        with self._lock:
            self._readiness_summary = None
            self._failure_report = None


STATE = StartupPreflightState()

