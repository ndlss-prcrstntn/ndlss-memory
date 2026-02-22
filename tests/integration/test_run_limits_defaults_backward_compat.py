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


def _reset_states() -> None:
    handler.FULL_SCAN_STATE._jobs.clear()  # noqa: SLF001
    handler.FULL_SCAN_STATE._active_job_id = None  # noqa: SLF001
    handler.INGESTION_STATE._runs.clear()  # noqa: SLF001
    handler.INGESTION_STATE._active_run_id = None  # noqa: SLF001


def _skip_codes(summary: dict) -> set[str]:
    return {item["code"] for item in summary.get("skipBreakdown", [])}


def test_defaults_keep_backward_compatible_behavior(monkeypatch, tmp_path: Path):
    _reset_states()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INDEX_MAX_FILE_SIZE_BYTES", "1024")
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "0")
    monkeypatch.setenv("INGESTION_CHUNK_SIZE", "32")
    monkeypatch.setenv("INGESTION_CHUNK_OVERLAP", "0")
    monkeypatch.setenv("INGESTION_RETRY_MAX_ATTEMPTS", "1")
    monkeypatch.setenv("INGESTION_RETRY_BACKOFF_SECONDS", "0.1")

    (tmp_path / "one.md").write_text("one", encoding="utf-8")
    (tmp_path / "two.md").write_text("two", encoding="utf-8")

    client = handler.app.test_client()

    full_scan_start = client.post(
        "/v1/indexing/full-scan/jobs",
        json={"workspacePath": str(tmp_path), "maxFileSizeBytes": 1024},
    )
    assert full_scan_start.status_code == 202
    full_scan_job_id = full_scan_start.get_json()["jobId"]
    full_scan_summary = client.get(f"/v1/indexing/full-scan/jobs/{full_scan_job_id}/summary").get_json()

    ingestion_start = client.post("/v1/indexing/ingestion/jobs", json={"workspacePath": str(tmp_path)})
    assert ingestion_start.status_code == 202
    ingestion_run_id = ingestion_start.get_json()["runId"]
    ingestion_summary = client.get(f"/v1/indexing/ingestion/jobs/{ingestion_run_id}/summary").get_json()

    assert full_scan_summary["appliedLimits"] == {"maxTraversalDepth": None, "maxFilesPerRun": None}
    assert ingestion_summary["appliedLimits"] == {"maxTraversalDepth": None, "maxFilesPerRun": None}
    assert "LIMIT_DEPTH_EXCEEDED" not in _skip_codes(full_scan_summary)
    assert "LIMIT_MAX_FILES_REACHED" not in _skip_codes(full_scan_summary)
    assert "LIMIT_DEPTH_EXCEEDED" not in _skip_codes(ingestion_summary)
    assert "LIMIT_MAX_FILES_REACHED" not in _skip_codes(ingestion_summary)
