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


def _skip_map(summary: dict) -> dict[str, int]:
    return {item["code"]: int(item["count"]) for item in summary["skipBreakdown"]}


def test_full_scan_depth_limit_via_api(monkeypatch, tmp_path: Path):
    _reset_full_scan_state()
    monkeypatch.setattr(handler, "Thread", _ImmediateThread)
    monkeypatch.setenv("INDEX_FILE_TYPES", ".md")
    monkeypatch.setenv("INDEX_EXCLUDE_PATTERNS", "")
    monkeypatch.setenv("INDEX_MAX_FILE_SIZE_BYTES", "1024")

    (tmp_path / "root.md").write_text("root", encoding="utf-8")
    (tmp_path / "level1").mkdir()
    (tmp_path / "level1" / "ok.md").write_text("ok", encoding="utf-8")
    (tmp_path / "level1" / "level2").mkdir()
    (tmp_path / "level1" / "level2" / "too-deep.md").write_text("too deep", encoding="utf-8")

    client = handler.app.test_client()
    start_response = client.post(
        "/v1/indexing/full-scan/jobs",
        json={
            "workspacePath": str(tmp_path),
            "maxTraversalDepth": 1,
            "maxFileSizeBytes": 1024,
        },
    )

    assert start_response.status_code == 202
    job_id = start_response.get_json()["jobId"]

    summary_response = client.get(f"/v1/indexing/full-scan/jobs/{job_id}/summary")
    assert summary_response.status_code == 200
    summary = summary_response.get_json()

    assert summary["appliedLimits"] == {"maxTraversalDepth": 1, "maxFilesPerRun": None}
    assert summary["totals"]["indexedCount"] == 2
    assert _skip_map(summary)["LIMIT_DEPTH_EXCEEDED"] == 1
