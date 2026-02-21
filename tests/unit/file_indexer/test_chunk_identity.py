from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.chunk_identity import build_chunk_identity


def test_chunk_identity_is_deterministic():
    a = build_chunk_identity(file_path="docs/a.md", chunk_index=0, chunk_text="alpha")
    b = build_chunk_identity(file_path="docs/a.md", chunk_index=0, chunk_text="alpha")
    assert a.chunk_id == b.chunk_id


def test_chunk_identity_changes_when_chunk_text_changes():
    a = build_chunk_identity(file_path="docs/a.md", chunk_index=0, chunk_text="alpha")
    b = build_chunk_identity(file_path="docs/a.md", chunk_index=0, chunk_text="beta")
    assert a.chunk_id != b.chunk_id


def test_chunk_identity_changes_when_index_changes():
    a = build_chunk_identity(file_path="docs/a.md", chunk_index=0, chunk_text="alpha")
    b = build_chunk_identity(file_path="docs/a.md", chunk_index=1, chunk_text="alpha")
    assert a.chunk_id != b.chunk_id

