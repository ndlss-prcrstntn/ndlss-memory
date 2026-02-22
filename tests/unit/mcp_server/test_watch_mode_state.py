from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from watch_mode_coalescer import coalesce_events  # noqa: E402
from watch_mode_models import IncrementalIndexResult, WatchEvent  # noqa: E402
from watch_mode_state import WatchModeState  # noqa: E402


def test_watch_state_queue_lifecycle():
    state = WatchModeState()
    state.start("/workspace")
    state.set_state("running")

    added = state.enqueue_events(
        [
            WatchEvent(event_type="created", path="docs/a.md"),
            WatchEvent(event_type="updated", path="docs/b.md"),
        ]
    )
    assert added == 2

    status = state.get_status()
    assert status["state"] == "running"
    assert status["queueDepth"] == 2

    batch = state.dequeue_events(10)
    assert len(batch) == 2
    state.mark_processed(processed=2, failed=1)
    state.set_state("recovering")

    status = state.get_status()
    assert status["queueDepth"] == 0
    assert status["processedEvents"] == 2
    assert status["failedEvents"] == 1
    assert status["state"] == "recovering"


def test_coalescer_prioritizes_delete_and_deduplicates_paths():
    events = [
        WatchEvent(event_type="created", path="docs/a.md"),
        WatchEvent(event_type="updated", path="docs/a.md"),
        WatchEvent(event_type="deleted", path="docs/a.md"),
        WatchEvent(event_type="renamed", path="docs/new.md", old_path="docs/old.md"),
    ]

    coalesced = coalesce_events(events)
    by_path = {item.path: item for item in coalesced}

    assert by_path["docs/a.md"].event_type == "deleted"
    assert by_path["docs/old.md"].event_type == "deleted"
    assert by_path["docs/new.md"].event_type == "updated"
    assert all(item.coalesced_at for item in coalesced)


def test_incremental_index_result_sets_partial_status_with_failures():
    summary = IncrementalIndexResult(
        affected_files=["docs/a.md"],
        indexed_files=1,
        deleted_records=0,
        skipped_files=0,
        failed_files=1,
        reason_breakdown={"UPSERT_FAILED": 1},
    )

    payload = summary.to_payload()

    assert payload["status"] == "partial"
    assert payload["failedFiles"] == 1
    assert payload["reasonBreakdown"][0]["code"] == "UPSERT_FAILED"
