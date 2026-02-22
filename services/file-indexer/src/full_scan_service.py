from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from file_type_filter import is_supported_file, parse_supported_types
from file_size_guard import is_file_too_large
from full_scan_walker import path_depth, walk_files
from path_exclude_filter import is_excluded_path, parse_exclude_patterns
from progress_reporter import ProgressReporter
from skip_reasons import (
    EMPTY_FILE,
    EXCLUDED_BY_PATTERN,
    FILE_TOO_LARGE,
    LIMIT_DEPTH_EXCEEDED,
    LIMIT_MAX_FILES_REACHED,
    READ_ERROR,
    UNSUPPORTED_TYPE,
)


def run_full_scan(
    workspace_path: str,
    file_types_csv: str,
    exclude_patterns_csv: str,
    max_file_size_bytes: int,
    max_traversal_depth: int | None = None,
    max_files_per_run: int | None = None,
    progress_interval_seconds: int = 15,
) -> dict[str, Any]:
    supported_types = parse_supported_types(file_types_csv)
    exclude_patterns = parse_exclude_patterns(exclude_patterns_csv)
    files = walk_files(workspace_path)
    reporter = ProgressReporter(progress_interval_seconds)

    processed = 0
    indexed = 0
    skipped = 0
    errors = 0
    skip_breakdown: dict[str, int] = defaultdict(int)

    root = Path(workspace_path)
    selected_files = 0
    for path in files:
        try:
            processed += 1
            rel = path.relative_to(root) if root in path.parents or path == root else path
            depth = path_depth(root, path)

            if max_traversal_depth is not None and depth > max_traversal_depth:
                skipped += 1
                skip_breakdown[LIMIT_DEPTH_EXCEEDED] += 1
                continue

            if is_excluded_path(rel, exclude_patterns):
                skipped += 1
                skip_breakdown[EXCLUDED_BY_PATTERN] += 1
                continue

            if not is_supported_file(path, supported_types):
                skipped += 1
                skip_breakdown[UNSUPPORTED_TYPE] += 1
                continue

            too_large, size = is_file_too_large(path, max_file_size_bytes)
            if size < 0:
                skipped += 1
                errors += 1
                skip_breakdown[READ_ERROR] += 1
                continue

            if size == 0:
                skipped += 1
                skip_breakdown[EMPTY_FILE] += 1
                continue

            if too_large:
                skipped += 1
                skip_breakdown[FILE_TOO_LARGE] += 1
                continue

            if max_files_per_run is not None and selected_files >= max_files_per_run:
                skipped += 1
                skip_breakdown[LIMIT_MAX_FILES_REACHED] += 1
                continue

            path.read_bytes()
            indexed += 1
            selected_files += 1
        except OSError:
            skipped += 1
            errors += 1
            skip_breakdown[READ_ERROR] += 1
        finally:
            reporter.emit(
                {
                    "processedCount": processed,
                    "indexedCount": indexed,
                    "skipCount": skipped,
                    "errorCount": errors,
                }
            )

    summary = {
        "processedCount": processed,
        "indexedCount": indexed,
        "skipCount": skipped,
        "errorCount": errors,
        "appliedLimits": {
            "maxTraversalDepth": max_traversal_depth,
            "maxFilesPerRun": max_files_per_run,
        },
        "skipBreakdown": [{"code": code, "count": count} for code, count in sorted(skip_breakdown.items())],
    }
    reporter.force_emit({"status": "completed", **summary})
    return summary
