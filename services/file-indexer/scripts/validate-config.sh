#!/usr/bin/env sh
set -eu

if [ -z "${INDEX_MODE:-}" ]; then
  echo "INDEX_MODE is required"
  exit 1
fi

case "$INDEX_MODE" in
  full-scan|delta-after-commit|watch) ;;
  *)
    echo "INDEX_MODE must be full-scan, delta-after-commit, or watch"
    exit 1
    ;;
esac

if [ -z "${INDEX_FILE_TYPES:-}" ]; then
  echo "INDEX_FILE_TYPES is required"
  exit 1
fi

if [ -z "${COMMAND_TIMEOUT_SECONDS:-}" ]; then
  echo "COMMAND_TIMEOUT_SECONDS is required"
  exit 1
fi

if [ -z "${INDEX_MAX_FILE_SIZE_BYTES:-}" ]; then
  echo "INDEX_MAX_FILE_SIZE_BYTES is required"
  exit 1
fi

if [ -n "${INDEX_MAX_TRAVERSAL_DEPTH:-}" ]; then
  if ! echo "$INDEX_MAX_TRAVERSAL_DEPTH" | grep -Eq '^[0-9]+$'; then
    echo "INDEX_MAX_TRAVERSAL_DEPTH must be a non-negative integer"
    exit 1
  fi
fi

if [ -n "${INDEX_MAX_FILES_PER_RUN:-}" ]; then
  if ! echo "$INDEX_MAX_FILES_PER_RUN" | grep -Eq '^[0-9]+$'; then
    echo "INDEX_MAX_FILES_PER_RUN must be a positive integer"
    exit 1
  fi
  if [ "$INDEX_MAX_FILES_PER_RUN" -lt 1 ]; then
    echo "INDEX_MAX_FILES_PER_RUN must be >= 1"
    exit 1
  fi
fi

if [ -z "${INDEX_PROGRESS_INTERVAL_SECONDS:-}" ]; then
  echo "INDEX_PROGRESS_INTERVAL_SECONDS is required"
  exit 1
fi

if [ -z "${INGESTION_CHUNK_SIZE:-}" ]; then
  echo "INGESTION_CHUNK_SIZE is required"
  exit 1
fi

if [ -z "${INGESTION_CHUNK_OVERLAP:-}" ]; then
  echo "INGESTION_CHUNK_OVERLAP is required"
  exit 1
fi

if [ -z "${INGESTION_RETRY_MAX_ATTEMPTS:-}" ]; then
  echo "INGESTION_RETRY_MAX_ATTEMPTS is required"
  exit 1
fi

if [ -z "${INGESTION_RETRY_BACKOFF_SECONDS:-}" ]; then
  echo "INGESTION_RETRY_BACKOFF_SECONDS is required"
  exit 1
fi

if [ -z "${DELTA_GIT_BASE_REF:-}" ]; then
  echo "DELTA_GIT_BASE_REF is required"
  exit 1
fi

if [ -z "${DELTA_GIT_TARGET_REF:-}" ]; then
  echo "DELTA_GIT_TARGET_REF is required"
  exit 1
fi

if [ -z "${DELTA_INCLUDE_RENAMES:-}" ]; then
  echo "DELTA_INCLUDE_RENAMES is required"
  exit 1
fi

if [ -z "${DELTA_ENABLE_FALLBACK:-}" ]; then
  echo "DELTA_ENABLE_FALLBACK is required"
  exit 1
fi

if [ -z "${DELTA_BOOTSTRAP_ON_START:-}" ]; then
  echo "DELTA_BOOTSTRAP_ON_START is required"
  exit 1
fi

if [ -z "${WATCH_POLL_INTERVAL_SECONDS:-}" ]; then
  echo "WATCH_POLL_INTERVAL_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_COALESCE_WINDOW_SECONDS:-}" ]; then
  echo "WATCH_COALESCE_WINDOW_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_RECONCILE_INTERVAL_SECONDS:-}" ]; then
  echo "WATCH_RECONCILE_INTERVAL_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_RETRY_MAX_ATTEMPTS:-}" ]; then
  echo "WATCH_RETRY_MAX_ATTEMPTS is required"
  exit 1
fi

if [ -z "${WATCH_RETRY_BASE_DELAY_SECONDS:-}" ]; then
  echo "WATCH_RETRY_BASE_DELAY_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_RETRY_MAX_DELAY_SECONDS:-}" ]; then
  echo "WATCH_RETRY_MAX_DELAY_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_HEARTBEAT_INTERVAL_SECONDS:-}" ]; then
  echo "WATCH_HEARTBEAT_INTERVAL_SECONDS is required"
  exit 1
fi

if [ -z "${WATCH_MAX_EVENTS_PER_CYCLE:-}" ]; then
  echo "WATCH_MAX_EVENTS_PER_CYCLE is required"
  exit 1
fi

