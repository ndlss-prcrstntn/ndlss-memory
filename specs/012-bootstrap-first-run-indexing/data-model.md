# Data Model: First-Run Bootstrap Indexing

## Entity: WorkspaceBootstrapState

**Description**: Персистентное состояние bootstrap для конкретного workspace.

### Fields

- `workspaceKey` (string, required): детерминированный ключ workspace (нормализованный путь/идентификатор).
- `collectionName` (string, required): целевая коллекция Qdrant.
- `status` (enum, required): `pending | running | completed | failed | skipped`.
- `trigger` (enum, required): `auto-startup | manual`.
- `attempt` (integer, required): номер попытки bootstrap.
- `lastRunId` (string, optional): связанный ingestion run id.
- `startedAt` (date-time, optional): время начала активного запуска.
- `finishedAt` (date-time, optional): время завершения.
- `errorCode` (string, optional): код последней ошибки.
- `errorMessage` (string, optional): краткое описание ошибки.
- `createdCollection` (boolean, required): была ли коллекция создана в этой попытке.
- `pointCountAfterRun` (integer, required): число точек после завершения bootstrap.

### Validation Rules

- `status=running` требует `startedAt`.
- `status in [completed, failed, skipped]` требует `finishedAt`.
- `status=failed` требует `errorCode` и `errorMessage`.
- `attempt` монотонно возрастает для одного `workspaceKey`.

## Entity: CollectionReadinessSnapshot

**Description**: Снимок готовности целевой коллекции для проверки searchable-state.

### Fields

- `collectionName` (string, required)
- `exists` (boolean, required)
- `pointCount` (integer, required, >= 0)
- `checkedAt` (date-time, required)
- `qdrantHost` (string, required)
- `qdrantApiPort` (integer, required)

### Validation Rules

- `exists=false` => `pointCount=0`.
- `pointCount` не может быть отрицательным.

## Entity: StartupBootstrapSummary

**Description**: Агрегированная startup-сводка по bootstrap для логов и API-ответов.

### Fields

- `status` (enum, required): `ready | running | blocked | failed | skipped`.
- `workspacePath` (string, required)
- `indexMode` (enum, required): `full-scan | delta-after-commit`.
- `bootstrap` (object, required):
  - `trigger` (`auto-startup | manual`)
  - `decision` (`run | skip-already-completed | retry-failed`)
  - `runId` (string, optional)
  - `reason` (string, optional)
  - `stateRef` (string, optional, workspaceKey)
- `collection` (`CollectionReadinessSnapshot`, required)
- `serviceReadiness` (object, required): `qdrant | fileIndexer | mcpServer`
- `checkedAt` (date-time, required)

### Validation Rules

- `decision=run` требует `bootstrap.runId`.
- `status=ready` допускается только при `collection.exists=true`.
- `decision=skip-already-completed` допустим только если `WorkspaceBootstrapState.status=completed`.

## Entity: BootstrapIngestionLink

**Description**: Связь авто-bootstrap и стандартного ingestion run.

### Fields

- `runId` (string, required)
- `workspaceKey` (string, required)
- `initiator` (enum, required): `auto-bootstrap | manual-api`
- `isBootstrapRun` (boolean, required)
- `summaryExposed` (boolean, required): признак, что bootstrap-поля опубликованы в summary endpoint.

### Relationships

- `WorkspaceBootstrapState.lastRunId` -> `BootstrapIngestionLink.runId`.
- `BootstrapIngestionLink.runId` соответствует записи в ingestion runtime state.
- `StartupBootstrapSummary.bootstrap.stateRef` -> `WorkspaceBootstrapState.workspaceKey`.

## State Transitions

- `pending -> running -> completed`
- `pending -> running -> failed`
- `completed -> skipped` (на restart без изменений; дорогой bootstrap не повторяется)
- `failed -> running` (контролируемый retry по политике)
- `skipped -> running` (только при явном manual ingestion или reset состояния)

