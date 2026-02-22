from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from bootstrap_collection_service import BootstrapCollectionService  # noqa: E402
from bootstrap_state_repository import BootstrapStateRepository  # noqa: E402


def test_bootstrap_services_use_internal_qdrant_api_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.setenv("QDRANT_API_PORT", "6333")

    collection_service = BootstrapCollectionService.from_env()
    state_repository = BootstrapStateRepository.from_env()

    assert collection_service.qdrant_url == "http://qdrant:6333"
    assert state_repository.qdrant_url == "http://qdrant:6333"
