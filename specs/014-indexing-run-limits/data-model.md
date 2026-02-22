# Data Model: Ограничение глубины и объема индексации

## Entity: IndexingRunLimitPolicy

- Purpose: Хранит фактически примененные ограничения запуска индексации.

### Fields

- `maxTraversalDepth` (integer | null)
  - Описание: Максимально разрешенная глубина обхода директорий.
  - Validation:
    - `null` = лимит не задан;
    - целое число `>= 0`.
- `maxFilesPerRun` (integer | null)
  - Описание: Максимально разрешенное количество файлов на запуск.
  - Validation:
    - `null` = лимит не задан;
    - целое число `>= 1`.
- `isDefaultBehavior` (boolean)
  - Описание: Индикатор, что запуск выполняется в полностью обратносуместимом режиме (без ограничений).

## Entity: FileSelectionCandidate

- Purpose: Представляет файл-кандидат на индексацию до применения лимитов.

### Fields

- `path` (string, required)
  - Validation: непустой, нормализованный относительный путь внутри workspace.
- `depth` (integer, required)
  - Validation: `>= 0`.
- `eligible` (boolean, required)
  - Описание: прошел ли файл базовые правила отбора (тип/исключения).

## Entity: FileSelectionDecision

- Purpose: Фиксирует итоговое решение по файлу после применения лимитов.

### Fields

- `path` (string, required)
- `depth` (integer, required)
- `decision` (enum, required)
  - Allowed values: `selected`, `skipped`.
- `skipReasonCode` (enum | null)
  - Allowed values: `LIMIT_DEPTH_EXCEEDED`, `LIMIT_MAX_FILES_REACHED`, `null`.
- `orderIndex` (integer, required)
  - Описание: позиция файла в детерминированном порядке отбора.

### Validation Rules

- Если `decision=selected`, тогда `skipReasonCode=null`.
- Если `decision=skipped`, тогда `skipReasonCode` обязателен.

## Entity: IndexingRunLimitSummary

- Purpose: Публичная сводка применения лимитов в результате запуска.

### Fields

- `appliedLimits` (object, required)
  - `maxTraversalDepth` (integer | null)
  - `maxFilesPerRun` (integer | null)
- `skipBreakdown` (array, required)
  - каждый элемент: `{ code: string, count: integer >= 0 }`
  - ожидаемые коды для этой фичи:
    - `LIMIT_DEPTH_EXCEEDED`
    - `LIMIT_MAX_FILES_REACHED`
- `selectedFilesCount` (integer, required, `>= 0`)
- `skippedByLimitsCount` (integer, required, `>= 0`)

## Relationships

- `IndexingRunLimitPolicy` 1:many `FileSelectionDecision`.
- `FileSelectionCandidate` 1:1 `FileSelectionDecision` (в рамках одного запуска).
- `IndexingRunLimitSummary` агрегирует множество `FileSelectionDecision`.

## State Transitions

### FileSelectionDecision Lifecycle

- `evaluated` -> `selected`
  - Условие: файл проходит лимит глубины и попадает в диапазон `maxFilesPerRun`.
- `evaluated` -> `skipped (LIMIT_DEPTH_EXCEEDED)`
  - Условие: `depth > maxTraversalDepth`.
- `evaluated` -> `skipped (LIMIT_MAX_FILES_REACHED)`
  - Условие: лимит количества файлов уже достигнут.

## Derived Invariants

- `selectedFilesCount <= maxFilesPerRun`, если `maxFilesPerRun` задан.
- Файлы с `depth > maxTraversalDepth` не могут иметь `decision=selected`.
- Для одинакового множества `FileSelectionCandidate` и одинаковой `IndexingRunLimitPolicy` набор `selected` файлов идентичен между запусками.
