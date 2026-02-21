#!/usr/bin/env sh
set -eu

if [ -z "${MCP_PORT:-}" ]; then
  export MCP_PORT=8080
fi

if [ -z "${COMMAND_TIMEOUT_SECONDS:-}" ]; then
  export COMMAND_TIMEOUT_SECONDS=20
fi

exec python /app/src/system_status_handler.py
