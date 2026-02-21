# Tasks: Delta-after-commit режим

**Input**: Документы из `/specs/005-delta-after-commit/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты включены обязательно, так как конституция требует unit/integration,
MCP-контракты, `docker compose up` и регрессию индексатора.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: можно выполнять параллельно (разные файлы, нет блокирующих зависимостей)
- **[Story]**: метка user story (`[US1]`, `[US2]`, `[US3]`)
- В каждой задаче указан точный путь к файлу

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить окружение, фикстуры и операционные сценарии delta-режима

- [X] T001 Создать manifest фикстур delta-after-commit в `tests/fixtures/delta-after-commit/fixture-manifest.md`
- [X] T002 [P] Добавить базовые фикстуры (`added/modified/deleted/renamed`) в `tests/fixtures/delta-after-commit/`
- [X] T003 [P] Добавить скрипт подготовки тестового окружения в `scripts/tests/delta_after_commit_test_env.ps1`
- [X] T004 [P] Добавить delta env-параметры в `.env.example`
- [X] T005 [P] Обновить описание delta параметров в `docs/configuration.md`
- [X] T006 [P] Добавить smoke-сценарий контрактной проверки в `tests/contract/delta_after_commit_contract_smoke.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты, блокирующие все user stories

- [X] T007 Расширить runtime schema для delta параметров в `services/file-indexer/config/runtime-config.schema.json`
- [X] T008 Реализовать валидацию delta env-параметров в `services/file-indexer/scripts/validate-config.sh`
- [X] T009 [P] Подключить delta env-переменные в `infra/docker/docker-compose.yml`
- [X] T010 [P] Создать пакет delta-after-commit в `services/file-indexer/src/delta_after_commit/__init__.py`
- [X] T011 Реализовать модели `GitChangeSet` и `DeltaCandidateFile` в `services/file-indexer/src/delta_after_commit/change_models.py`
- [X] T012 [P] Реализовать reader git diff в `services/file-indexer/src/delta_after_commit/git_diff_reader.py`
- [X] T013 Реализовать классификатор решений (`index/delete/skip`) в `services/file-indexer/src/delta_after_commit/change_classifier.py`
- [X] T014 [P] Реализовать модель сводки delta-run в `services/file-indexer/src/delta_after_commit/delta_run_summary.py`
- [X] T015 Реализовать состояние delta-run API в `services/mcp-server/src/delta_after_commit_state.py`
- [X] T016 [P] Реализовать error-model delta API в `services/mcp-server/src/delta_after_commit_errors.py`
- [X] T017 Добавить каркас delta endpoints в `services/mcp-server/src/system_status_handler.py`
- [X] T018 Синхронизировать runtime OpenAPI delta API в `services/mcp-server/openapi/delta-after-commit-indexing.openapi.yaml`

**Checkpoint**: После T007-T018 можно независимо реализовывать user stories

---

## Phase 3: User Story 1 - Индексация только измененных файлов (Priority: P1) MVP

**Goal**: Индексировать только `added/modified` файлы на основе `git diff` без повторной обработки неизмененных

**Independent Test**: Запустить delta-run на наборе с `added/modified/unchanged` и подтвердить обработку только измененных

### Tests for User Story 1

- [X] T019 [P] [US1] Добавить unit-тесты парсинга git diff в `tests/unit/file_indexer/test_git_diff_reader.py`
- [X] T020 [P] [US1] Добавить контрактный сценарий start/status endpoint в `tests/contract/us1_delta_jobs_contract.md`
- [X] T021 [P] [US1] Добавить integration-сценарий changed-only в `tests/integration/us1_delta_changed_only.md`
- [X] T022 [US1] Реализовать integration-скрипт changed-only проверки в `scripts/tests/us1_delta_changed_only.ps1`

### Implementation for User Story 1

