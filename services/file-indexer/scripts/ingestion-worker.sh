#!/usr/bin/env sh
set -eu

WORKSPACE="${WORKSPACE_PATH:-/workspace}"

python - <<'PY'
from pathlib import Path
import json
import os
import sys

sys.path.insert(0, "/app/src")
from ingestion_pipeline.ingestion_service import run_ingestion_pipeline

workspace = os.getenv("WORKSPACE_PATH", "/workspace")
if not Path(workspace).exists():
    print(f"ingestion-worker skipped: workspace does not exist ({workspace})")
    raise SystemExit(0)

summary = run_ingestion_pipeline(workspace)
print(json.dumps({"event": "ingestion-bootstrap-finished", "summary": summary.to_dict()}, ensure_ascii=False))
PY