if [ -z "${IDEMPOTENCY_HASH_ALGORITHM:-}" ]; then
  echo "IDEMPOTENCY_HASH_ALGORITHM is required"
  exit 1
fi

if [ -z "${IDEMPOTENCY_SKIP_UNCHANGED:-}" ]; then
  echo "IDEMPOTENCY_SKIP_UNCHANGED is required"
  exit 1
fi

if [ -z "${IDEMPOTENCY_ENABLE_STALE_CLEANUP:-}" ]; then
  echo "IDEMPOTENCY_ENABLE_STALE_CLEANUP is required"
  exit 1
fi

if ! echo "$COMMAND_TIMEOUT_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "COMMAND_TIMEOUT_SECONDS must be a positive integer"
  exit 1
fi

if [ "$COMMAND_TIMEOUT_SECONDS" -lt 1 ]; then
  echo "COMMAND_TIMEOUT_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$INDEX_MAX_FILE_SIZE_BYTES" | grep -Eq '^[0-9]+$'; then
  echo "INDEX_MAX_FILE_SIZE_BYTES must be a positive integer"
  exit 1
fi

if [ "$INDEX_MAX_FILE_SIZE_BYTES" -lt 1 ]; then
  echo "INDEX_MAX_FILE_SIZE_BYTES must be >= 1"
  exit 1
fi

if ! echo "$INDEX_PROGRESS_INTERVAL_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "INDEX_PROGRESS_INTERVAL_SECONDS must be a positive integer"
  exit 1
fi

if [ "$INDEX_PROGRESS_INTERVAL_SECONDS" -lt 1 ]; then
  echo "INDEX_PROGRESS_INTERVAL_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$INGESTION_CHUNK_SIZE" | grep -Eq '^[0-9]+$'; then
  echo "INGESTION_CHUNK_SIZE must be a positive integer"
  exit 1
fi

if [ "$INGESTION_CHUNK_SIZE" -lt 1 ]; then
  echo "INGESTION_CHUNK_SIZE must be >= 1"
  exit 1
fi

if ! echo "$INGESTION_CHUNK_OVERLAP" | grep -Eq '^[0-9]+$'; then
  echo "INGESTION_CHUNK_OVERLAP must be a non-negative integer"
  exit 1
fi

if [ "$INGESTION_CHUNK_OVERLAP" -lt 0 ]; then
  echo "INGESTION_CHUNK_OVERLAP must be >= 0"
  exit 1
fi

if [ "$INGESTION_CHUNK_OVERLAP" -ge "$INGESTION_CHUNK_SIZE" ]; then
  echo "INGESTION_CHUNK_OVERLAP must be < INGESTION_CHUNK_SIZE"
  exit 1
fi

if ! echo "$INGESTION_RETRY_MAX_ATTEMPTS" | grep -Eq '^[0-9]+$'; then
  echo "INGESTION_RETRY_MAX_ATTEMPTS must be a positive integer"
  exit 1
fi

if [ "$INGESTION_RETRY_MAX_ATTEMPTS" -lt 1 ]; then
  echo "INGESTION_RETRY_MAX_ATTEMPTS must be >= 1"
  exit 1
fi

if ! echo "$INGESTION_RETRY_BACKOFF_SECONDS" | grep -Eq '^[0-9]+([.][0-9]+)?$'; then
  echo "INGESTION_RETRY_BACKOFF_SECONDS must be > 0"
  exit 1
fi

if [ "${INGESTION_RETRY_BACKOFF_SECONDS#0}" = "." ] || [ "$INGESTION_RETRY_BACKOFF_SECONDS" = "0" ] || [ "$INGESTION_RETRY_BACKOFF_SECONDS" = "0.0" ]; then
  echo "INGESTION_RETRY_BACKOFF_SECONDS must be > 0"
  exit 1
fi

if [ "$DELTA_INCLUDE_RENAMES" != "0" ] && [ "$DELTA_INCLUDE_RENAMES" != "1" ]; then
  echo "DELTA_INCLUDE_RENAMES must be 0 or 1"
  exit 1
fi

if [ "$DELTA_ENABLE_FALLBACK" != "0" ] && [ "$DELTA_ENABLE_FALLBACK" != "1" ]; then
  echo "DELTA_ENABLE_FALLBACK must be 0 or 1"
  exit 1
fi

if [ "$DELTA_BOOTSTRAP_ON_START" != "0" ] && [ "$DELTA_BOOTSTRAP_ON_START" != "1" ]; then
  echo "DELTA_BOOTSTRAP_ON_START must be 0 or 1"
  exit 1
fi

if ! echo "$WATCH_POLL_INTERVAL_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_POLL_INTERVAL_SECONDS must be a positive integer"
  exit 1
fi

if [ "$WATCH_POLL_INTERVAL_SECONDS" -lt 1 ]; then
  echo "WATCH_POLL_INTERVAL_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$WATCH_COALESCE_WINDOW_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_COALESCE_WINDOW_SECONDS must be a positive integer"
  exit 1