- [X] T023 [US1] Реализовать сервис delta-run orchestration в `services/file-indexer/src/delta_after_commit/delta_after_commit_service.py`
- [X] T024 [US1] Интегрировать выполнение git diff и выбор `added/modified` в `services/file-indexer/src/delta_after_commit/delta_after_commit_service.py`
- [X] T025 [US1] Подключить режим `delta-after-commit` в worker-поток в `services/file-indexer/scripts/ingestion-worker.sh`
- [X] T026 [US1] Реализовать endpoint запуска `POST /v1/indexing/delta-after-commit/jobs` в `services/mcp-server/src/system_status_handler.py`
- [X] T027 [US1] Реализовать endpoint статуса `GET /v1/indexing/delta-after-commit/jobs/{runId}` в `services/mcp-server/src/system_status_handler.py`
- [X] T028 [US1] Синхронизировать счетчики `added/modified/indexed/skipped` в `services/mcp-server/src/delta_after_commit_state.py`

**Checkpoint**: US1 дает MVP-ценность и проверяется независимо

---

## Phase 4: User Story 2 - Корректная обработка удаления и переименования (Priority: P2)

**Goal**: Удалять stale-записи для `deleted` и корректно переносить связи при `renamed`

**Independent Test**: Удалить файл и переименовать файл, затем подтвердить отсутствие старых путей в индексе

### Tests for User Story 2

- [X] T029 [P] [US2] Добавить контрактный сценарий summary (`deletedFiles`, `renamedFiles`) в `tests/contract/us2_delta_summary_contract.md`
- [X] T030 [P] [US2] Добавить integration-сценарий delete+rename в `tests/integration/us2_delta_delete_rename.md`
- [X] T031 [US2] Реализовать integration-скрипт delete+rename проверки в `scripts/tests/us2_delta_delete_rename.ps1`

### Implementation for User Story 2

- [X] T032 [US2] Реализовать обработку `deleted` изменений в `services/file-indexer/src/delta_after_commit/delta_after_commit_service.py`
- [X] T033 [US2] Реализовать модель `PathTransition` в `services/file-indexer/src/delta_after_commit/path_transition.py`
- [X] T034 [US2] Интегрировать удаление stale-записей по пути в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T035 [US2] Реализовать обработку `renamed` (remove old + index new) в `services/file-indexer/src/delta_after_commit/delta_after_commit_service.py`
- [X] T036 [US2] Реализовать endpoint summary `GET /v1/indexing/delta-after-commit/jobs/{runId}/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T037 [US2] Расширить reason codes и summary counters в `services/mcp-server/src/delta_after_commit_errors.py`

**Checkpoint**: US2 проверяема отдельно после US1

---

## Phase 5: User Story 3 - Надежный фоллбек на полный скан (Priority: P3)

**Goal**: При ошибке Git автоматически выполнять `full-scan-fallback` и фиксировать причину

**Independent Test**: Смоделировать ошибку Git diff и подтвердить `effectiveMode=full-scan-fallback`

### Tests for User Story 3

- [X] T038 [P] [US3] Добавить контрактный сценарий fallback-полей (`effectiveMode`, `fallbackReasonCode`) в `tests/contract/us3_delta_fallback_contract.md`
- [X] T039 [P] [US3] Добавить integration-сценарий fallback на full-scan в `tests/integration/us3_delta_fallback_full_scan.md`
- [X] T040 [US3] Реализовать integration-скрипт fallback проверки в `scripts/tests/us3_delta_fallback_full_scan.ps1`

### Implementation for User Story 3

- [X] T041 [US3] Реализовать политику fallback в `services/file-indexer/src/delta_after_commit/fallback_policy.py`
- [X] T042 [US3] Интегрировать автопереключение на full-scan в `services/file-indexer/src/delta_after_commit/delta_after_commit_service.py`
- [X] T043 [US3] Передавать `effectiveMode` и `fallbackReasonCode` в run-state в `services/mcp-server/src/delta_after_commit_state.py`
- [X] T044 [US3] Реализовать машиночитаемые fallback-ошибки в `services/mcp-server/src/delta_after_commit_errors.py`
- [X] T045 [US3] Обновить status/summary обработчики fallback-метриками в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US3 завершает отказоустойчивость delta-run

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная валидация регрессий, контрактов и документации

- [X] T046 [P] Валидировать feature OpenAPI контракт в `specs/005-delta-after-commit/contracts/delta-after-commit-indexing.openapi.yaml`
- [X] T047 [P] Проверить runtime OpenAPI синхронизацию в `services/mcp-server/openapi/delta-after-commit-indexing.openapi.yaml`
- [X] T048 Проверить регрессию `full-scan` после delta внедрения в `tests/integration/regression_full_scan_after_delta_after_commit.md`
- [X] T049 [P] Проверить регрессию идемпотентности после delta внедрения в `tests/integration/regression_idempotency_after_delta_after_commit.md`
- [X] T050 [P] Добавить compose regression-скрипт delta режима в `scripts/tests/delta_after_commit_compose_regression.ps1`
- [X] T051 Обновить основную документацию и quickstart в `README.md`
- [X] T052 [P] Обновить quickstart фичи в `specs/005-delta-after-commit/quickstart.md`
- [X] T053 Зафиксировать e2e результаты проверок фичи в `specs/005-delta-after-commit/implementation-report.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): старт сразу
- Foundational (Phase 2): зависит от Setup, блокирует user stories
- User Stories (Phase 3-5): стартуют после Foundational
- Polish (Phase 6): после завершения целевых user stories

