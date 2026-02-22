from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import bootstrap_orchestrator as module  # noqa: E402
from bootstrap_state import BootstrapStateRecord, build_workspace_key  # noqa: E402


class _Repo:
    def __init__(self) -> None:
        self.record = BootstrapStateRecord(
            workspace_key=build_workspace_key("/workspace"),
            collection_name="workspace_chunks",
            status="completed",
            last_run_id="run-initial",
            attempt=1,
        )

    def get(self, _workspace_key: str):
        return self.record

    def upsert(self, record):
        self.record = record


class _Collection:
    collection_name = "workspace_chunks"

    def ensure_collection_exists(self):
        return False

    def point_count(self):
        return 42


def test_restart_does_not_trigger_expensive_bootstrap():
    orchestrator = module.BootstrapOrchestrator(
        state_repository=_Repo(),
        collection_service=_Collection(),
    )
    called = {"count": 0}

    def _start(_workspace_path: str) -> str:
        called["count"] += 1
        return "run-second"

    decision = orchestrator.evaluate_startup(workspace_path="/workspace", start_ingestion_run=_start)

    assert decision.decision == "skip-already-completed"
    assert decision.status == "ready"
    assert called["count"] == 0
