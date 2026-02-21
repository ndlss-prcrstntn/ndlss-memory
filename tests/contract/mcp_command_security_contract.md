# Contract Smoke: MCP Command Security

## Preconditions

- `mcp-server` доступен на `http://localhost:8080`
- Политика `COMMAND_ALLOWLIST` и `COMMAND_TIMEOUT_SECONDS` задана

## Execute Command Contract

- [ ] `POST /v1/commands/execute` с валидным allowlist-командой возвращает HTTP 200
- [ ] Ответ содержит `status`, `result`, `meta`
- [ ] `meta` содержит `requestId`, `requestedAt`, `finishedAt`, `durationMs`
- [ ] Для неразрешенной команды возвращается HTTP 403 и `errorCode=COMMAND_NOT_ALLOWED`
- [ ] Для пустого `command` возвращается HTTP 400 и `errorCode=INVALID_REQUEST`
- [ ] Для timeout-сценария возвращается `status=timeout` с `result.errorCode=COMMAND_TIMEOUT`

## Execution Lookup Contract

- [ ] `GET /v1/commands/executions/{requestId}` для существующего requestId возвращает HTTP 200
- [ ] Для неизвестного requestId возвращается HTTP 404 и `errorCode=REQUEST_NOT_FOUND`

## Audit Contract

- [ ] `GET /v1/commands/audit` возвращает HTTP 200 и поля `status`, `records`, `meta`
- [ ] `records[]` содержит `requestId`, `timestamp`, `command`, `status`
- [ ] Фильтр `status` ограничивает выборку
- [ ] Некорректный `status` фильтр возвращает HTTP 400 и `errorCode=INVALID_REQUEST`

## Isolation & Resource Policy Contract

- [ ] Запрос с `workingDirectory` вне workspace отклоняется с `WORKSPACE_ISOLATION_VIOLATION`
- [ ] Команда выполняется только в разрешенной рабочей зоне
- [ ] Команда с превышением лимита времени не остается в фоне после ответа
