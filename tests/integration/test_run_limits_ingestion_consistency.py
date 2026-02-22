from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
FILE_INDEXER_SRC = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(FILE_INDEXER_SRC))

from full_scan_service import run_full_scan
from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.embedding_provider import EmbeddingProvider
from ingestion_pipeline.ingestion_service import IngestionService
from ingestion_pipeline.vector_upsert_repository import VectorUpsertRepository


def _skip_map(summary: dict) -> dict[str, int]:
    return {item["code"]: int(item["count"]) for item in summary.get("skipBreakdown", [])}


def test_ingestion_and_full_scan_apply_limits_consistently(tmp_path: Path):
    (tmp_path / "a.md").write_text("alpha", encoding="utf-8")
    (tmp_path / "b.md").write_text("beta", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "c.md").write_text("gamma", encoding="utf-8")
    (tmp_path / "nested" / "deep").mkdir()
    (tmp_path / "nested" / "deep" / "d.md").write_text("delta", encoding="utf-8")

    full_scan_summary = run_full_scan(
        workspace_path=str(tmp_path),
        file_types_csv=".md",
        exclude_patterns_csv="",
        max_file_size_bytes=1024,
        max_traversal_depth=1,
        max_files_per_run=2,
        progress_interval_seconds=60,
    )

    config = ChunkingConfig(chunk_size=32, chunk_overlap=0, retry_max_attempts=1, retry_backoff_seconds=0.1)
    provider = EmbeddingProvider(vector_size=4)
    repository = VectorUpsertRepository(
        collection_name="test_collection",
        qdrant_url="http://localhost:6333",
        vector_size=4,
        enable_http_upsert=False,
    )
    ingestion_summary = IngestionService(
        config=config,
        provider=provider,
        repository=repository,
        file_types_csv=".md",
        exclude_patterns_csv="",
        max_file_size_bytes=1024,
        max_traversal_depth=1,
        max_files_per_run=2,
    ).run(run_id="run-limits-consistency", workspace_path=str(tmp_path)).to_dict()

    assert ingestion_summary["appliedLimits"] == full_scan_summary["appliedLimits"]
    assert ingestion_summary["totalFiles"] == full_scan_summary["indexedCount"]

    fs_skip = _skip_map(full_scan_summary)
    ing_skip = _skip_map(ingestion_summary)
    assert ing_skip["LIMIT_DEPTH_EXCEEDED"] == fs_skip["LIMIT_DEPTH_EXCEEDED"]
    assert ing_skip["LIMIT_MAX_FILES_REACHED"] == fs_skip["LIMIT_MAX_FILES_REACHED"]
