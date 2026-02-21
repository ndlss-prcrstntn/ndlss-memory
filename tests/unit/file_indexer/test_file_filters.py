from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from file_type_filter import is_supported_file, parse_supported_types
from path_exclude_filter import is_excluded_path, parse_exclude_patterns


def test_parse_supported_types_normalizes_dot_and_case():
    allowed = parse_supported_types(".md,TXT,json")
    assert allowed == {".md", ".txt", ".json"}


def test_is_supported_file_uses_case_insensitive_suffix():
    allowed = {".md", ".txt"}
    assert is_supported_file(Path("ReadMe.MD"), allowed)
    assert not is_supported_file(Path("image.png"), allowed)


def test_exclude_patterns_match_path_segments():
    patterns = parse_exclude_patterns(".git,node_modules,dist")
    assert is_excluded_path(Path("node_modules/pkg/a.txt"), patterns)
    assert not is_excluded_path(Path("docs/readme.md"), patterns)
