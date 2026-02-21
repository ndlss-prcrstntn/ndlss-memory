#!/usr/bin/env sh
set -eu

if [ -z "${INDEX_MODE:-}" ]; then
  export INDEX_MODE="full-scan"
fi

if [ -z "${INDEX_FILE_TYPES:-}" ]; then
  export INDEX_FILE_TYPES=".md,.txt,.json,.yml,.yaml"
fi

if [ -z "${INDEX_EXCLUDE_PATTERNS:-}" ]; then
  export INDEX_EXCLUDE_PATTERNS=".git,node_modules,dist,build"
fi

if [ -z "${INDEX_MAX_FILE_SIZE_BYTES:-}" ]; then
  export INDEX_MAX_FILE_SIZE_BYTES="1048576"
fi

if [ -z "${INDEX_PROGRESS_INTERVAL_SECONDS:-}" ]; then
  export INDEX_PROGRESS_INTERVAL_SECONDS="15"
fi

/app/scripts/validate-config.sh

touch /tmp/indexer_ready

echo "file-indexer started in mode: ${INDEX_MODE}"
echo "file-indexer watching workspace: ${WORKSPACE_PATH:-/workspace}"

if [ "${INDEX_MODE}" = "full-scan" ]; then
  /app/scripts/full-scan-worker.sh &
fi

while true; do
  date -u +"%Y-%m-%dT%H:%M:%SZ file-indexer heartbeat mode=${INDEX_MODE}"
  sleep 30
done
