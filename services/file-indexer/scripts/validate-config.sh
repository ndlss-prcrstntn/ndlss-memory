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

if ! echo "$COMMAND_TIMEOUT_SECONDS" | grep -Eq '^[0-9]+$'; then
  echo "COMMAND_TIMEOUT_SECONDS must be a positive integer"
  exit 1
fi

if [ "$COMMAND_TIMEOUT_SECONDS" -lt 1 ]; then
  echo "COMMAND_TIMEOUT_SECONDS must be >= 1"
  exit 1
fi

echo "Configuration validation passed"
