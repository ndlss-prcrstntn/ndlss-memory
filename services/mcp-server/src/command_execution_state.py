from __future__ import annotations

from threading import Lock

from command_execution_models import CommandExecutionResult


class CommandExecutionState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._results: dict[str, CommandExecutionResult] = {}

    def save_result(self, result: CommandExecutionResult) -> None:
        with self._lock:
            self._results[result.request_id] = result

    def get_result(self, request_id: str) -> CommandExecutionResult | None:
        with self._lock:
            return self._results.get(request_id)


STATE = CommandExecutionState()

