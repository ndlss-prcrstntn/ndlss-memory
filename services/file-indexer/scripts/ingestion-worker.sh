#!/usr/bin/env sh
set -eu

WORKSPACE="${WORKSPACE_PATH:-/workspace}"

if ! command -v python >/dev/null 2>&1; then
  echo "ingestion-worker skipped: python binary is not available in file-indexer container"
  exit 0
fi

python - <<'PY'
from pathlib import Path
import json
import os
import sys

sys.path.insert(0, "/app/src")
from ingestion_pipeline.ingestion_service import run_ingestion_pipeline
from delta_after_commit.delta_after_commit_service import run_delta_after_commit_pipeline

workspace = os.getenv("WORKSPACE_PATH", "/workspace")
if not Path(workspace).exists():
    print(f"ingestion-worker skipped: workspace does not exist ({workspace})")
    raise SystemExit(0)

index_mode = os.getenv("INDEX_MODE", "full-scan")
if index_mode == "delta-after-commit":
    summary = run_delta_after_commit_pipeline(
        run_id=os.getenv("DELTA_BOOTSTRAP_RUN_ID", "delta-bootstrap"),
        workspace_path=workspace,
        base_ref=os.getenv("DELTA_GIT_BASE_REF", "HEAD~1"),
        target_ref=os.getenv("DELTA_GIT_TARGET_REF", "HEAD"),
    )
    payload = summary.to_dict()
    print(json.dumps({"event": "delta-bootstrap-finished", "summary": payload}, ensure_ascii=False))
else:
    summary = run_ingestion_pipeline(workspace)
    print(json.dumps({"event": "ingestion-bootstrap-finished", "summary": summary.to_dict()}, ensure_ascii=False))
PY
