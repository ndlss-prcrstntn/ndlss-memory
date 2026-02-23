from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.embedding_provider import EmbeddingProvider
from ingestion_pipeline.ingestion_service import IngestionService
from ingestion_pipeline.vector_upsert_repository import VectorUpsertRepository


def test_docs_indexing_full_scan_isolation(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("alpha docs content", encoding="utf-8")
    (tmp_path / "docs" / "b.md").write_text("beta docs content", encoding="utf-8")
    (tmp_path / "src.py").write_text("print('code')", encoding="utf-8")

    repository = VectorUpsertRepository(
        collection_name="workspace_docs_chunks",
        qdrant_url="http://localhost:6333",
        vector_size=4,
        enable_http_upsert=False,
    )
    service = IngestionService(
        config=ChunkingConfig(chunk_size=32, chunk_overlap=0, retry_max_attempts=1, retry_backoff_seconds=0.0),
        provider=EmbeddingProvider(vector_size=4),
        repository=repository,
        docs_repository=repository,
        docs_file_types_csv=".md",
        docs_exclude_patterns_csv="",
        file_types_csv=".md,.py,.txt",
        exclude_patterns_csv="",
        max_file_size_bytes=4096,
    )

    summary = service.run_docs_index(run_id="docs-isolation", workspace_path=str(tmp_path)).to_dict()

    assert summary["status"] == "completed"
    assert summary["totals"]["indexedDocuments"] == 2
    assert summary["totals"]["updatedDocuments"] == 0
    assert all(point["payload"]["fileType"] == ".md" for point in repository._points.values())  # noqa: SLF001
    assert all(point["payload"]["sourceType"] == "documentation" for point in repository._points.values())  # noqa: SLF001
