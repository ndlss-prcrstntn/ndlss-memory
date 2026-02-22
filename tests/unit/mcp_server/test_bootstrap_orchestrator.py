from __future__ import annotations

import threading
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from bootstrap_orchestrator import BootstrapOrchestrator  # noqa: E402
from bootstrap_state import BootstrapStateRecord, build_workspace_key  # noqa: E402


class _InMemoryStateRepository:
    def __init__(self, initial: BootstrapStateRecord | None = None) -> None:
        self._record = initial
        self._lock = threading.Lock()

    def get(self, workspace_key: str) -> BootstrapStateRecord | None:
        with self._lock:
            if self._record is None:
                return None
            if self._record.workspace_key != workspace_key:
                return None
            return self._record

    def upsert(self, record: BootstrapStateRecord) -> None:
        with self._lock:
            self._record = record


class _CollectionService:
    def __init__(self, *, collection_name: str = "workspace_chunks", created: bool = True, points: int = 0) -> None:
        self.collection_name = collection_name
        self._created = created
        self._points = points

    def ensure_collection_exists(self) -> bool:
        return self._created

    def point_count(self) -> int:
        return self._points

    def snapshot(self, checked_at: str):
        return type(
            "Snapshot",
            (),
            {
                "to_dict": lambda self_: {
                    "collectionName": self.collection_name,
                    "exists": True,
                    "pointCount": self._points,
                    "checkedAt": checked_at,
                }
            },
        )()


def test_skip_when_bootstrap_completed():
    workspace_key = build_workspace_key("/workspace")
    existing = BootstrapStateRecord(
        workspace_key=workspace_key,
        collection_name="workspace_chunks",
        status="completed",
        last_run_id="run-completed",
    )
    orchestrator = BootstrapOrchestrator(
        state_repository=_InMemoryStateRepository(existing),
        collection_service=_CollectionService(created=False),
    )
    called = {"count": 0}

    def _start(_workspace_path: str) -> str:
        called["count"] += 1
        return "run-new"

    decision = orchestrator.evaluate_startup(workspace_path="/workspace", start_ingestion_run=_start)

    assert decision.decision == "skip-already-completed"
    assert decision.status == "ready"
    assert decision.run_id == "run-completed"
    assert called["count"] == 0


def test_skip_failed_retry_when_disabled(monkeypatch):
    monkeypatch.setenv("BOOTSTRAP_RETRY_FAILED_ON_START", "0")
    workspace_key = build_workspace_key("/workspace")
    existing = BootstrapStateRecord(
        workspace_key=workspace_key,
        collection_name="workspace_chunks",
        status="failed",
        last_run_id="run-failed",
        error_code="BOOTSTRAP_PIPELINE_FAILED",
        error_message="ingestion failed",
    )
    orchestrator = BootstrapOrchestrator(
        state_repository=_InMemoryStateRepository(existing),
        collection_service=_CollectionService(created=False),
    )

    decision = orchestrator.evaluate_startup(workspace_path="/workspace", start_ingestion_run=lambda _: "run-new")

    assert decision.decision == "skip-already-completed"
    assert decision.status == "failed"
    assert decision.error_code in {"BOOTSTRAP_PIPELINE_FAILED", "BOOTSTRAP_RETRY_DISABLED"}


def test_concurrent_startup_runs_only_once():
    repository = _InMemoryStateRepository()
    orchestrator = BootstrapOrchestrator(
        state_repository=repository,
        collection_service=_CollectionService(created=True),
    )
    calls = {"count": 0}
    results = []

    def _start(_workspace_path: str) -> str:
        calls["count"] += 1
        time.sleep(0.05)
        return "run-auto"

    def _worker() -> None:
        decision = orchestrator.evaluate_startup(workspace_path="/workspace", start_ingestion_run=_start)
        results.append(decision.decision)

    t1 = threading.Thread(target=_worker)
    t2 = threading.Thread(target=_worker)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert calls["count"] == 1
    assert "run" in results
    assert "skip-already-completed" in results
