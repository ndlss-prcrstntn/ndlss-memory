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


def _skip_codes(summary: dict) -> set[str]:
    return {item["code"] for item in summary.get("skipBreakdown", [])}


def test_ingestion_summary_contract_includes_run_limits(monkeypatch, tmp_path: Path):
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

    def _fake_run_ingestion_job(run_id: str, workspace_path: str, payload: dict):
        run = handler.INGESTION_STATE.get_run(run_id)
        assert run is not None
        summary = {
            "runId": run_id,
            "status": "completed",
            "totalFiles": 1,
            "totalChunks": 1,
            "embeddedChunks": 1,
            "failedChunks": 0,
            "retryCount": 0,
            "startedAt": run.started_at,
            "finishedAt": run.started_at,
            "metadataCoverage": {
                "path": 1.0,
                "fileName": 1.0,
                "fileType": 1.0,
                "contentHash": 1.0,
                "timestamp": 1.0,
            },
            "appliedLimits": {
                "maxTraversalDepth": run.max_traversal_depth,
                "maxFilesPerRun": run.max_files_per_run,
            },
            "skipBreakdown": [
                {"code": "LIMIT_DEPTH_EXCEEDED", "count": 1},
                {"code": "LIMIT_MAX_FILES_REACHED", "count": 1},
            ],
        }
        handler.INGESTION_STATE.finish_run(run_id, summary=summary, status="completed")

    monkeypatch.setattr(handler, "_run_ingestion_job", _fake_run_ingestion_job)

    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "deep").mkdir()
    (tmp_path / "deep" / "c.md").write_text("c", encoding="utf-8")

    client = handler.app.test_client()
    start_response = client.post(
        "/v1/indexing/ingestion/jobs",
        json={
            "workspacePath": str(tmp_path),
            "maxTraversalDepth": 0,
            "maxFilesPerRun": 1,
        },
    )
    assert start_response.status_code == 202

    run_id = start_response.get_json()["runId"]
    summary_response = client.get(f"/v1/indexing/ingestion/jobs/{run_id}/summary")
    assert summary_response.status_code == 200

    payload = summary_response.get_json()
    assert payload["runId"] == run_id
    assert payload["status"] in {"completed", "partial", "failed"}
    assert payload["appliedLimits"] == {"maxTraversalDepth": 0, "maxFilesPerRun": 1}
    assert isinstance(payload["skipBreakdown"], list)
    assert isinstance(payload["metadataCoverage"], dict)
    skip_codes = _skip_codes(payload)
    assert "LIMIT_DEPTH_EXCEEDED" in skip_codes
    assert "LIMIT_MAX_FILES_REACHED" in skip_codes
