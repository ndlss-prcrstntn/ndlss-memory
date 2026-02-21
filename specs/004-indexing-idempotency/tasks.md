# Tasks: Идемпотентность индексации

**Input**: Документы из `/specs/004-indexing-idempotency/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты включены обязательно, так как конституция требует unit/integration,
MCP-контракты, `docker compose up` и регрессию обоих режимов индексатора.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: можно выполнять параллельно (разные файлы, нет блокирующих зависимостей)
- **[Story]**: метка user story (`[US1]`, `[US2]`, `[US3]`)
- В каждой задаче указан точный путь к файлу

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить окружение, фикстуры и документацию для идемпотентной синхронизации

- [X] T001 Создать manifest фикстур идемпотентности в `tests/fixtures/idempotency/fixture-manifest.md`
- [X] T002 [P] Добавить скрипт подготовки тестового окружения в `scripts/tests/idempotency_test_env.ps1`
- [X] T003 [P] Добавить idempotency env-параметры в `.env.example`
- [X] T004 [P] Обновить описание idempotency параметров в `docs/configuration.md`
- [X] T005 [P] Добавить smoke-сценарий контрактной проверки в `tests/contract/idempotency_pipeline_contract_smoke.md`
- [X] T006 [P] Добавить базовый интеграционный сценарий повторного запуска в `tests/integration/us1_idempotent_repeat_run.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты, блокирующие все user stories

- [X] T007 Расширить runtime schema для idempotency параметров в `services/file-indexer/config/runtime-config.schema.json`
- [X] T008 Реализовать валидацию idempotency env-параметров в `services/file-indexer/scripts/validate-config.sh`
- [X] T009 [P] Подключить idempotency env-переменные в `infra/docker/docker-compose.yml`
- [X] T010 Реализовать модель `FileFingerprint` в `services/file-indexer/src/ingestion_pipeline/file_fingerprint.py`
- [X] T011 [P] Реализовать модель `ChunkSyncResult` в `services/file-indexer/src/ingestion_pipeline/chunk_sync_result.py`
- [X] T012 Реализовать состояние idempotency run в `services/mcp-server/src/idempotency_state.py`
- [X] T013 [P] Реализовать error-model idempotency API в `services/mcp-server/src/idempotency_errors.py`
- [X] T014 Добавить каркас idempotency endpoints в `services/mcp-server/src/system_status_handler.py`
- [X] T015 Синхронизировать runtime OpenAPI idempotency API в `services/mcp-server/openapi/idempotency-indexing.openapi.yaml`

**Checkpoint**: После T007-T015 можно независимо реализовывать user stories

---

## Phase 3: User Story 1 - Стабильная идентификация контента (Priority: P1) MVP

**Goal**: Определять неизмененные файлы по SHA256 и пропускать повторную запись без дубликатов

**Independent Test**: Два запуска на неизмененном наборе файлов не увеличивают число уникальных записей

### Tests for User Story 1

- [X] T016 [P] [US1] Добавить unit-тесты SHA256 fingerprint логики в `tests/unit/file_indexer/test_file_fingerprint.py`
- [X] T017 [US1] Реализовать integration-скрипт двух запусков без изменений в `scripts/tests/us1_idempotent_repeat_run.ps1`
- [X] T018 [P] [US1] Добавить integration-спецификацию проверки skip неизмененных файлов в `tests/integration/us1_idempotent_repeat_run.md`

### Implementation for User Story 1

- [X] T019 [US1] Реализовать SHA256 fingerprint builder и сравнение версий в `services/file-indexer/src/ingestion_pipeline/file_fingerprint.py`
- [X] T020 [US1] Реализовать guard проверки существующего hash перед upsert в `services/file-indexer/src/ingestion_pipeline/idempotency_guard.py`
- [X] T021 [US1] Интегрировать skip неизмененных файлов в pipeline в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T022 [US1] Реализовать endpoint запуска `POST /v1/indexing/idempotency/jobs` в `services/mcp-server/src/system_status_handler.py`
- [X] T023 [US1] Реализовать endpoint статуса `GET /v1/indexing/idempotency/jobs/{runId}` в `services/mcp-server/src/system_status_handler.py`
- [X] T024 [US1] Синхронизировать счетчики `updated/skipped/failed` в run state в `services/mcp-server/src/idempotency_state.py`

**Checkpoint**: US1 дает MVP-ценность и проверяется независимо

---

## Phase 4: User Story 2 - Детерминированное обновление чанков (Priority: P2)

**Goal**: Использовать deterministic ID чанков и обновлять только затронутые записи

**Independent Test**: После изменения части файла обновляются только соответствующие чанки без дубликатов

### Tests for User Story 2

- [X] T025 [P] [US2] Добавить unit-тесты deterministic chunk ID в `tests/unit/file_indexer/test_chunk_identity.py`
- [X] T026 [P] [US2] Добавить integration-сценарий selective update в `tests/integration/us2_deterministic_chunk_updates.md`
- [X] T027 [US2] Реализовать integration-скрипт selective update проверки в `scripts/tests/us2_deterministic_chunk_updates.ps1`

### Implementation for User Story 2

- [X] T028 [US2] Реализовать builder `ChunkIdentity` в `services/file-indexer/src/ingestion_pipeline/chunk_identity.py`
- [X] T029 [US2] Обновить upsert-репозиторий на deterministic ID чанков в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T030 [US2] Интегрировать diff текущих и прошлых чанков в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T031 [US2] Реализовать reason codes `UPDATED/SKIPPED_UNCHANGED` в `services/file-indexer/src/ingestion_pipeline/chunk_sync_result.py`
- [X] T032 [US2] Расширить status API счетчиками `updatedChunks/skippedChunks` в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US2 проверяема отдельно после US1