### User Story Dependencies

- US1 (P1): зависит только от Foundational, формирует MVP delta режима
- US2 (P2): зависит от US1, использует готовый delta pipeline и run-state
- US3 (P3): зависит от US1, добавляет fallback-политику без изменения бизнес-логики US2

### Dependency Graph

- `US1 -> MVP`
- `US2 -> US1`
- `US3 -> US1`
- Рекомендуемый порядок поставки: `P1 -> P2 -> P3`

---

## Parallel Execution Examples

### US1

```text
- [X] T019 [P] [US1] Добавить unit-тесты парсинга git diff в `tests/unit/file_indexer/test_git_diff_reader.py`
- [X] T020 [P] [US1] Добавить контрактный сценарий start/status endpoint в `tests/contract/us1_delta_jobs_contract.md`
- [X] T021 [P] [US1] Добавить integration-сценарий changed-only в `tests/integration/us1_delta_changed_only.md`
```

### US2

```text
- [X] T029 [P] [US2] Добавить контрактный сценарий summary (`deletedFiles`, `renamedFiles`) в `tests/contract/us2_delta_summary_contract.md`
- [X] T030 [P] [US2] Добавить integration-сценарий delete+rename в `tests/integration/us2_delta_delete_rename.md`
- [X] T034 [US2] Интегрировать удаление stale-записей по пути в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
```

### US3

```text
- [X] T038 [P] [US3] Добавить контрактный сценарий fallback-полей (`effectiveMode`, `fallbackReasonCode`) в `tests/contract/us3_delta_fallback_contract.md`
- [X] T039 [P] [US3] Добавить integration-сценарий fallback на full-scan в `tests/integration/us3_delta_fallback_full_scan.md`
- [X] T041 [US3] Реализовать политику fallback в `services/file-indexer/src/delta_after_commit/fallback_policy.py`
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать US1 (T019-T028)
3. Проверить независимый acceptance тест US1
4. Зафиксировать MVP baseline с индексированием только измененных файлов

### Incremental Delivery

1. MVP delta changed-only flow (US1)
2. Delete/rename synchronization (US2)
3. Full-scan fallback hardening (US3)
4. Финальная регрессия и документация (Phase 6)

### Format Validation

- Все задачи соответствуют формату: `- [ ] T### [P?] [US?] Описание с путем`
- Для задач user story всегда указан story label (`[US1]`, `[US2]`, `[US3]`)
- Для Setup/Foundational/Polish story label не используется
- Каждая задача содержит явный путь к файлу
