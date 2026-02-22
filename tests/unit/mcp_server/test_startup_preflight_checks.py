from pathlib import Path
import sys
import urllib.error

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from startup_preflight_checks import run_startup_preflight  # noqa: E402
from startup_preflight_errors import StartupPreflightError  # noqa: E402


class _DummyHttpResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_preflight_fails_when_qdrant_unreachable(monkeypatch):
    workspace = str(ROOT)
    monkeypatch.setenv("WORKSPACE_PATH", workspace)
    monkeypatch.setenv("INDEX_MODE", "full-scan")

    def _raise_unreachable(*args, **kwargs):
        raise urllib.error.URLError("connection refused")

    monkeypatch.setattr("startup_preflight_checks.urllib.request.urlopen", _raise_unreachable)

    with pytest.raises(StartupPreflightError) as exc_info:
        run_startup_preflight()

    assert exc_info.value.error_code == "STARTUP_PREFLIGHT_FAILED"
    report = exc_info.value.to_failure_report()
    assert report["errorCode"] == "STARTUP_PREFLIGHT_FAILED"
    assert any(item["errorCode"] == "PREFLIGHT_QDRANT_UNREACHABLE" for item in report["failedChecks"])


def test_preflight_fails_when_workspace_missing(monkeypatch):
    monkeypatch.setenv("WORKSPACE_PATH", str(ROOT / "missing-workspace-path"))
    monkeypatch.setenv("INDEX_MODE", "full-scan")
    monkeypatch.setattr("startup_preflight_checks.urllib.request.urlopen", lambda *a, **k: _DummyHttpResponse())

    with pytest.raises(StartupPreflightError) as exc_info:
        run_startup_preflight()

    report = exc_info.value.to_failure_report()
    assert any(item["errorCode"] == "PREFLIGHT_WORKSPACE_NOT_FOUND" for item in report["failedChecks"])


def test_preflight_fails_when_git_required_but_missing(monkeypatch):
    monkeypatch.setenv("WORKSPACE_PATH", str(ROOT))
    monkeypatch.setenv("INDEX_MODE", "delta-after-commit")
    monkeypatch.setenv("STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA", "1")
    monkeypatch.setattr("startup_preflight_checks.urllib.request.urlopen", lambda *a, **k: _DummyHttpResponse())
    monkeypatch.setattr("startup_preflight_checks.shutil.which", lambda *_: None)

    with pytest.raises(StartupPreflightError) as exc_info:
        run_startup_preflight()

    report = exc_info.value.to_failure_report()
    assert any(item["errorCode"] == "PREFLIGHT_GIT_NOT_AVAILABLE" for item in report["failedChecks"])


def test_preflight_passes_in_full_scan_when_dependencies_available(monkeypatch):
    monkeypatch.setenv("WORKSPACE_PATH", str(ROOT))
    monkeypatch.setenv("INDEX_MODE", "full-scan")
    monkeypatch.setattr("startup_preflight_checks.urllib.request.urlopen", lambda *a, **k: _DummyHttpResponse())

    context, checks = run_startup_preflight()

    assert context["indexMode"] == "full-scan"
    by_id = {item.check_id: item for item in checks}
    assert by_id["qdrant_reachability"].status == "passed"
    assert by_id["workspace_readable"].status == "passed"
    assert by_id["git_available"].status == "skipped"

