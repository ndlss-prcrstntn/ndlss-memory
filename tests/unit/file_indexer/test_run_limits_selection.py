from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

from full_scan_service import run_full_scan
from full_scan_walker import walk_files, walk_files_pruned


def _skip_map(summary: dict) -> dict[str, int]:
    return {item["code"]: int(item["count"]) for item in summary["skipBreakdown"]}


def test_walk_files_is_sorted_by_relative_path(tmp_path: Path):
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "c.md").write_text("c", encoding="utf-8")

    files = walk_files(str(tmp_path))
    rel = [str(path.relative_to(tmp_path)).replace("\\", "/") for path in files]
    assert rel == ["a.md", "b.md", "nested/c.md"]


def test_walk_files_pruned_skips_excluded_directories(tmp_path: Path):
    (tmp_path / "keep").mkdir()
    (tmp_path / "keep" / "ok.md").write_text("ok", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "pkg.js").write_text("skip", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "node_modules").mkdir()
    (tmp_path / "src" / "node_modules" / "deep.js").write_text("skip", encoding="utf-8")

    files = walk_files_pruned(str(tmp_path), exclude_patterns=["node_modules"])
    rel = [str(path.relative_to(tmp_path)).replace("\\", "/") for path in files]

    assert rel == ["keep/ok.md"]


def test_run_full_scan_respects_depth_and_max_files_limits(tmp_path: Path):
    (tmp_path / "a.md").write_text("a", encoding="utf-8")
    (tmp_path / "b.md").write_text("b", encoding="utf-8")
    (tmp_path / "deep").mkdir()
    (tmp_path / "deep" / "c.md").write_text("c", encoding="utf-8")
    (tmp_path / "deep" / "deeper").mkdir()
    (tmp_path / "deep" / "deeper" / "d.md").write_text("d", encoding="utf-8")

    summary = run_full_scan(
        workspace_path=str(tmp_path),
        file_types_csv=".md",
        exclude_patterns_csv="",
        max_file_size_bytes=1024,
        max_traversal_depth=1,
        max_files_per_run=2,
        progress_interval_seconds=60,
    )

    assert summary["processedCount"] == 4
    assert summary["indexedCount"] == 2
    assert summary["appliedLimits"] == {"maxTraversalDepth": 1, "maxFilesPerRun": 2}

    skip_map = _skip_map(summary)
    assert skip_map["LIMIT_DEPTH_EXCEEDED"] == 1
    assert skip_map["LIMIT_MAX_FILES_REACHED"] == 1
