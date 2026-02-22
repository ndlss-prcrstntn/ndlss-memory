from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from bootstrap_state import (  # noqa: E402
    BootstrapRuntimeSnapshot,
    BootstrapStateRecord,
    BootstrapRuntimeState,
    build_workspace_key,
)


def test_workspace_key_is_stable_and_normalized():
    key1 = build_workspace_key("C:\\Repo\\Project")
    key2 = build_workspace_key("c:/repo/project")
    assert key1 == key2
    assert "|" in key1


def test_bootstrap_state_record_payload_roundtrip():
    record = BootstrapStateRecord(
        workspace_key="workspace|abc",
        collection_name="workspace_chunks",
        status="running",
        attempt=2,
        last_run_id="run-1",
        created_collection=True,
    )
    payload = record.to_payload()
    restored = BootstrapStateRecord.from_payload(payload)
    assert restored.workspace_key == record.workspace_key
    assert restored.collection_name == record.collection_name
    assert restored.status == record.status
    assert restored.attempt == 2
    assert restored.last_run_id == "run-1"
    assert restored.created_collection is True


def test_runtime_state_bind_and_lookup():
    runtime = BootstrapRuntimeState()
    snapshot = BootstrapRuntimeSnapshot(
        workspace_key="workspace|abc",
        trigger="auto-startup",
        decision="run",
        status="running",
        run_id="run-123",
    )
    runtime.set_snapshot(snapshot)
    assert runtime.workspace_for_run("run-123") == "workspace|abc"
    assert runtime.get_snapshot("workspace|abc") is not None
