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


def _skip_map(summary: dict) -> dict[str, int]:
    return {item["code"]: int(item["count"]) for item in summary.get("skipBreakdown", [])}


def test_summary_reports_depth_and_max_files_skip_reasons(monkeypatch, tmp_path: Path):
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

    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "c.md").write_text("c", encoding="utf-8")

    client = handler.app.test_client()
    limits_payload = {
        "workspacePath": str(tmp_path),
        "maxTraversalDepth": 0,
        "maxFilesPerRun": 1,
        "maxFileSizeBytes": 1024,
    }

    full_scan_start = client.post("/v1/indexing/full-scan/jobs", json=limits_payload)
    assert full_scan_start.status_code == 202
    full_scan_job_id = full_scan_start.get_json()["jobId"]
    full_scan_summary = client.get(f"/v1/indexing/full-scan/jobs/{full_scan_job_id}/summary").get_json()

    ingestion_start = client.post("/v1/indexing/ingestion/jobs", json=limits_payload)
    assert ingestion_start.status_code == 202
    ingestion_run_id = ingestion_start.get_json()["runId"]
    ingestion_summary = client.get(f"/v1/indexing/ingestion/jobs/{ingestion_run_id}/summary").get_json()

    full_scan_skip = _skip_map(full_scan_summary)
    ingestion_skip = _skip_map(ingestion_summary)

    assert full_scan_summary["appliedLimits"] == {"maxTraversalDepth": 0, "maxFilesPerRun": 1}
    assert ingestion_summary["appliedLimits"] == {"maxTraversalDepth": 0, "maxFilesPerRun": 1}
    assert full_scan_skip["LIMIT_DEPTH_EXCEEDED"] >= 1
    assert full_scan_skip["LIMIT_MAX_FILES_REACHED"] >= 1
    assert ingestion_skip["LIMIT_DEPTH_EXCEEDED"] >= 1
    assert ingestion_skip["LIMIT_MAX_FILES_REACHED"] >= 1
