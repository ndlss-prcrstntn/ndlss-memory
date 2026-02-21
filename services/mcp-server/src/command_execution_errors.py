from __future__ import annotations


class CommandExecutionError(RuntimeError):
    def __init__(self, code: str, message: str, status_code: int, details: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


def error_payload(code: str, message: str, details: str | None = None) -> dict[str, str]:
    payload = {"errorCode": code, "message": message}
    if details:
        payload["details"] = details
    return payload


def json_error(code: str, message: str, status_code: int, details: str | None = None):
    from flask import jsonify

    return jsonify(error_payload(code, message, details)), status_code


def json_error_from_exception(exc: CommandExecutionError):
    return json_error(exc.code, exc.message, exc.status_code, exc.details)


def invalid_request(message: str, details: str | None = None) -> CommandExecutionError:
    return CommandExecutionError("INVALID_REQUEST", message, 400, details)


def command_not_allowed(command: str) -> CommandExecutionError:
    return CommandExecutionError("COMMAND_NOT_ALLOWED", f"Command '{command}' is not allowed", 403)


def workspace_isolation_violation(path: str) -> CommandExecutionError:
    return CommandExecutionError(
        "WORKSPACE_ISOLATION_VIOLATION",
        f"Working directory '{path}' is outside allowed workspace",
        403,
    )


def request_not_found(request_id: str) -> CommandExecutionError:
    return CommandExecutionError("REQUEST_NOT_FOUND", f"Request '{request_id}' is not found", 404)


def process_execution_failed(message: str, details: str | None = None) -> CommandExecutionError:
    return CommandExecutionError("COMMAND_EXECUTION_FAILED", message, 500, details)

