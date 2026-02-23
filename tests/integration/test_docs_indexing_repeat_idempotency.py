from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.embedding_provider import EmbeddingProvider
from ingestion_pipeline.ingestion_service import IngestionService
from ingestion_pipeline.vector_upsert_repository import VectorUpsertRepository


def test_docs_indexing_repeat_run_is_idempotent(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "readme.md").write_text("stable docs", encoding="utf-8")

    repository = VectorUpsertRepository(
        collection_name="workspace_docs_chunks",
        qdrant_url="http://localhost:6333",
        vector_size=4,
        enable_http_upsert=False,
    )
    service = IngestionService(
        config=ChunkingConfig(chunk_size=24, chunk_overlap=0, retry_max_attempts=1, retry_backoff_seconds=0.0),
        provider=EmbeddingProvider(vector_size=4),
        repository=repository,
        docs_repository=repository,
        docs_file_types_csv=".md",
        docs_exclude_patterns_csv="",
        file_types_csv=".md",
        exclude_patterns_csv="",
        max_file_size_bytes=4096,
    )

    first = service.run_docs_index(run_id="docs-repeat-1", workspace_path=str(tmp_path)).to_dict()
    points_after_first = len(repository._points)  # noqa: SLF001
    second = service.run_docs_index(run_id="docs-repeat-2", workspace_path=str(tmp_path)).to_dict()
    points_after_second = len(repository._points)  # noqa: SLF001

    assert first["totals"]["indexedDocuments"] == 1
    assert second["totals"]["indexedDocuments"] == 0
    assert second["totals"]["updatedDocuments"] == 0
    assert second["totals"]["skippedDocuments"] >= 1
    assert points_after_first == points_after_second
