#!/usr/bin/env sh
set -eu

if [ -z "${INDEX_MODE:-}" ]; then
  echo "INDEX_MODE is required"
  exit 1
fi

case "$INDEX_MODE" in
  full-scan|delta-after-commit) ;;
  *)
    echo "INDEX_MODE must be full-scan or delta-after-commit"
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

if [ -z "${INDEX_PROGRESS_INTERVAL_SECONDS:-}" ]; then
  echo "INDEX_PROGRESS_INTERVAL_SECONDS is required"
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

echo "Configuration validation passed"
