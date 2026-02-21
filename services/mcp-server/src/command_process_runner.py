from __future__ import annotations

import os
import signal
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter

try:
    import resource
except ImportError:  # pragma: no cover - unavailable on Windows
    resource = None  # type: ignore[assignment]


@dataclass(frozen=True)
class ProcessRunOutcome:
    status: str
    started_at: str
    finished_at: str
    duration_ms: int
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    error_code: str | None = None
    error_message: str | None = None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _make_limits_preexec(*, cpu_time_limit_seconds: int, memory_limit_bytes: int | None):
    if resource is None:
        return None

    def _apply_limits() -> None:
        if cpu_time_limit_seconds > 0:
            resource.setrlimit(resource.RLIMIT_CPU, (cpu_time_limit_seconds, cpu_time_limit_seconds))
        if memory_limit_bytes and memory_limit_bytes > 0:
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

    return _apply_limits


class CommandProcessRunner:
    def __init__(self, *, cpu_time_limit_seconds: int, memory_limit_bytes: int | None) -> None:
        self._cpu_time_limit_seconds = cpu_time_limit_seconds
        self._memory_limit_bytes = memory_limit_bytes

    def run(
        self,
        *,
        command: str,
        args: tuple[str, ...],
        working_directory: str,
        timeout_seconds: int,
    ) -> ProcessRunOutcome:
        started_at = _now_iso()
        started_perf = perf_counter()
        cmd = [command, *args]
        preexec = _make_limits_preexec(
            cpu_time_limit_seconds=self._cpu_time_limit_seconds,
            memory_limit_bytes=self._memory_limit_bytes,
        )

        proc = subprocess.Popen(
            cmd,
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
            preexec_fn=preexec if os.name != "nt" else None,
        )

        try:
            stdout, stderr = proc.communicate(timeout=timeout_seconds)
            duration_ms = int((perf_counter() - started_perf) * 1000)
            status = "ok" if proc.returncode == 0 else "failed"
            error_code = None if status == "ok" else "COMMAND_EXIT_NON_ZERO"
            error_message = None if status == "ok" else f"Command exited with code {proc.returncode}"
            return ProcessRunOutcome(
                status=status,
                started_at=started_at,
                finished_at=_now_iso(),
                duration_ms=duration_ms,
                exit_code=proc.returncode,
                stdout=stdout,
                stderr=stderr,
                error_code=error_code,
                error_message=error_message,
            )
        except subprocess.TimeoutExpired:
            self._terminate_process_tree(proc)
            stdout, stderr = proc.communicate()
            duration_ms = int((perf_counter() - started_perf) * 1000)
            return ProcessRunOutcome(
                status="timeout",
                started_at=started_at,
                finished_at=_now_iso(),
                duration_ms=duration_ms,
                exit_code=proc.returncode,
                stdout=stdout,
                stderr=stderr,
                error_code="COMMAND_TIMEOUT",
                error_message="Command exceeded timeout limit",
            )

    @staticmethod
    def _terminate_process_tree(proc: subprocess.Popen[str]) -> None:
        try:
            if os.name != "nt":
                os.killpg(proc.pid, signal.SIGKILL)
            else:  # pragma: no cover - fallback for Windows
                proc.kill()
        except ProcessLookupError:
            pass
        except OSError:
            proc.kill()

