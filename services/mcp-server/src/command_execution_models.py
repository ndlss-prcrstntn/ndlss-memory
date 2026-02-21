from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from command_execution_errors import invalid_request


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CommandExecutionRequest:
    command: str
    args: tuple[str, ...]
    working_directory: str
    timeout_seconds: int | None = None

    @classmethod
    def from_payload(cls, payload: Any) -> "CommandExecutionRequest":
        if not isinstance(payload, dict):
            raise invalid_request("Request body must be a JSON object")

        command = str(payload.get("command", "")).strip()
        if not command:
            raise invalid_request("command must not be empty")
        if any(ch.isspace() for ch in command):
            raise invalid_request("command must be a single executable name without spaces")

        args_raw = payload.get("args", [])
        if args_raw is None:
            args_raw = []
        if not isinstance(args_raw, list):
            raise invalid_request("args must be an array of strings")
        args: list[str] = []
        for item in args_raw:
            args.append(str(item))

        working_directory = str(payload.get("workingDirectory", "")).strip()
        if not working_directory:
            raise invalid_request("workingDirectory must not be empty")

        timeout_raw = payload.get("timeoutSeconds")
        timeout_seconds: int | None = None
        if timeout_raw is not None:
            try:
                timeout_seconds = int(timeout_raw)
            except (TypeError, ValueError) as exc:
                raise invalid_request("timeoutSeconds must be an integer") from exc
            if timeout_seconds < 1:
                raise invalid_request("timeoutSeconds must be >= 1")

        return cls(
            command=command,
            args=tuple(args),
            working_directory=working_directory,
            timeout_seconds=timeout_seconds,
        )


@dataclass
class CommandExecutionResult:
    request_id: str
    status: str
    started_at: str
    finished_at: str
    duration_ms: int
    command: str
    args: tuple[str, ...]
    working_directory: str
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    error_code: str | None = None
    error_message: str | None = None

    def to_result_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"requestId": self.request_id, "status": self.status}
        if self.exit_code is not None:
            payload["exitCode"] = self.exit_code
        if self.stdout:
            payload["stdout"] = self.stdout
        if self.stderr:
            payload["stderr"] = self.stderr
        if self.error_code:
            payload["errorCode"] = self.error_code
        if self.error_message:
            payload["errorMessage"] = self.error_message
        return payload

    def to_response_envelope(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "result": self.to_result_payload(),
            "meta": {
                "requestId": self.request_id,
                "requestedAt": self.started_at,
                "finishedAt": self.finished_at,
                "durationMs": self.duration_ms,
            },
        }


@dataclass(frozen=True)
class CommandAuditRecord:
    request_id: str
    timestamp: str
    command: str
    args: tuple[str, ...]
    working_directory: str
    status: str
    error_code: str | None = None
    policy_snapshot: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "requestId": self.request_id,
            "timestamp": self.timestamp,
            "command": self.command,
            "args": list(self.args),
            "workingDirectory": self.working_directory,
            "status": self.status,
        }
        if self.error_code:
            payload["errorCode"] = self.error_code
        if self.policy_snapshot:
            payload["policy"] = self.policy_snapshot
        return payload

