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
    monkeypatch.setenv("WATCH_MAX_EVENTS_PER_CYCLE", "500")


def test_watch_handles_burst_without_failed_state(tmp_path: Path, monkeypatch):
    _configure_repo_env(monkeypatch)
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)

    events: list[WatchEvent] = []
    for index in range(120):
        file_path = workspace / f"burst-{index}.md"
        file_path.write_text(f"burst file {index}", encoding="utf-8")
        events.append(WatchEvent(event_type="created", path=file_path.name))

    state = WatchModeState()
    orchestrator = WatchModeOrchestrator(workspace_path=str(workspace), state=state)
    state.start(str(workspace))
    state.set_state("running")

    orchestrator._on_events(events)  # noqa: SLF001
    status = state.get_status()
    summary = state.get_last_summary()

    assert status["state"] == "running"
    assert status["failedEvents"] == 0
    assert summary is not None
    assert summary["indexedFiles"] >= 100
