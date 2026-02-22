from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_errors import SearchApiError
from search_result_ref import build_result_id, parse_result_id
from search_service import SearchService


class _ResolutionRepoStub:
    def get_source_by_result_id(self, result_id):
        if result_id == "chunk:1111111111111111111111111111111111111111111111111111111111111111":
            return {
                "resultId": result_id,
                "content": "example-content",
                "sourcePath": "docs/readme.md",
                "chunkIndex": 0,
            }
        return None

    def get_metadata_by_result_id(self, result_id):
        if result_id == "chunk:1111111111111111111111111111111111111111111111111111111111111111":
            return {
                "resultId": result_id,
                "fileName": "readme.md",
                "fileType": ".md",
                "sourcePath": "docs/readme.md",
                "contentHash": "abc",
                "indexedAt": "2026-02-21T00:00:00Z",
            }
        return None


def test_result_id_roundtrip_is_stable():
    point_id = "1111111111111111111111111111111111111111111111111111111111111111"
    result_id = build_result_id(point_id)
    assert parse_result_id(result_id) == point_id


def test_result_id_roundtrip_accepts_uuid():
    point_id = "11111111-1111-4111-8111-111111111111"
    result_id = build_result_id(point_id)
    assert parse_result_id(result_id) == point_id


def test_source_and_metadata_raise_not_found_for_unknown_id():
    service = SearchService(_ResolutionRepoStub())
    missing = "chunk:2222222222222222222222222222222222222222222222222222222222222222"

    with pytest.raises(SearchApiError) as source_err:
        service.get_source(missing)
    assert source_err.value.code == "RESULT_NOT_FOUND"

    with pytest.raises(SearchApiError) as metadata_err:
        service.get_metadata(missing)
    assert metadata_err.value.code == "RESULT_NOT_FOUND"


def test_invalid_result_id_format_raises_invalid_request():
    with pytest.raises(SearchApiError) as exc:
        parse_result_id("bad-id")
    assert exc.value.code == "INVALID_REQUEST"
