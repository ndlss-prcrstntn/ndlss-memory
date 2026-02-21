from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from command_audit_store import CommandAuditStore
from command_execution_errors import CommandExecutionError
from command_execution_models import CommandExecutionRequest
from command_execution_service import CommandExecutionService
from command_execution_state import CommandExecutionState
from command_process_runner import ProcessRunOutcome
from command_security_policy import CommandSecurityPolicy


class _RunnerStub:
    def __init__(self, outcome: ProcessRunOutcome):
        self.outcome = outcome
        self.calls = []

    def run(self, *, command, args, working_directory, timeout_seconds):
        self.calls.append(
            {
                "command": command,
                "args": args,
                "working_directory": working_directory,
                "timeout_seconds": timeout_seconds,
            }
        )
        return self.outcome


def _policy(audit_log_path: Path) -> CommandSecurityPolicy:
    return CommandSecurityPolicy(
        allowlist=("pwd", "sleep", "echo"),
        timeout_seconds=5,
        workspace_root="/workspace",
        run_as_non_root=True,
        cpu_time_limit_seconds=5,
        memory_limit_bytes=268435456,
        audit_log_path=str(audit_log_path),
        audit_retention_days=7,
    )


def test_command_outside_allowlist_is_rejected(tmp_path: Path):
    policy = _policy(tmp_path / "audit.log")
    runner = _RunnerStub(
        ProcessRunOutcome(
            status="ok",
            started_at="2026-02-21T10:00:00Z",
            finished_at="2026-02-21T10:00:01Z",
            duration_ms=100,
            exit_code=0,
            stdout="ok",
        )
    )
    service = CommandExecutionService(
        policy=policy,
        state=CommandExecutionState(),
        runner=runner,
        audit_store=CommandAuditStore(audit_log_path=str(tmp_path / "audit.log"), retention_days=7),
    )

    with pytest.raises(CommandExecutionError) as exc:
        service.execute(
            CommandExecutionRequest.from_payload(
                {"command": "rm", "args": ["-rf", "/"], "workingDirectory": "/workspace"}
            )
        )

    assert exc.value.code == "COMMAND_NOT_ALLOWED"
    assert runner.calls == []


def test_timeout_result_is_returned_and_persisted(tmp_path: Path):
    policy = _policy(tmp_path / "audit.log")
    runner = _RunnerStub(
        ProcessRunOutcome(
            status="timeout",
            started_at="2026-02-21T10:00:00Z",
            finished_at="2026-02-21T10:00:02Z",
            duration_ms=2000,
            exit_code=-9,
            stdout="",
            stderr="",
            error_code="COMMAND_TIMEOUT",
            error_message="Command exceeded timeout limit",
        )
    )
    state = CommandExecutionState()
    service = CommandExecutionService(
        policy=policy,
        state=state,
        runner=runner,
        audit_store=CommandAuditStore(audit_log_path=str(tmp_path / "audit.log"), retention_days=7),
    )

    result = service.execute(
        CommandExecutionRequest.from_payload(
            {"command": "sleep", "args": ["30"], "workingDirectory": "/workspace", "timeoutSeconds": 10}
        )
    )

    assert result.status == "timeout"
    assert result.error_code == "COMMAND_TIMEOUT"
    assert runner.calls[0]["timeout_seconds"] == 5
    assert state.get_result(result.request_id) is not None
