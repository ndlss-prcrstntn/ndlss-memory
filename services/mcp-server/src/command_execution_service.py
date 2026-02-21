from __future__ import annotations

from uuid import uuid4

from command_audit_store import CommandAuditStore
from command_execution_errors import command_not_allowed, invalid_request, request_not_found
from command_execution_models import (
    CommandAuditRecord,
    CommandExecutionRequest,
    CommandExecutionResult,
    now_iso,
)
from command_execution_state import CommandExecutionState
from command_process_runner import CommandProcessRunner
from command_security_policy import CommandSecurityPolicy
from command_workspace_guard import resolve_workspace_directory


class CommandExecutionService:
    def __init__(
        self,
        *,
        policy: CommandSecurityPolicy,
        state: CommandExecutionState,
        runner: CommandProcessRunner,
        audit_store: CommandAuditStore,
    ) -> None:
        self._policy = policy
        self._state = state
        self._runner = runner
        self._audit_store = audit_store

    def execute(self, request: CommandExecutionRequest) -> CommandExecutionResult:
        if not self._policy.allows(request.command):
            raise command_not_allowed(request.command)

        working_dir = resolve_workspace_directory(
            workspace_root=self._policy.workspace_root,
            requested_working_directory=request.working_directory,
        )

        request_timeout = request.timeout_seconds or self._policy.timeout_seconds
        timeout_seconds = min(max(1, request_timeout), self._policy.timeout_seconds)

        outcome = self._runner.run(
            command=request.command,
            args=request.args,
            working_directory=str(working_dir),
            timeout_seconds=timeout_seconds,
        )
        request_id = uuid4().hex
        result = CommandExecutionResult(
            request_id=request_id,
            status=outcome.status,
            started_at=outcome.started_at,
            finished_at=outcome.finished_at,
            duration_ms=outcome.duration_ms,
            command=request.command,
            args=request.args,
            working_directory=str(working_dir),
            exit_code=outcome.exit_code,
            stdout=outcome.stdout,
            stderr=outcome.stderr,
            error_code=outcome.error_code,
            error_message=outcome.error_message,
        )
        self._state.save_result(result)
        self._audit_store.append(
            CommandAuditRecord(
                request_id=request_id,
                timestamp=now_iso(),
                command=request.command,
                args=request.args,
                working_directory=str(working_dir),
                status=result.status,
                error_code=result.error_code,
                policy_snapshot={
                    "timeoutSeconds": self._policy.timeout_seconds,
                    "cpuTimeLimitSeconds": self._policy.cpu_time_limit_seconds,
                    "memoryLimitBytes": self._policy.memory_limit_bytes,
                    "workspaceRoot": self._policy.workspace_root,
                },
            )
        )
        return result

    def get_result(self, request_id: str) -> CommandExecutionResult:
        normalized = str(request_id).strip()
        if not normalized:
            raise invalid_request("requestId must not be empty")
        result = self._state.get_result(normalized)
        if result is None:
            raise request_not_found(normalized)
        return result

    def list_audit(self, *, limit: int, status: str | None) -> dict:
        safe_limit = max(1, min(limit, 200))
        if status and status not in {"ok", "rejected", "timeout", "failed"}:
            raise invalid_request("status must be one of: ok, rejected, timeout, failed")
        records = self._audit_store.list_records(limit=safe_limit, status=status)
        return {
            "status": "ok",
            "records": records,
            "meta": {"count": len(records), "returnedAt": now_iso()},
        }
