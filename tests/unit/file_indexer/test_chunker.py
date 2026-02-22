from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.chunk_record_builder import build_chunk_records
from ingestion_pipeline.chunker import chunk_text
from ingestion_pipeline.chunking_validation import ChunkingConfigError


def test_chunker_respects_size_and_overlap():
    chunks = chunk_text("abcdefghijklmnopqrstuvwxyz", chunk_size=8, chunk_overlap=2)
    assert chunks == ["abcdefgh", "ghijklmn", "mnopqrst", "stuvwxyz"]


def test_chunker_rejects_invalid_overlap():
    try:
        chunk_text("abc", chunk_size=4, chunk_overlap=4)
        assert False, "ChunkingConfigError was expected"
    except ChunkingConfigError:
        assert True


def test_chunk_records_are_deterministic_and_ordered():
    root = ROOT / "tests" / "fixtures" / "full-scan"
    file_path = root / "valid" / "readme.md"
    content = "0123456789abcdef" * 8
    config = ChunkingConfig(
        chunk_size=16,
        chunk_overlap=4,
        retry_max_attempts=3,
        retry_backoff_seconds=1.0,
    )
    a = build_chunk_records(root=root, file_path=file_path, content=content, config=config, processed_at="2026-02-21T10:00:00Z")
    b = build_chunk_records(root=root, file_path=file_path, content=content, config=config, processed_at="2026-02-21T10:00:00Z")
    assert [item.chunk_index for item in a] == list(range(len(a)))
    assert [item.chunk_id for item in a] == [item.chunk_id for item in b]


def test_chunker_returns_empty_for_empty_content():
    assert chunk_text("", chunk_size=16, chunk_overlap=4) == []


def test_chunker_respects_max_chunks_per_file():
    chunks = chunk_text(
        "0123456789abcdefghijklmnopqrstuvwxyz",
        chunk_size=10,
        chunk_overlap=2,
        max_chunks_per_file=2,
    )
    assert len(chunks) == 2
    assert chunks[0] == "0123456789"
    assert chunks[1] == "89abcdefgh"

