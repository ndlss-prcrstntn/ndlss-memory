# Integration: MCP Command Security Smoke

## Planned Steps

1. Запустить стек:
   - `powershell -File scripts/dev/up.ps1`
2. Проверить health:
   - `curl http://localhost:8080/health`
3. Выполнить разрешенную команду `pwd` через `POST /v1/commands/execute`.
4. Проверить response envelope (`status`, `result`, `meta.requestId`).
5. Получить execution result по `GET /v1/commands/executions/{requestId}`.
6. Проверить, что `GET /v1/commands/audit?limit=20` содержит запись вызова.

## Execution Record (2026-02-21)

- `docker compose up -d --build` частично выполнен, но общий smoke blocked:
  - `file-indexer` unhealthy из-за CRLF shebang (`env: 'sh\r': No such file or directory`).
- Для проверки feature runtime отдельно поднят контейнер `ndlss-memory-mcp-server:latest` на `http://localhost:18080`.

Проверки:

1. `GET /health`:
   - `{"status":"ok", ...}`.
2. `POST /v1/commands/execute` (`pwd`):
   - `status=ok`, `result.exitCode=0`, корректный `meta.requestId`.
3. `POST /v1/commands/execute` (`rm -rf /`):
   - HTTP `403`, `errorCode=COMMAND_NOT_ALLOWED`.
4. `POST /v1/commands/execute` (`sleep 10`, `timeoutSeconds=2`):
   - `status=timeout`, `result.errorCode=COMMAND_TIMEOUT`.
5. `GET /v1/commands/executions/{requestId}`:
   - возвращает сохраненный execution result.
6. `GET /v1/commands/audit?limit=10`:
   - содержит записи вызовов с `requestId`, `command`, `status`.
