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


def test_ingestion_start_rejects_invalid_run_limits(monkeypatch):
    _reset_ingestion_state()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "0")
    monkeypatch.setenv("INGESTION_CHUNK_SIZE", "32")
    monkeypatch.setenv("INGESTION_CHUNK_OVERLAP", "0")
    monkeypatch.setenv("INGESTION_RETRY_MAX_ATTEMPTS", "1")
    monkeypatch.setenv("INGESTION_RETRY_BACKOFF_SECONDS", "0.1")
    client = handler.app.test_client()

    invalid_depth = client.post("/v1/indexing/ingestion/jobs", json={"maxTraversalDepth": -1})
    assert invalid_depth.status_code == 400
    assert invalid_depth.get_json()["errorCode"] == "INVALID_LIMIT_VALUE"

    invalid_max_files = client.post("/v1/indexing/ingestion/jobs", json={"maxFilesPerRun": 0})
    assert invalid_max_files.status_code == 400
    assert invalid_max_files.get_json()["errorCode"] == "INVALID_LIMIT_VALUE"


def test_ingestion_status_contains_applied_limits(monkeypatch, tmp_path: Path):
    _reset_ingestion_state()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INDEX_MAX_FILE_SIZE_BYTES", "1024")
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "0")
    monkeypatch.setenv("INGESTION_CHUNK_SIZE", "32")
    monkeypatch.setenv("INGESTION_CHUNK_OVERLAP", "0")
    monkeypatch.setenv("INGESTION_RETRY_MAX_ATTEMPTS", "1")
    monkeypatch.setenv("INGESTION_RETRY_BACKOFF_SECONDS", "0.1")
    (tmp_path / "doc.md").write_text("hello", encoding="utf-8")

    client = handler.app.test_client()
    start_response = client.post(
        "/v1/indexing/ingestion/jobs",
        json={"workspacePath": str(tmp_path), "maxTraversalDepth": 1, "maxFilesPerRun": 3},
    )
    assert start_response.status_code == 202

    run_id = start_response.get_json()["runId"]
    status_response = client.get(f"/v1/indexing/ingestion/jobs/{run_id}")
    assert status_response.status_code == 200
    payload = status_response.get_json()
    assert payload["appliedLimits"] == {"maxTraversalDepth": 1, "maxFilesPerRun": 3}
