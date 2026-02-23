# Data Model: Docs Collection Indexing + Baseline Docs Search

## Entity: DocumentationCollectionPolicy

- Purpose: Описывает правила отбора и уникальности для docs-индекса.

### Fields

- `allowedExtensions` (array[string], required)
  - Validation: непустой список расширений; для этой фичи включает `.md`.
- `documentIdentityRule` (string, required)
  - Allowed value: `normalized_path`.
- `chunkIdentityRule` (string, required)
  - Allowed value: `path_plus_stable_chunk_index`.
- `changeDetectionRule` (string, required)
  - Allowed value: `content_hash`.

## Entity: DocumentationFile

- Purpose: Представляет markdown-документ, отслеживаемый docs-индексацией.

### Fields

- `path` (string, required)
  - Validation: нормализованный относительный путь в пределах workspace.
- `contentHash` (string, required)
  - Validation: непустой hash текущего содержимого.
- `status` (enum, required)
  - Allowed values: `indexed`, `updated`, `deleted`, `skipped`.
- `lastIndexedAt` (string, required)
  - Validation: ISO 8601 datetime.

## Entity: DocumentationChunk

- Purpose: Индексируемый фрагмент документации для поиска.

### Fields

- `documentPath` (string, required)
- `stableChunkIndex` (integer, required)
  - Validation: `>= 0`.
- `chunkText` (string, required)
  - Validation: непустой текст.
- `sourceTitle` (string, nullable)
- `metadata` (object, required)
  - Minimum keys: `path`, `fileType`, `contentHash`.

### Validation Rules

- Пара `documentPath + stableChunkIndex` уникальна в рамках docs-коллекции.
- При изменении `contentHash` документа stale-чанки удаляются до записи новых.

## Entity: DocsIndexingRunSummary

- Purpose: Сводка запуска docs-индексации.

### Fields

- `runId` (string, required)
- `status` (enum, required)
  - Allowed values: `completed`, `partial`, `failed`.
- `totals` (object, required)
  - `processedDocuments` (integer, `>= 0`)
  - `indexedDocuments` (integer, `>= 0`)
  - `updatedDocuments` (integer, `>= 0`)
  - `skippedDocuments` (integer, `>= 0`)
  - `deletedDocuments` (integer, `>= 0`)
- `skipBreakdown` (array, required)
  - элемент: `{ code: string, count: integer >= 0 }`
- `startedAt` (string, required, datetime)
- `finishedAt` (string, nullable, datetime)

## Entity: DocsSearchRequest

- Purpose: Входной запрос на baseline docs-поиск.

### Fields

- `query` (string, required)
  - Validation: непустой после trim.
- `limit` (integer, optional)
  - Validation: `1..50`, default `10`.
- `workspacePath` (string, optional)

## Entity: DocsSearchResultItem

- Purpose: Единица выдачи docs-поиска.

### Fields

- `documentPath` (string, required)
- `chunkIndex` (integer, required)
- `snippet` (string, required)
- `score` (number, required)
- `sourceType` (string, required)
  - Allowed value: `documentation`.

## Relationships

- `DocumentationFile` 1:many `DocumentationChunk`.
- `DocsSearchRequest` 1:many `DocsSearchResultItem` (в рамках одного ответа).
- `DocsIndexingRunSummary` агрегирует множество `DocumentationFile` transitions.

## State Transitions

### DocumentationFile Lifecycle

- `discovered` -> `indexed`
  - Условие: новый markdown-документ прошел правила отбора.
- `indexed` -> `updated`
  - Условие: зафиксировано изменение `contentHash`.
- `indexed|updated` -> `deleted`
  - Условие: документ удален из workspace.
- `discovered` -> `skipped`
  - Условие: документ не прошел правила отбора/валидации.

## Derived Invariants

- В docs-выдаче `sourceType` всегда равно `documentation`.
- В docs-коллекции отсутствуют чанки исходного кода.
- Для одинакового индекса и одинакового запроса порядок top-k детерминирован.
