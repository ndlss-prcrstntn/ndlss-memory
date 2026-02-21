from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _split_csv(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class CommandSecurityPolicy:
    allowlist: tuple[str, ...]
    timeout_seconds: int
    workspace_root: str
    run_as_non_root: bool
    cpu_time_limit_seconds: int
    memory_limit_bytes: int | None
    audit_log_path: str
    audit_retention_days: int

    def allows(self, command: str) -> bool:
        normalized = command.strip()
        return normalized in self.allowlist

    @property
    def workspace_root_path(self) -> Path:
        return Path(self.workspace_root).resolve()


def load_command_security_policy(*, security_policy: dict | None = None) -> CommandSecurityPolicy:
    security_policy = security_policy or {}
    cfg_allowlist = security_policy.get("command_allowlist", [])
    env_allowlist = os.getenv("COMMAND_ALLOWLIST", "")
    allowlist = tuple(_split_csv(env_allowlist) if env_allowlist else [str(item).strip() for item in cfg_allowlist if str(item).strip()])

    cfg_timeout = int(security_policy.get("command_timeout_seconds", 20))
    timeout_seconds = max(1, _parse_int_env("COMMAND_TIMEOUT_SECONDS", cfg_timeout))

    isolation_cfg = security_policy.get("isolation", {}) if isinstance(security_policy.get("isolation", {}), dict) else {}
    run_as_non_root = _parse_bool_env("COMMAND_RUN_AS_NON_ROOT", bool(isolation_cfg.get("run_as_non_root", True)))
    workspace_root = os.getenv("WORKSPACE_PATH", "/workspace")

    limits_cfg = security_policy.get("limits", {}) if isinstance(security_policy.get("limits", {}), dict) else {}
    cpu_time_limit_seconds = max(
        1,
        _parse_int_env("COMMAND_CPU_TIME_LIMIT_SECONDS", int(limits_cfg.get("cpu_time_limit_seconds", timeout_seconds))),
    )
    memory_limit_bytes_raw = _parse_int_env("COMMAND_MEMORY_LIMIT_BYTES", int(limits_cfg.get("memory_limit_bytes", 0)))
    memory_limit_bytes = memory_limit_bytes_raw if memory_limit_bytes_raw > 0 else None

    audit_log_path = os.getenv("COMMAND_AUDIT_LOG_PATH", "/tmp/mcp-command-audit.log")
    audit_cfg = security_policy.get("audit", {}) if isinstance(security_policy.get("audit", {}), dict) else {}
    audit_retention_days = max(1, _parse_int_env("COMMAND_AUDIT_RETENTION_DAYS", int(audit_cfg.get("retention_days", 7))))

    return CommandSecurityPolicy(
        allowlist=allowlist,
        timeout_seconds=timeout_seconds,
        workspace_root=workspace_root,
        run_as_non_root=run_as_non_root,
        cpu_time_limit_seconds=cpu_time_limit_seconds,
        memory_limit_bytes=memory_limit_bytes,
        audit_log_path=audit_log_path,
        audit_retention_days=audit_retention_days,
    )
