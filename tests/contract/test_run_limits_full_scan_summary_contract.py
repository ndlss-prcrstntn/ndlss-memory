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


def _reset_full_scan_state() -> None:
    handler.FULL_SCAN_STATE._jobs.clear()  # noqa: SLF001
    handler.FULL_SCAN_STATE._active_job_id = None  # noqa: SLF001


def _skip_codes(summary: dict) -> set[str]:
    return {item["code"] for item in summary.get("skipBreakdown", [])}


def test_full_scan_summary_contract_includes_run_limits(monkeypatch, tmp_path: Path):
    _reset_full_scan_state()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INDEX_MAX_FILE_SIZE_BYTES", "1024")

    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "deep").mkdir()
    (tmp_path / "deep" / "c.md").write_text("c", encoding="utf-8")

    client = handler.app.test_client()
    start_response = client.post(
        "/v1/indexing/full-scan/jobs",
        json={
            "workspacePath": str(tmp_path),
            "maxTraversalDepth": 0,
            "maxFilesPerRun": 1,
            "maxFileSizeBytes": 1024,
        },
    )
    assert start_response.status_code == 202

    job_id = start_response.get_json()["jobId"]
    summary_response = client.get(f"/v1/indexing/full-scan/jobs/{job_id}/summary")
    assert summary_response.status_code == 200

    payload = summary_response.get_json()
    assert payload["jobId"] == job_id
    assert payload["result"] in {"completed", "failed", "cancelled"}
    assert isinstance(payload["durationSeconds"], (float, int))
    assert payload["appliedLimits"] == {"maxTraversalDepth": 0, "maxFilesPerRun": 1}
    assert isinstance(payload["totals"], dict)
    assert isinstance(payload["skipBreakdown"], list)
    skip_codes = _skip_codes(payload)
    assert "LIMIT_DEPTH_EXCEEDED" in skip_codes
    assert "LIMIT_MAX_FILES_REACHED" in skip_codes
