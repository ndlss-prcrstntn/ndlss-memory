# Startup Preflight Readiness Contract

## Scope

Контракт фиксирует поведение startup preflight и readiness API для фичи
`001-startup-preflight-summary`.

## Endpoints

- `GET /health`
- `GET /v1/system/startup/readiness`
- `GET /v1/system/config`

## Assertions

1. `GET /health` возвращает `200` и JSON с `status=ok`.
2. `GET /v1/system/startup/readiness`:
   - в ready-сценарии возвращает `200` и `status=ready`;
   - в fail-fast сценарии возвращает `503` и объект `StartupFailureReport`.
   - при неготовности без сохраненного fail-report возвращает `503` и
     `errorCode=STARTUP_NOT_READY`.
3. Ready payload содержит поля:
   - `serviceReadiness`
   - `workspacePath`
   - `indexMode`
   - `mcpEndpoint`
   - `collectionName`
   - `preflightChecks`
   - `checkedAt`
4. Fail payload содержит поля:
   - `errorCode`
   - `message`
   - `failedChecks`
   - `generatedAt`
5. `GET /v1/system/config` содержит startup-диагностику без удаления
   существующих полей.

## Error Model Assertions

Для fail-fast ответа обязательны поля:

- `errorCode` (string)
- `message` (string)
- `failedChecks` (array, минимум 1 элемент)
- `generatedAt` (ISO date-time)

Для каждого элемента `failedChecks` обязательны:

- `checkId`
- `status=failed`
- `severity`
- `message`
- `checkedAt`

Опциональные, но поддерживаемые поля:

- `details`
- `action`
- `recommendedActions`

## Negative Scenarios

- Недоступный Qdrant -> fail-fast с кодом ошибки preflight.
- Нечитаемый/отсутствующий workspace -> fail-fast.
- `INDEX_MODE=delta-after-commit` и недоступный git -> fail-fast.

## Notes

- Контракт не изменяет существующее поведение endpoint после успешного старта.
- Формат ошибок должен оставаться машиночитаемым (`errorCode`, `message`, `details`).
