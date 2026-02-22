from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from ingestion_pipeline.file_fingerprint import FileFingerprint


def test_file_fingerprint_new_file():
    fp = FileFingerprint.from_content(file_path="docs/readme.md", content="hello", previous_hash=None)
    assert fp.status == "new"
    assert len(fp.content_hash) == 64


def test_file_fingerprint_unchanged_file():
    a = FileFingerprint.from_content(file_path="docs/readme.md", content="hello", previous_hash=None)
    b = FileFingerprint.from_content(file_path="docs/readme.md", content="hello", previous_hash=a.content_hash)
    assert b.status == "unchanged"


def test_file_fingerprint_changed_file():
    a = FileFingerprint.from_content(file_path="docs/readme.md", content="hello", previous_hash=None)
    b = FileFingerprint.from_content(file_path="docs/readme.md", content="hello world", previous_hash=a.content_hash)
    assert b.status == "changed"


def test_file_fingerprint_hash_is_stable_for_same_input():
    a = FileFingerprint.from_content(file_path="docs/readme.md", content="stable-content", previous_hash=None)
    b = FileFingerprint.from_content(file_path="docs/readme.md", content="stable-content", previous_hash=None)
    assert a.content_hash == b.content_hash


def test_file_fingerprint_deleted_status():
    deleted = FileFingerprint.deleted(file_path="docs/readme.md", previous_hash="abc")
    assert deleted.status == "deleted"
    assert deleted.previous_hash == "abc"
    assert deleted.content_hash == ""

