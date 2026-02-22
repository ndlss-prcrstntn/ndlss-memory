from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from watch_mode_models import WatchEvent  # noqa: E402
from watch_mode_orchestrator import WatchModeOrchestrator  # noqa: E402
from watch_mode_state import WatchModeState  # noqa: E402


def _configure_repo_env(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "unit-test-qdrant")
    monkeypatch.setenv("QDRANT_API_PORT", "6333")
    monkeypatch.setenv("QDRANT_COLLECTION_NAME", f"watch-test-{uuid4().hex}")
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "0")
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md,.txt")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules")


def test_watch_incremental_delete_cleans_index(tmp_path: Path, monkeypatch):
    _configure_repo_env(monkeypatch)
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)
    target = workspace / "obsolete.md"
    target.write_text("content to remove", encoding="utf-8")

    state = WatchModeState()
    orchestrator = WatchModeOrchestrator(workspace_path=str(workspace), state=state)
    orchestrator.process_events([WatchEvent(event_type="created", path="obsolete.md")])

    target.unlink()
    delete_summary = orchestrator.process_events([WatchEvent(event_type="deleted", path="obsolete.md")])
    payload = delete_summary.to_payload()

    assert payload["deletedRecords"] > 0
    assert payload["failedFiles"] == 0
