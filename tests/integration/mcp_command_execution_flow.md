# Integration: Command Execution Allowlist/Timeout

## Goal

Проверить основной поток allowlist/deny/timeout для secure command runtime.

## Steps

1. Разрешенная команда:
   - `POST /v1/commands/execute` с `command=pwd`.
   - Ожидание: HTTP 200, `status=ok`.
2. Запрещенная команда:
   - `POST /v1/commands/execute` с `command=rm`.
   - Ожидание: HTTP 403, `errorCode=COMMAND_NOT_ALLOWED`.
3. Таймаут:
   - `POST /v1/commands/execute` с `command=sleep`, `args=[30]`, `timeoutSeconds=2`.
   - Ожидание: `status=timeout`, `result.errorCode=COMMAND_TIMEOUT`.
4. Проверка lookup:
   - `GET /v1/commands/executions/{requestId}` для валидного requestId.
