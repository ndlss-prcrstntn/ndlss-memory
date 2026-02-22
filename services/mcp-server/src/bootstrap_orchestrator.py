from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Callable

from bootstrap_collection_service import BootstrapCollectionService, BootstrapCollectionServiceError
from bootstrap_state import (
    RUNTIME_STATE,
    BootstrapRuntimeSnapshot,
    BootstrapStateRecord,
    build_workspace_key,
)
from bootstrap_state_repository import BootstrapStateRepository, BootstrapStateRepositoryError


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _env_flag(name: str, default: str = "1") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class BootstrapDecision:
    trigger: str
    decision: str
    status: str
    workspace_key: str
    run_id: str | None = None
    reason: str | None = None
    error_code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "trigger": self.trigger,
            "decision": self.decision,
            "status": self.status,
            "workspaceKey": self.workspace_key,
            "checkedAt": _now_iso(),
        }
        if self.run_id:
            payload["runId"] = self.run_id
        if self.reason:
            payload["reason"] = self.reason
        if self.error_code:
            payload["errorCode"] = self.error_code
        return payload


class BootstrapOrchestrator:
    def __init__(
        self,
        *,
        state_repository: BootstrapStateRepository | None = None,
        collection_service: BootstrapCollectionService | None = None,
    ) -> None:
        self._state_repository = state_repository or BootstrapStateRepository.from_env()
        self._collection_service = collection_service or BootstrapCollectionService.from_env()
        self._startup_lock = Lock()

    def evaluate_startup(
        self,
        *,
        workspace_path: str,
        start_ingestion_run: Callable[[str], str],
    ) -> BootstrapDecision:
        with self._startup_lock:
            workspace_key = build_workspace_key(workspace_path)
            trigger = "auto-startup"

            if not _env_flag("BOOTSTRAP_AUTO_INGEST_ON_START", "1"):
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="skip-already-completed",
                    status="skipped",
                    workspace_key=workspace_key,
                    reason="BOOTSTRAP_AUTO_INGEST_ON_START is disabled",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-skipped", decision)
                return decision

            try:
                existing = self._state_repository.get(workspace_key)
            except BootstrapStateRepositoryError as exc:
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="retry-failed",
                    status="failed",
                    workspace_key=workspace_key,
                    reason=str(exc),
                    error_code="BOOTSTRAP_STATE_UNAVAILABLE",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-failed", decision)
                return decision

            retry_failed = _env_flag("BOOTSTRAP_RETRY_FAILED_ON_START", "1")
            if existing and existing.status == "completed":
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="skip-already-completed",
                    status="ready",
                    workspace_key=workspace_key,
                    run_id=existing.last_run_id,
                    reason="bootstrap already completed for workspace",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-skipped", decision)
                return decision
            if existing and existing.status == "running":
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="skip-already-completed",
                    status="running",
                    workspace_key=workspace_key,
                    run_id=existing.last_run_id,
                    reason="bootstrap is already running",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-skipped", decision)
                return decision
            if existing and existing.status == "failed" and not retry_failed:
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="skip-already-completed",
                    status="failed",
                    workspace_key=workspace_key,
                    run_id=existing.last_run_id,
                    reason="failed bootstrap retry is disabled",
                    error_code=existing.error_code or "BOOTSTRAP_RETRY_DISABLED",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-skipped", decision)
                return decision

            created_collection = False
            try:
                created_collection = self._collection_service.ensure_collection_exists()
            except BootstrapCollectionServiceError as exc:
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="retry-failed",
                    status="failed",
                    workspace_key=workspace_key,
                    reason=str(exc),
                    error_code="BOOTSTRAP_COLLECTION_UNAVAILABLE",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-failed", decision)
                return decision

            try:
                run_id = start_ingestion_run(workspace_path)
            except RuntimeError as exc:
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="retry-failed",
                    status="failed",
                    workspace_key=workspace_key,
                    reason=str(exc),
                    error_code="BOOTSTRAP_INGESTION_START_FAILED",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-failed", decision)
                return decision

            attempt = 1 if existing is None else existing.attempt + 1
            record = BootstrapStateRecord(
                workspace_key=workspace_key,
                collection_name=self._collection_service.collection_name,
                status="running",
                trigger=trigger,
                attempt=attempt,
                last_run_id=run_id,
                started_at=_now_iso(),
                created_collection=created_collection,
                point_count_after_run=0,
            )
            try:
                self._state_repository.upsert(record)
            except BootstrapStateRepositoryError as exc:
                decision = BootstrapDecision(
                    trigger=trigger,
                    decision="retry-failed",
                    status="failed",
                    workspace_key=workspace_key,
                    run_id=run_id,
                    reason=str(exc),
                    error_code="BOOTSTRAP_STATE_UNAVAILABLE",
                )
                self._set_runtime_snapshot(decision)
                self._emit_event("bootstrap-failed", decision)
                return decision
            decision = BootstrapDecision(
                trigger=trigger,
                decision="run",
                status="running",
                workspace_key=workspace_key,
                run_id=run_id,
                reason="auto bootstrap started",
            )
            self._set_runtime_snapshot(decision)
            RUNTIME_STATE.bind_run(run_id, workspace_key)
            self._emit_event("bootstrap-started", decision)
            return decision

    def on_ingestion_finished(
        self,
        *,
        run_id: str,
        workspace_path: str,
        status: str,
        error_code: str | None,
        error_message: str | None,
    ) -> None:
        workspace_key = RUNTIME_STATE.workspace_for_run(run_id) or build_workspace_key(workspace_path)
        try:
            existing = self._state_repository.get(workspace_key)
        except BootstrapStateRepositoryError:
            return
        if existing is None:
            return

        points = 0
        try:
            points = self._collection_service.point_count()
        except BootstrapCollectionServiceError:
            points = 0

        final_status = "completed" if status == "completed" and points > 0 else "failed"
        record = BootstrapStateRecord(
            workspace_key=workspace_key,
            collection_name=existing.collection_name,
            status=final_status,
            trigger=existing.trigger,
            attempt=existing.attempt,
            last_run_id=run_id,
            started_at=existing.started_at,
            finished_at=_now_iso(),
            error_code=error_code if final_status == "failed" else None,
            error_message=error_message if final_status == "failed" else None,
            created_collection=existing.created_collection,
            point_count_after_run=points,
        )
        try:
            self._state_repository.upsert(record)
        except BootstrapStateRepositoryError:
            return

        decision = BootstrapDecision(
            trigger=record.trigger,
            decision="run" if final_status == "completed" else "retry-failed",
            status="ready" if final_status == "completed" else "failed",
            workspace_key=workspace_key,
            run_id=run_id,
            reason="bootstrap completed" if final_status == "completed" else (error_message or "bootstrap failed"),
            error_code=error_code if final_status == "failed" else None,
        )
        self._set_runtime_snapshot(decision)
        self._emit_event("bootstrap-finished", decision)

    def get_bootstrap_payload(self, workspace_path: str) -> dict[str, Any]:
        workspace_key = build_workspace_key(workspace_path)
        snapshot = RUNTIME_STATE.get_snapshot(workspace_key)
        if snapshot is not None:
            return snapshot.to_dict()
        try:
            existing = self._state_repository.get(workspace_key)
        except BootstrapStateRepositoryError as exc:
            return {
                "trigger": "auto-startup",
                "decision": "retry-failed",
                "status": "failed",
                "workspaceKey": workspace_key,
                "reason": str(exc),
                "errorCode": "BOOTSTRAP_STATE_UNAVAILABLE",
                "checkedAt": _now_iso(),
            }
        if existing is None:
            return {
                "trigger": "auto-startup",
                "decision": "skip-already-completed",
                "status": "skipped",
                "workspaceKey": workspace_key,
                "reason": "bootstrap decision is not available yet",
                "checkedAt": _now_iso(),
            }
        status_map = {
            "completed": "ready",
            "running": "running",
            "failed": "failed",
            "pending": "running",
            "skipped": "skipped",
        }
        decision = "retry-failed" if existing.status == "failed" else "skip-already-completed"
        payload: dict[str, Any] = {
            "trigger": existing.trigger,
            "decision": decision,
            "status": status_map.get(existing.status, "skipped"),
            "workspaceKey": existing.workspace_key,
            "checkedAt": _now_iso(),
            "collectionName": existing.collection_name,
        }
        if existing.last_run_id:
            payload["runId"] = existing.last_run_id
        if existing.error_message:
            payload["reason"] = existing.error_message
        if existing.error_code:
            payload["errorCode"] = existing.error_code
        return payload

    def get_collection_payload(self) -> dict[str, Any]:
        checked_at = _now_iso()
        try:
            snapshot = self._collection_service.snapshot(checked_at=checked_at)
            return snapshot.to_dict()
        except BootstrapCollectionServiceError:
            return {
                "collectionName": self._collection_service.collection_name,
                "exists": False,
                "pointCount": 0,
                "checkedAt": checked_at,
            }

    def _set_runtime_snapshot(self, decision: BootstrapDecision) -> None:
        RUNTIME_STATE.set_snapshot(
            BootstrapRuntimeSnapshot(
                workspace_key=decision.workspace_key,
                trigger=decision.trigger,
                decision=decision.decision,
                status=decision.status,
                reason=decision.reason,
                error_code=decision.error_code,
                run_id=decision.run_id,
                collection_name=self._collection_service.collection_name,
            )
        )

    @staticmethod
    def _emit_event(event: str, decision: BootstrapDecision) -> None:
        print(
            json.dumps(
                {
                    "event": event,
                    "bootstrap": decision.to_dict(),
                },
                ensure_ascii=False,
            )
        )
