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

/app/scripts/validate-config.sh

touch /tmp/indexer_ready

echo "file-indexer started in mode: ${INDEX_MODE}"
echo "file-indexer watching workspace: ${WORKSPACE_PATH:-/workspace}"

while true; do
  date -u +"%Y-%m-%dT%H:%M:%SZ file-indexer heartbeat mode=${INDEX_MODE}"
  sleep 30
done
