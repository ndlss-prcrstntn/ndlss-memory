# Data Model: Качество и стабильность

## Entity: QualityRun

- Description: Единичный прогон полного quality-контура.
- Fields:
  - `runId` (string, required): уникальный идентификатор прогона.
  - `startedAt` (datetime, required): время старта.
  - `finishedAt` (datetime, optional): время завершения.
  - `status` (enum, required): `queued | running | passed | failed | canceled`.
  - `scope` (object, required): какие наборы включены (`unit`, `integration`, `contract`, `e2e`).
  - `summary` (object, required): агрегированные метрики (`totalStages`, `passedStages`, `failedStages`).
- Validation Rules:
  - `runId` не пустой и уникальный в рамках истории прогонов.
  - `finishedAt` >= `startedAt`, если указан.
  - `status=passed` допустим только при `failedStages=0`.

## Entity: QualityStageResult

- Description: Результат отдельного этапа внутри одного `QualityRun`.
- Fields:
  - `runId` (string, required): ссылка на родительский прогон.
  - `stageName` (enum, required): `unit | integration | contract | e2e`.
  - `status` (enum, required): `passed | failed | skipped`.
  - `durationMs` (integer, required): длительность этапа.
  - `failureCode` (string, optional): машиночитаемый код ошибки.
  - `failureMessage` (string, optional): краткое объяснение причины сбоя.
  - `artifactPaths` (array[string], optional): ссылки на артефакты (`tests/`, logs, reports).
- Validation Rules:
  - `durationMs >= 0`.
  - `failureCode` и `failureMessage` обязательны при `status=failed`.
  - `artifactPaths` должны ссылаться на пути внутри репозитория.

## Entity: RegressionEvidence

- Description: Набор артефактов для диагностики регрессий и доказательства идемпотентности.
- Fields:
  - `evidenceId` (string, required): уникальный идентификатор записи.
  - `runId` (string, required): ссылка на `QualityRun`.
  - `category` (enum, required): `unit-report | integration-log | contract-report | e2e-log | idempotency-proof`.
  - `path` (string, required): путь к артефакту.
  - `checksum` (string, optional): контрольная сумма содержимого.
  - `createdAt` (datetime, required): время фиксации артефакта.
- Validation Rules:
  - `path` должен быть относительным к `Z:\WORK\ndlss-memory`.
  - `category=idempotency-proof` требует подтверждение отсутствия прироста дублей.

## Relationships

- `QualityRun` 1 -> N `QualityStageResult`.
- `QualityRun` 1 -> N `RegressionEvidence`.
- `QualityStageResult` может ссылаться на 0..N `RegressionEvidence` через `artifactPaths`.

## State Transitions

### QualityRun

- `queued -> running`: старт запуска.
- `running -> passed`: все этапы завершились `passed`.
- `running -> failed`: хотя бы один этап завершился `failed`.
- `running -> canceled`: запуск остановлен вручную или по глобальному timeout.

### QualityStageResult

- `skipped -> passed|failed` не допускается (этап пересоздается новым запуском).
- `passed|failed` считаются terminal-состояниями для конкретного этапа в рамках `runId`.
