from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.versioning import resolve_service_version


def test_resolve_service_version_uses_explicit_ndlss_version(monkeypatch):
    monkeypatch.setenv("NDLSS_VERSION", "0.2.9")
    monkeypatch.setenv("NDLSS_IMAGE_TAG", "0.2.8")
    monkeypatch.setenv("NDLSS_GIT_REF", "main")

    assert resolve_service_version() == "0.2.9"


def test_resolve_service_version_falls_back_to_image_tag(monkeypatch):
    monkeypatch.delenv("NDLSS_VERSION", raising=False)
    monkeypatch.setenv("NDLSS_IMAGE_TAG", "0.2.9")
    monkeypatch.setenv("NDLSS_GIT_REF", "main")

    assert resolve_service_version() == "0.2.9"


def test_resolve_service_version_falls_back_to_git_ref(monkeypatch):
    monkeypatch.delenv("NDLSS_VERSION", raising=False)
    monkeypatch.delenv("NDLSS_IMAGE_TAG", raising=False)
    monkeypatch.setenv("NDLSS_GIT_REF", "main")

    assert resolve_service_version() == "main"


def test_resolve_service_version_returns_unknown_when_empty(monkeypatch):
    monkeypatch.delenv("NDLSS_VERSION", raising=False)
    monkeypatch.delenv("NDLSS_IMAGE_TAG", raising=False)
    monkeypatch.delenv("NDLSS_GIT_REF", raising=False)

    assert resolve_service_version() == "unknown"
