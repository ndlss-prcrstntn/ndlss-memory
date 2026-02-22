#!/usr/bin/env sh
set -eu

if [ "${STARTUP_PREFLIGHT_ENABLED:-1}" != "1" ]; then
  echo "startup-preflight skipped: STARTUP_PREFLIGHT_ENABLED=${STARTUP_PREFLIGHT_ENABLED:-0}"
  exit 0
fi

workspace="${WORKSPACE_PATH:-/workspace}"
qdrant_host="${QDRANT_HOST:-qdrant}"
qdrant_port="${QDRANT_API_PORT:-6333}"
index_mode="${INDEX_MODE:-full-scan}"
timeout_seconds="${STARTUP_PREFLIGHT_TIMEOUT_SECONDS:-3}"
require_git_delta="${STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA:-1}"

if [ ! -d "$workspace" ]; then
  echo "{\"errorCode\":\"PREFLIGHT_WORKSPACE_NOT_FOUND\",\"message\":\"workspace directory is missing\",\"details\":{\"workspacePath\":\"$workspace\"}}"
  exit 1
fi

if [ ! -r "$workspace" ]; then
  echo "{\"errorCode\":\"PREFLIGHT_WORKSPACE_NOT_READABLE\",\"message\":\"workspace is not readable\",\"details\":{\"workspacePath\":\"$workspace\"}}"
  exit 1
fi

qdrant_url="http://${qdrant_host}:${qdrant_port}/collections"
if ! wget -q -T "$timeout_seconds" -O - "$qdrant_url" >/dev/null 2>&1; then
  echo "{\"errorCode\":\"PREFLIGHT_QDRANT_UNREACHABLE\",\"message\":\"qdrant is not reachable from file-indexer\",\"details\":{\"url\":\"$qdrant_url\"}}"
  exit 1
fi

if [ "$index_mode" = "delta-after-commit" ] && [ "$require_git_delta" = "1" ]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "{\"errorCode\":\"PREFLIGHT_GIT_NOT_AVAILABLE\",\"message\":\"git is required for delta-after-commit mode\",\"details\":{\"indexMode\":\"$index_mode\"}}"
    exit 1
  fi
fi

echo "startup-preflight passed for file-indexer"
