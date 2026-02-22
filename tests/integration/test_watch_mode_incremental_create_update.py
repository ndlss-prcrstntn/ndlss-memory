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


def test_watch_incremental_create_and_update(tmp_path: Path, monkeypatch):
    _configure_repo_env(monkeypatch)
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)
    target = workspace / "feature.md"
    target.write_text("watch mode create content", encoding="utf-8")

    state = WatchModeState()
    orchestrator = WatchModeOrchestrator(workspace_path=str(workspace), state=state)

    create_summary = orchestrator.process_events([WatchEvent(event_type="created", path="feature.md")])
    create_payload = create_summary.to_payload()
    assert create_payload["indexedFiles"] == 1
    assert create_payload["failedFiles"] == 0

    target.write_text("watch mode updated content", encoding="utf-8")
    update_summary = orchestrator.process_events([WatchEvent(event_type="updated", path="feature.md")])
    update_payload = update_summary.to_payload()
    assert update_payload["indexedFiles"] == 1
    assert update_payload["failedFiles"] == 0
    assert "feature.md" in update_payload["affectedFiles"]
