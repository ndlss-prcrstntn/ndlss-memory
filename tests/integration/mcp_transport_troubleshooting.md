# Integration: MCP Transport Troubleshooting

## Цель

Подтвердить, что типовые ошибки конфигурации MCP клиента диагностируются предсказуемо.

## Сценарии

1. Клиент использует `http://localhost:8080/` вместо `/mcp`.
   - ожидаемо получает 404/405 при попытке JSON-RPC.
2. Клиент отправляет non-JSON payload в `/mcp`.
   - ожидается JSON-RPC parse error (`-32700`).
3. Клиент вызывает `/messages` без `sessionId`.
   - ожидается JSON-RPC invalid request (`-32600`) и HTTP 400.
4. Клиент вызывает `/messages` с несуществующим `sessionId`.
   - ожидается HTTP 404 и `error.data.errorCode=SESSION_NOT_FOUND`.
5. Клиент вызывает `tools/list` без инициализации сессии.
   - ожидается `error.data.errorCode=SESSION_NOT_INITIALIZED`.

