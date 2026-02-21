from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from command_audit_store import CommandAuditStore
from command_execution_models import CommandAuditRecord


def test_audit_store_appends_and_lists_records(tmp_path: Path):
    audit_path = tmp_path / "audit.log"
    store = CommandAuditStore(audit_log_path=str(audit_path), retention_days=7)

    store.append(
        CommandAuditRecord(
            request_id="req-1",
            timestamp="2026-02-21T10:00:00+00:00",
            command="pwd",
            args=(),
            working_directory="/workspace",
            status="ok",
            error_code=None,
            policy_snapshot={"timeoutSeconds": 20},
        )
    )
    store.append(
        CommandAuditRecord(
            request_id="req-2",
            timestamp="2026-02-21T10:01:00+00:00",
            command="rm",
            args=("-rf", "/"),
            working_directory="/workspace",
            status="rejected",
            error_code="COMMAND_NOT_ALLOWED",
            policy_snapshot={"timeoutSeconds": 20},
        )
    )

    records = store.list_records(limit=10)
    assert len(records) == 2
    assert records[0]["requestId"] == "req-2"

    rejected = store.list_records(limit=10, status="rejected")
    assert len(rejected) == 1
    assert rejected[0]["errorCode"] == "COMMAND_NOT_ALLOWED"


def test_audit_store_prunes_records_older_than_retention(tmp_path: Path):
    audit_path = tmp_path / "audit-retention.log"
    store = CommandAuditStore(audit_log_path=str(audit_path), retention_days=1)
    audit_path.write_text(
        "\n".join(
            [
                '{"auditId":"a1","requestId":"old","timestamp":"2000-01-01T00:00:00+00:00","command":"pwd","status":"ok"}',
                '{"auditId":"a2","requestId":"new","timestamp":"2999-01-01T00:00:00+00:00","command":"pwd","status":"ok"}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    records = store.list_records(limit=10)
    assert len(records) == 1
    assert records[0]["requestId"] == "new"