---

## Phase 5: User Story 3 - Очистка устаревших данных (Priority: P3)

**Goal**: Удалять устаревшие чанки при изменении/удалении исходных файлов

**Independent Test**: После удаления файла или сокращения контента stale чанки отсутствуют в индексе

### Tests for User Story 3

- [X] T033 [P] [US3] Добавить контрактный тест summary с `deletedChunks` в `tests/contract/us3_idempotency_summary_contract.md`
- [X] T034 [P] [US3] Добавить integration-сценарий stale cleanup в `tests/integration/us3_stale_chunk_cleanup.md`
- [X] T035 [US3] Реализовать integration-скрипт удаления/сокращения файла в `scripts/tests/us3_stale_chunk_cleanup.ps1`

### Implementation for User Story 3

- [X] T036 [US3] Реализовать модель `StaleChunkSet` в `services/file-indexer/src/ingestion_pipeline/stale_chunk_set.py`
- [X] T037 [US3] Реализовать удаление obsolete chunk IDs в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T038 [US3] Интегрировать обработку удаленных файлов в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T039 [US3] Реализовать endpoint summary `GET /v1/indexing/idempotency/jobs/{runId}/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T040 [US3] Реализовать summary-модель `IndexSyncSummary` с `reasonBreakdown` в `services/file-indexer/src/ingestion_pipeline/index_sync_summary.py`
- [X] T041 [US3] Обновить quickstart под сценарии stale cleanup в `specs/004-indexing-idempotency/quickstart.md`

**Checkpoint**: US3 завершает требования по очистке устаревших чанков

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная валидация регрессий, контрактов и документации

- [X] T042 [P] Валидировать feature OpenAPI контракт в `specs/004-indexing-idempotency/contracts/idempotency-indexing.openapi.yaml`
- [X] T043 Проверить регрессию `full-scan` после idempotency внедрения в `tests/integration/regression_full_scan_after_idempotency.md`
- [X] T044 [P] Проверить регрессию `delta-after-commit` после idempotency внедрения в `tests/integration/regression_delta_after_commit_after_idempotency.md`
- [X] T045 [P] Добавить compose regression-скрипт идемпотентности в `scripts/tests/idempotency_compose_regression.ps1`
- [X] T046 Обновить roadmap-статусы section 5 в `README.md`
- [X] T047 [P] Обновить release checklist фичи в `specs/004-indexing-idempotency/release-checklist.md`
- [X] T048 Зафиксировать e2e результаты проверок фичи в `specs/004-indexing-idempotency/implementation-report.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): старт сразу
- Foundational (Phase 2): зависит от Setup, блокирует user stories
- User Stories (Phase 3-5): стартуют после Foundational
- Polish (Phase 6): после завершения целевых user stories

### User Story Dependencies

- US1 (P1): зависит только от Foundational, формирует MVP идемпотентности
- US2 (P2): зависит от US1, использует готовый fingerprint/skip flow
- US3 (P3): зависит от US2, требует deterministic ID и diff чанков

### Dependency Graph

- `US1 -> MVP`
- `US2 -> US1`
- `US3 -> US2`
- Рекомендуемый порядок поставки: `P1 -> P2 -> P3`

---

## Parallel Execution Examples

### US1

```text
- [ ] T016 [P] [US1] Добавить unit-тесты SHA256 fingerprint логики в `tests/unit/file_indexer/test_file_fingerprint.py`
- [ ] T018 [P] [US1] Добавить integration-спецификацию проверки skip неизмененных файлов в `tests/integration/us1_idempotent_repeat_run.md`
- [ ] T020 [US1] Реализовать guard проверки существующего hash перед upsert в `services/file-indexer/src/ingestion_pipeline/idempotency_guard.py`
```

### US2

```text
- [ ] T025 [P] [US2] Добавить unit-тесты deterministic chunk ID в `tests/unit/file_indexer/test_chunk_identity.py`
- [ ] T026 [P] [US2] Добавить integration-сценарий selective update в `tests/integration/us2_deterministic_chunk_updates.md`
- [ ] T029 [US2] Обновить upsert-репозиторий на deterministic ID чанков в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
```

### US3

```text
- [ ] T033 [P] [US3] Добавить контрактный тест summary с `deletedChunks` в `tests/contract/us3_idempotency_summary_contract.md`
- [ ] T034 [P] [US3] Добавить integration-сценарий stale cleanup в `tests/integration/us3_stale_chunk_cleanup.md`
- [ ] T036 [US3] Реализовать модель `StaleChunkSet` в `services/file-indexer/src/ingestion_pipeline/stale_chunk_set.py`
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать US1 (T016-T024)
3. Проверить независимый acceptance тест US1
4. Зафиксировать MVP baseline без дубликатов

### Incremental Delivery

1. MVP fingerprint + skip unchanged (US1)
2. Deterministic chunk updates (US2)
3. Stale chunk cleanup (US3)
4. Финальная регрессия и документация (Phase 6)

### Format Validation

- Все задачи соответствуют формату: `- [ ] T### [P?] [US?] Описание с путем`
- Для задач user story всегда указан story label (`[US1]`, `[US2]`, `[US3]`)
- Для Setup/Foundational/Polish story label не используется
- Каждая задача содержит явный путь к файлу
