#!/usr/bin/env sh
set -eu

INTERVAL="${INDEX_PROGRESS_INTERVAL_SECONDS:-15}"

echo "full-scan worker started (interval=${INTERVAL}s, workspace=${WORKSPACE_PATH:-/workspace})"

while true; do
  date -u +"%Y-%m-%dT%H:%M:%SZ full-scan-worker alive"
  sleep "$INTERVAL"
done

