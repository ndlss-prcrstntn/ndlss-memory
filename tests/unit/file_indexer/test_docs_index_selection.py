from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.embedding_provider import EmbeddingProvider
from ingestion_pipeline.ingestion_service import IngestionService
from ingestion_pipeline.vector_upsert_repository import VectorUpsertRepository


def _build_service(repo: VectorUpsertRepository) -> IngestionService:
    return IngestionService(
        config=ChunkingConfig(chunk_size=20, chunk_overlap=0, retry_max_attempts=1, retry_backoff_seconds=0.0),
        provider=EmbeddingProvider(vector_size=4),
        repository=repo,
        docs_repository=repo,
        file_types_csv=".md,.py,.txt",
        exclude_patterns_csv="",
        docs_file_types_csv=".md",
        docs_exclude_patterns_csv="",
        max_file_size_bytes=4096,
    )


def _skip_map(summary: dict) -> dict[str, int]:
    return {item["code"]: int(item["count"]) for item in summary.get("skipBreakdown", [])}


def test_docs_index_selects_markdown_and_uses_stable_chunk_ids(tmp_path: Path):
    doc = tmp_path / "guide.md"
    doc.write_text("alpha alpha alpha alpha alpha alpha", encoding="utf-8")
    (tmp_path / "main.py").write_text("print('hello')", encoding="utf-8")

    repository = VectorUpsertRepository(
        collection_name="workspace_docs_chunks",
        qdrant_url="http://localhost:6333",
        vector_size=4,
        enable_http_upsert=False,
    )
    service = _build_service(repository)

    first = service.run_docs_index(run_id="docs-run-1", workspace_path=str(tmp_path)).to_dict()
    ids_before = sorted(repository._points.keys())  # noqa: SLF001
    metadata_before = [repository._points[item]["payload"]["chunkIndex"] for item in ids_before]  # noqa: SLF001

    doc.write_text("beta beta beta beta beta beta", encoding="utf-8")
    second = service.run_docs_index(run_id="docs-run-2", workspace_path=str(tmp_path)).to_dict()
    ids_after = sorted(repository._points.keys())  # noqa: SLF001
    metadata_after = [repository._points[item]["payload"]["chunkIndex"] for item in ids_after]  # noqa: SLF001

    assert first["totals"]["indexedDocuments"] == 1
    assert second["totals"]["updatedDocuments"] == 1
    assert ids_before == ids_after
    assert metadata_before == metadata_after
    assert all(point["payload"]["path"].endswith(".md") for point in repository._points.values())  # noqa: SLF001
    assert _skip_map(first).get("UNSUPPORTED_EXTENSION", 0) >= 1
