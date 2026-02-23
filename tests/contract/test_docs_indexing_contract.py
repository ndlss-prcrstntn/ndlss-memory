from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


class _ImmediateThread:
    def __init__(self, target, args=(), kwargs=None, daemon=None):
        self._target = target
        self._args = args
        self._kwargs = kwargs or {}

    def start(self):
        self._target(*self._args, **self._kwargs)


def _reset_ingestion_state() -> None:
    handler.INGESTION_STATE._runs.clear()  # noqa: SLF001
    handler.INGESTION_STATE._active_run_id = None  # noqa: SLF001


def test_docs_indexing_start_and_summary_contract(monkeypatch, tmp_path: Path):
    _reset_ingestion_state()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "0")
    monkeypatch.setenv("DOCS_INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("DOCS_INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INGESTION_CHUNK_SIZE", "32")
    monkeypatch.setenv("INGESTION_CHUNK_OVERLAP", "0")
    monkeypatch.setenv("INGESTION_RETRY_MAX_ATTEMPTS", "1")
    monkeypatch.setenv("INGESTION_RETRY_BACKOFF_SECONDS", "0.1")

    (tmp_path / "guide.md").write_text("docs contract content", encoding="utf-8")
    client = handler.app.test_client()

    start_response = client.post(
        "/v1/indexing/docs/jobs",
        json={"workspacePath": str(tmp_path), "includeExtensions": [".md"]},
    )
    assert start_response.status_code == 202
    start_payload = start_response.get_json()
    assert "runId" in start_payload
    assert start_payload["status"] in {"running", "completed"}
    assert "acceptedAt" in start_payload

    run_id = start_payload["runId"]
    summary_response = client.get(f"/v1/indexing/docs/jobs/{run_id}/summary")
    assert summary_response.status_code == 200
    payload = summary_response.get_json()
    assert payload["runId"] == run_id
    assert payload["status"] in {"completed", "partial", "failed"}
    assert isinstance(payload["totals"]["processedDocuments"], int)
    assert isinstance(payload["totals"]["indexedDocuments"], int)
    assert isinstance(payload["totals"]["updatedDocuments"], int)
    assert isinstance(payload["totals"]["skippedDocuments"], int)
    assert isinstance(payload["totals"]["deletedDocuments"], int)
    assert isinstance(payload["skipBreakdown"], list)