fi

if [ "$WATCH_COALESCE_WINDOW_SECONDS" -lt 1 ]; then
  echo "WATCH_COALESCE_WINDOW_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$WATCH_RECONCILE_INTERVAL_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_RECONCILE_INTERVAL_SECONDS must be a positive integer"
  exit 1
fi

if [ "$WATCH_RECONCILE_INTERVAL_SECONDS" -lt 1 ]; then
  echo "WATCH_RECONCILE_INTERVAL_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$WATCH_RETRY_MAX_ATTEMPTS" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_RETRY_MAX_ATTEMPTS must be a positive integer"
  exit 1
fi

if [ "$WATCH_RETRY_MAX_ATTEMPTS" -lt 1 ]; then
  echo "WATCH_RETRY_MAX_ATTEMPTS must be >= 1"
  exit 1
fi

if ! echo "$WATCH_RETRY_BASE_DELAY_SECONDS" | grep -Eq '^[0-9]+([.][0-9]+)?$'; then
  echo "WATCH_RETRY_BASE_DELAY_SECONDS must be > 0"
  exit 1
fi

if [ "$WATCH_RETRY_BASE_DELAY_SECONDS" = "0" ] || [ "$WATCH_RETRY_BASE_DELAY_SECONDS" = "0.0" ]; then
  echo "WATCH_RETRY_BASE_DELAY_SECONDS must be > 0"
  exit 1
fi

if ! echo "$WATCH_RETRY_MAX_DELAY_SECONDS" | grep -Eq '^[0-9]+([.][0-9]+)?$'; then
  echo "WATCH_RETRY_MAX_DELAY_SECONDS must be > 0"
  exit 1
fi

if [ "$WATCH_RETRY_MAX_DELAY_SECONDS" = "0" ] || [ "$WATCH_RETRY_MAX_DELAY_SECONDS" = "0.0" ]; then
  echo "WATCH_RETRY_MAX_DELAY_SECONDS must be > 0"
  exit 1
fi

if ! echo "$WATCH_HEARTBEAT_INTERVAL_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_HEARTBEAT_INTERVAL_SECONDS must be a positive integer"
  exit 1
fi

if [ "$WATCH_HEARTBEAT_INTERVAL_SECONDS" -lt 1 ]; then
  echo "WATCH_HEARTBEAT_INTERVAL_SECONDS must be >= 1"
  exit 1
fi

if ! echo "$WATCH_MAX_EVENTS_PER_CYCLE" | grep -Eq '^[0-9]+$'; then
  echo "WATCH_MAX_EVENTS_PER_CYCLE must be a positive integer"
  exit 1
fi

if [ "$WATCH_MAX_EVENTS_PER_CYCLE" -lt 1 ]; then
  echo "WATCH_MAX_EVENTS_PER_CYCLE must be >= 1"
  exit 1
fi

if [ -n "${INGESTION_MAX_CHUNKS_PER_FILE:-}" ]; then
  if ! echo "$INGESTION_MAX_CHUNKS_PER_FILE" | grep -Eq '^[0-9]+$'; then
    echo "INGESTION_MAX_CHUNKS_PER_FILE must be a positive integer"
    exit 1
  fi
  if [ "$INGESTION_MAX_CHUNKS_PER_FILE" -lt 1 ]; then
    echo "INGESTION_MAX_CHUNKS_PER_FILE must be >= 1"
    exit 1
  fi
fi

if [ "$IDEMPOTENCY_HASH_ALGORITHM" != "sha256" ]; then
  echo "IDEMPOTENCY_HASH_ALGORITHM must be sha256"
  exit 1
fi

if [ "$IDEMPOTENCY_SKIP_UNCHANGED" != "0" ] && [ "$IDEMPOTENCY_SKIP_UNCHANGED" != "1" ]; then
  echo "IDEMPOTENCY_SKIP_UNCHANGED must be 0 or 1"
  exit 1
fi

if [ "$IDEMPOTENCY_ENABLE_STALE_CLEANUP" != "0" ] && [ "$IDEMPOTENCY_ENABLE_STALE_CLEANUP" != "1" ]; then
  echo "IDEMPOTENCY_ENABLE_STALE_CLEANUP must be 0 or 1"
  exit 1
fi

if [ -n "${IDEMPOTENCY_MAX_DELETE_BATCH:-}" ]; then
  if ! echo "$IDEMPOTENCY_MAX_DELETE_BATCH" | grep -Eq '^[0-9]+$'; then
    echo "IDEMPOTENCY_MAX_DELETE_BATCH must be a positive integer"
    exit 1
  fi
  if [ "$IDEMPOTENCY_MAX_DELETE_BATCH" -lt 1 ]; then
    echo "IDEMPOTENCY_MAX_DELETE_BATCH must be >= 1"
    exit 1
  fi
fi

echo "Configuration validation passed"
