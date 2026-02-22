from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class McpSession:
    session_id: str
    transport: str
    created_at: str = field(default_factory=_now_iso)
    last_event_at: str = field(default_factory=_now_iso)
    initialized: bool = False
    client_info: dict[str, Any] | None = None
    queued_responses: list[dict[str, Any]] = field(default_factory=list)


class McpSessionStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._sessions: dict[str, McpSession] = {}

    def create_session(self, *, transport: str, session_id: str | None = None) -> McpSession:
        with self._lock:
            sid = session_id or uuid4().hex
            session = McpSession(session_id=sid, transport=transport)
            self._sessions[sid] = session
            return session

    def ensure_session(self, session_id: str, *, transport: str) -> McpSession:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                session = McpSession(session_id=session_id, transport=transport)
                self._sessions[session_id] = session
            else:
                session.transport = transport
                session.last_event_at = _now_iso()
            return session

    def get_session(self, session_id: str) -> McpSession | None:
        with self._lock:
            return self._sessions.get(session_id)

    def mark_initialized(self, session_id: str, *, client_info: dict[str, Any] | None = None) -> McpSession | None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            session.initialized = True
            if client_info:
                session.client_info = client_info
            session.last_event_at = _now_iso()
            return session

    def enqueue_response(self, session_id: str, payload: dict[str, Any]) -> McpSession | None:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None
            session.queued_responses.append(payload)
            session.last_event_at = _now_iso()
            return session

