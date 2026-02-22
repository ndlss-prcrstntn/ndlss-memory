# Data Model: Startup Preflight and Ready Summary

## Entity: StartupCheckResult

**Description**: Результат отдельной предполетной проверки зависимости перед запуском runtime.

### Fields

- `checkId` (string, required): стабильный идентификатор проверки (`qdrant_reachability`, `workspace_readable`, `git_available`).
- `status` (enum, required): `passed | failed | skipped`.
- `severity` (enum, required): `critical | warning | info`.
- `errorCode` (string, optional): код ошибки при `failed`.
- `message` (string, required): человекочитаемое описание результата.
- `details` (object, optional): структурированные диагностические детали.
- `action` (string, optional): краткая рекомендация оператору.
- `checkedAt` (string, required, date-time): время выполнения проверки.

### Validation Rules

- `status=failed` требует `errorCode` и `action`.
- `severity=critical` и `status=failed` блокируют запуск.
- `status=skipped` допустим только для проверок, не применимых к текущему `indexMode`.

## Entity: StartupFailureReport

**Description**: Единый fail-fast отчет о неуспешном старте.

### Fields

- `errorCode` (string, required): агрегированный код причины остановки старта.
- `message` (string, required): краткая причина отказа.
- `details` (object, optional): расширенный контекст ошибки.
- `failedChecks` (array[StartupCheckResult], required): список проверок со статусом `failed`.
- `recommendedActions` (array[string], optional): список действий для исправления.
- `generatedAt` (string, required, date-time): время формирования отчета.

### Validation Rules

- `failedChecks` должен содержать минимум один элемент.
- Каждый элемент `failedChecks` должен иметь `severity=critical` или явно помеченный блокирующий статус.

## Entity: StartupReadinessSummary

**Description**: Агрегированная сводка готовности после успешного старта.

### Fields

- `status` (enum, required): `ready`.
- `serviceReadiness` (object, required): состояние `qdrant`, `file-indexer`, `mcp-server`.
- `workspacePath` (string, required): эффективный путь workspace внутри контейнера.
- `indexMode` (enum, required): `full-scan | delta-after-commit`.
- `mcpEndpoint` (string, required): endpoint MCP транспорта (например, `/mcp`).
- `collectionName` (string, required): имя рабочей коллекции Qdrant.
- `preflightChecks` (array[StartupCheckResult], required): результаты всех startup checks.
- `checkedAt` (string, required, date-time): время завершения preflight.

### Validation Rules

- `status=ready` допустим только если нет `failed` проверок с `severity=critical`.
- `preflightChecks` должен включать минимум проверки `qdrant_reachability` и `workspace_readable`.
- Для `indexMode=delta-after-commit` `preflightChecks` обязан включать `git_available`.

## Entity: StartupRuntimeContext

**Description**: Нормализованный runtime-контекст для preflight.

### Fields

- `qdrantHost` (string, required)
- `qdrantApiPort` (integer, required, > 0)
- `workspacePath` (string, required)
- `indexMode` (string, required)
- `gitRequired` (boolean, required)
- `collectionName` (string, required)

### Relationships

- `StartupRuntimeContext` используется для вычисления набора `StartupCheckResult`.
- При наличии критического провала формируется `StartupFailureReport`.
- При успешных проверках формируется `StartupReadinessSummary`.

## State Transitions

- `booting -> preflight_running -> failed` (если есть блокирующий check).
- `booting -> preflight_running -> ready` (если все критичные проверки пройдены).
- `ready` не должен переходить в `failed` без нового процесса старта (новый контейнер/перезапуск).
