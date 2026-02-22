# Data Model: Watch Mode Incremental Indexing

## Entity: WatchEvent

**Description**: Нормализованное событие изменения файла, поступившее в watch-loop.

### Fields

- `eventId` (string, required): уникальный идентификатор события.
- `eventType` (enum, required): `created | updated | deleted | renamed`.
- `path` (string, required): абсолютный/контейнерный путь файла в workspace.
- `oldPath` (string, optional): предыдущий путь для rename.
- `detectedAt` (date-time, required): время обнаружения события.
- `coalescedAt` (date-time, optional): время включения в batch коалесценции.
- `status` (enum, required): `queued | processing | completed | failed | skipped`.
- `errorCode` (string, optional): машиночитаемый код ошибки обработки.
- `errorMessage` (string, optional): объяснение ошибки.

### Validation Rules

- `eventType=renamed` требует `oldPath`.
- `status=failed` требует `errorCode` и `errorMessage`.
- `path` должен принадлежать `workspacePath` и проходить фильтры include/exclude.

## Entity: WatchRunState

**Description**: Текущее состояние непрерывного watcher runtime.

### Fields

- `mode` (enum, required): `watch`.
- `state` (enum, required): `starting | running | recovering | failed | stopped`.
- `workspacePath` (string, required)
- `startedAt` (date-time, required)
- `lastHeartbeatAt` (date-time, required)
- `lastEventAt` (date-time, optional)
- `queueDepth` (integer, required, >= 0)
- `processedEvents` (integer, required, >= 0)
- `failedEvents` (integer, required, >= 0)
- `retryCount` (integer, required, >= 0)
- `lastErrorCode` (string, optional)
- `lastErrorMessage` (string, optional)

### Validation Rules

- `state=failed` допускается только при наличии `lastErrorCode`.
- `queueDepth` не может быть отрицательным.
- `lastHeartbeatAt` обновляется в каждом цикле watch-loop.

## Entity: IncrementalIndexResult

**Description**: Итог обработки события/батча событий в watch режиме.

### Fields

- `resultId` (string, required)
- `windowStartedAt` (date-time, required)
- `windowFinishedAt` (date-time, required)
- `affectedFiles` (array[string], required)
- `indexedFiles` (integer, required, >= 0)
- `deletedRecords` (integer, required, >= 0)
- `skippedFiles` (integer, required, >= 0)
- `failedFiles` (integer, required, >= 0)
- `reasonBreakdown` (array[object], optional): агрегированные причины skip/failure.

### Validation Rules

- `failedFiles > 0` требует непустой `reasonBreakdown`.
- `windowFinishedAt >= windowStartedAt`.

## Relationships

- `WatchRunState` 1:N `WatchEvent`.
- `IncrementalIndexResult` агрегирует набор `WatchEvent` в окне коалесценции.
- `IncrementalIndexResult.affectedFiles` должен быть подмножеством путей из соответствующих `WatchEvent`.

## State Transitions

- `WatchRunState`: `starting -> running -> recovering -> running`.
- `WatchRunState`: `running -> failed -> recovering -> running`.
- `WatchEvent`: `queued -> processing -> completed`.
- `WatchEvent`: `queued -> processing -> failed`.
- `WatchEvent`: `queued -> skipped` (unsupported/excluded path).
