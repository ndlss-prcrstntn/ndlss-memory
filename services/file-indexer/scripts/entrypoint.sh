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

if [ -z "${INDEX_MAX_TRAVERSAL_DEPTH+x}" ]; then
  export INDEX_MAX_TRAVERSAL_DEPTH=""
fi

if [ -z "${INDEX_MAX_FILES_PER_RUN+x}" ]; then
  export INDEX_MAX_FILES_PER_RUN=""
fi

if [ -z "${INDEX_PROGRESS_INTERVAL_SECONDS:-}" ]; then
  export INDEX_PROGRESS_INTERVAL_SECONDS="15"
fi

if [ -z "${INGESTION_CHUNK_SIZE:-}" ]; then
  export INGESTION_CHUNK_SIZE="800"
fi

if [ -z "${INGESTION_CHUNK_OVERLAP:-}" ]; then
  export INGESTION_CHUNK_OVERLAP="120"
fi

if [ -z "${INGESTION_RETRY_MAX_ATTEMPTS:-}" ]; then
  export INGESTION_RETRY_MAX_ATTEMPTS="3"
fi

if [ -z "${INGESTION_RETRY_BACKOFF_SECONDS:-}" ]; then
  export INGESTION_RETRY_BACKOFF_SECONDS="1.0"
fi

if [ -z "${INGESTION_BOOTSTRAP_ON_START:-}" ]; then
  export INGESTION_BOOTSTRAP_ON_START="0"
fi

if [ -z "${DELTA_GIT_BASE_REF:-}" ]; then
  export DELTA_GIT_BASE_REF="HEAD~1"
fi

if [ -z "${DELTA_GIT_TARGET_REF:-}" ]; then
  export DELTA_GIT_TARGET_REF="HEAD"
fi

if [ -z "${DELTA_INCLUDE_RENAMES:-}" ]; then
  export DELTA_INCLUDE_RENAMES="1"
fi

if [ -z "${DELTA_ENABLE_FALLBACK:-}" ]; then
  export DELTA_ENABLE_FALLBACK="1"
fi

if [ -z "${DELTA_BOOTSTRAP_ON_START:-}" ]; then
  export DELTA_BOOTSTRAP_ON_START="0"
fi

if [ -z "${WATCH_POLL_INTERVAL_SECONDS:-}" ]; then
  export WATCH_POLL_INTERVAL_SECONDS="5"
fi

if [ -z "${WATCH_COALESCE_WINDOW_SECONDS:-}" ]; then
  export WATCH_COALESCE_WINDOW_SECONDS="2"
fi

if [ -z "${WATCH_RECONCILE_INTERVAL_SECONDS:-}" ]; then
  export WATCH_RECONCILE_INTERVAL_SECONDS="60"
fi

if [ -z "${WATCH_RETRY_MAX_ATTEMPTS:-}" ]; then
  export WATCH_RETRY_MAX_ATTEMPTS="5"
fi

if [ -z "${WATCH_RETRY_BASE_DELAY_SECONDS:-}" ]; then
  export WATCH_RETRY_BASE_DELAY_SECONDS="1"
fi

if [ -z "${WATCH_RETRY_MAX_DELAY_SECONDS:-}" ]; then
  export WATCH_RETRY_MAX_DELAY_SECONDS="30"
fi

if [ -z "${WATCH_HEARTBEAT_INTERVAL_SECONDS:-}" ]; then
  export WATCH_HEARTBEAT_INTERVAL_SECONDS="30"
fi

if [ -z "${WATCH_MAX_EVENTS_PER_CYCLE:-}" ]; then
  export WATCH_MAX_EVENTS_PER_CYCLE="200"
fi

if [ -z "${IDEMPOTENCY_HASH_ALGORITHM:-}" ]; then
  export IDEMPOTENCY_HASH_ALGORITHM="sha256"
fi

if [ -z "${IDEMPOTENCY_SKIP_UNCHANGED:-}" ]; then
  export IDEMPOTENCY_SKIP_UNCHANGED="1"
fi

if [ -z "${IDEMPOTENCY_ENABLE_STALE_CLEANUP:-}" ]; then
  export IDEMPOTENCY_ENABLE_STALE_CLEANUP="1"
fi

if [ -z "${STARTUP_PREFLIGHT_ENABLED:-}" ]; then
  export STARTUP_PREFLIGHT_ENABLED="1"
fi

if [ -z "${STARTUP_PREFLIGHT_TIMEOUT_SECONDS:-}" ]; then
  export STARTUP_PREFLIGHT_TIMEOUT_SECONDS="3"
fi

if [ -z "${STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA:-}" ]; then
  export STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA="1"
fi

if [ -z "${STARTUP_READY_SUMMARY_LOG_ENABLED:-}" ]; then
  export STARTUP_READY_SUMMARY_LOG_ENABLED="1"
fi

if [ -z "${MCP_ENDPOINT_PATH:-}" ]; then
  export MCP_ENDPOINT_PATH="/mcp"
fi

/app/scripts/validate-config.sh
/app/scripts/startup-preflight.sh

touch /tmp/indexer_ready

echo "file-indexer started in mode: ${INDEX_MODE}"
echo "file-indexer watching workspace: ${WORKSPACE_PATH:-/workspace}"
if [ "${INDEX_MODE}" = "watch" ]; then
  echo "watch mode config poll=${WATCH_POLL_INTERVAL_SECONDS}s coalesce=${WATCH_COALESCE_WINDOW_SECONDS}s reconcile=${WATCH_RECONCILE_INTERVAL_SECONDS}s retryMax=${WATCH_RETRY_MAX_ATTEMPTS} retryBase=${WATCH_RETRY_BASE_DELAY_SECONDS}s retryMaxDelay=${WATCH_RETRY_MAX_DELAY_SECONDS}s maxEvents=${WATCH_MAX_EVENTS_PER_CYCLE}"
fi
if [ "${STARTUP_READY_SUMMARY_LOG_ENABLED}" = "1" ]; then
  echo "startup-ready summary service=file-indexer workspace=${WORKSPACE_PATH:-/workspace} mode=${INDEX_MODE} mcpEndpoint=${MCP_ENDPOINT_PATH} collection=${QDRANT_COLLECTION_NAME:-workspace_chunks}"
fi

if [ "${INDEX_MODE}" = "full-scan" ]; then
  /app/scripts/full-scan-worker.sh &
fi

if [ "${INGESTION_BOOTSTRAP_ON_START}" = "1" ]; then
  /app/scripts/ingestion-worker.sh &
fi

if [ "${INDEX_MODE}" = "delta-after-commit" ] && [ "${DELTA_BOOTSTRAP_ON_START}" = "1" ]; then
  /app/scripts/ingestion-worker.sh &
fi

while true; do
  date -u +"%Y-%m-%dT%H:%M:%SZ file-indexer heartbeat mode=${INDEX_MODE} watchPoll=${WATCH_POLL_INTERVAL_SECONDS} watchQueueMax=${WATCH_MAX_EVENTS_PER_CYCLE}"
  sleep 30
done
