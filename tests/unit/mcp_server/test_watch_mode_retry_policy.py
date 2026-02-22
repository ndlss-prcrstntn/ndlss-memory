from pathlib import Path
import sys
from threading import Event

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from watch_mode_watcher import PollingWorkspaceWatcher, WatchRetryPolicy  # noqa: E402


def test_retry_policy_backoff_grows_with_cap():
    policy = WatchRetryPolicy(max_attempts=5, base_delay_seconds=1.0, max_delay_seconds=4.0, jitter_ratio=0.0)

    assert policy.backoff_seconds(1) == 1.0
    assert policy.backoff_seconds(2) == 2.0
    assert policy.backoff_seconds(3) == 4.0
    assert policy.backoff_seconds(5) == 4.0


def test_retry_policy_applies_jitter_within_bounds():
    policy = WatchRetryPolicy(max_attempts=5, base_delay_seconds=2.0, max_delay_seconds=8.0, jitter_ratio=0.25)

    sample = [policy.backoff_seconds(2) for _ in range(20)]
    assert all(3.0 <= value <= 5.0 for value in sample)


def test_watch_loop_stops_after_retry_budget_exhausted(tmp_path: Path):
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True)
    (workspace / "note.md").write_text("hello", encoding="utf-8")

    watcher = PollingWorkspaceWatcher(
        workspace_path=str(workspace),
        poll_interval_seconds=1,
        max_events_per_cycle=10,
        retry_policy=WatchRetryPolicy(max_attempts=2, base_delay_seconds=0.01, max_delay_seconds=0.01, jitter_ratio=0.0),
    )

    original = watcher._scan_snapshot
    attempts = {"count": 0}

    def _always_fail():
        attempts["count"] += 1
        raise RuntimeError("boom")

    watcher._scan_snapshot = _always_fail  # type: ignore[assignment]
    stop_event = Event()
    retries: list[tuple[int, bool]] = []

    with pytest.raises(RuntimeError):
        watcher.watch_loop(
            stop_event=stop_event,
            coalesce_window_seconds=1,
            reconcile_interval_seconds=10,
            on_events=lambda _events: None,
            on_retry=lambda _exc, attempt, _delay, exhausted: retries.append((attempt, exhausted)),
        )

    watcher._scan_snapshot = original  # type: ignore[assignment]
    assert attempts["count"] >= 2
    assert retries[-1] == (2, True)
