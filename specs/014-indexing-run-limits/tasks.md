# Tasks: Ограничение глубины и объема индексации

**Input**: Документы из `/specs/014-indexing-run-limits/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Тесты включены, так как фича меняет критичный индексатор и публичные summary/контракты.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет зависимости по незавершенной задаче)
- **[Story]**: Привязка к user story (`[US1]`, `[US2]`, `[US3]`)
- Каждая задача содержит точные пути к файлам

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить конфигурацию окружения и compose-пресеты для лимитов запуска.

- [X] T001 Добавить переменные лимитов запуска в `.env.example`
- [X] T002 Добавить проброс переменных лимитов в `docker-compose.yml` и `infra/docker/docker-compose.yml`
- [X] T003 [P] Добавить проброс переменных лимитов в `deploy/compose-images/generic.yml`, `deploy/compose-images/typescript.yml`, `deploy/compose-images/csharp.yml`
- [X] T004 [P] Добавить валидацию и дефолты лимитов в `services/file-indexer/scripts/validate-config.sh` и `services/file-indexer/scripts/entrypoint.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты лимитов, которые блокируют все user story.

- [X] T005 Создать модель политики лимитов и функции валидации в `services/mcp-server/src/indexing_run_limits.py`
- [X] T006 [P] Добавить вычисление глубины пути и стабильную сортировку кандидатов в `services/file-indexer/src/full_scan_walker.py`
- [X] T007 [P] Добавить skip-reason коды лимитов в `services/file-indexer/src/skip_reasons.py` и `services/mcp-server/src/full_scan_state.py`
- [X] T008 Расширить состояния запусков полями лимитов в `services/mcp-server/src/full_scan_state.py` и `services/mcp-server/src/ingestion_state.py`
- [X] T009 [P] Подготовить фикстуры глубокой структуры/большого набора файлов в `tests/fixtures/full-scan/limits-depth` и `tests/fixtures/idempotency/limits-count`

**Checkpoint**: Базовая инфраструктура лимитов готова, можно реализовывать user stories.

---

## Phase 3: User Story 1 - Контроль масштаба одного запуска (Priority: P1) MVP

**Goal**: Ограничить blast radius одного запуска через `maxTraversalDepth` и `maxFilesPerRun` в full-scan.

**Independent Test**: Full-scan на репозитории глубже/больше лимитов должен обрабатывать только допустимые файлы и не превышать max-files.

### Tests for User Story 1

- [X] T010 [P] [US1] Добавить unit-тесты отбора файлов по глубине и количеству в `tests/unit/file_indexer/test_run_limits_selection.py`
- [X] T011 [P] [US1] Добавить integration-тест глубины обхода в `tests/integration/test_run_limits_full_scan_depth.py`
- [X] T012 [P] [US1] Добавить integration-тест ограничения количества файлов в `tests/integration/test_run_limits_full_scan_max_files.py`

### Implementation for User Story 1

- [X] T013 [US1] Реализовать фильтрацию по глубине и лимит по количеству в `services/file-indexer/src/full_scan_service.py`
- [X] T014 [US1] Прокинуть лимиты из запроса full-scan в выполнение джобы в `services/mcp-server/src/system_status_handler.py`
- [X] T015 [US1] Обновить модель full-scan run summary с полями applied limits в `services/file-indexer/src/scan_models.py` и `services/mcp-server/src/full_scan_state.py`
- [X] T016 [US1] Добавить отклонение невалидных значений лимитов в API full-scan в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US1 завершена, full-scan детерминированно уважает оба лимита.

---

## Phase 4: User Story 2 - Единые правила в разных режимах индексации (Priority: P2)

**Goal**: Применять те же лимиты и правила отбора в релевантных ingestion-путях с сохранением backward compatibility по дефолтам.

**Independent Test**: Ingestion с теми же лимитами должен демонстрировать те же правила отбора, а запуск без лимитов должен повторять старое поведение.

### Tests for User Story 2

- [X] T017 [P] [US2] Добавить integration-тест согласованности лимитов в ingestion в `tests/integration/test_run_limits_ingestion_consistency.py`
- [X] T018 [P] [US2] Добавить integration-тест backward compatibility при unset лимитах в `tests/integration/test_run_limits_defaults_backward_compat.py`
- [X] T019 [P] [US2] Добавить contract-тест валидации лимитов для ingestion start в `tests/contract/test_run_limits_ingestion_contract.py`

### Implementation for User Story 2

- [X] T020 [US2] Реализовать применение depth/max-files лимитов в ingestion pipeline в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T021 [US2] Прокинуть лимиты из ingestion API в pipeline запуск в `services/mcp-server/src/system_status_handler.py` и `services/mcp-server/src/ingestion_pipeline/ingestion_service.py`
- [X] T022 [US2] Добавить единое поведение ошибок невалидных лимитов для ingestion в `services/mcp-server/src/system_status_handler.py` и `services/mcp-server/src/ingestion_errors.py`
- [X] T023 [US2] Зафиксировать обратносуместимые дефолты для unset лимитов в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US2 завершена, full-scan и ingestion применяют лимиты единообразно.

---

## Phase 5: User Story 3 - Прозрачная отчетность по ограничениям (Priority: P3)

**Goal**: Summary полно и однозначно объясняет примененные лимиты и skip reasons.

**Independent Test**: При срабатывании лимитов summary full-scan и ingestion содержит applied limits и раздельные причины пропуска.

### Tests for User Story 3

- [X] T024 [P] [US3] Добавить contract-тест full-scan summary полей лимитов в `tests/contract/test_run_limits_full_scan_summary_contract.py`
- [X] T025 [P] [US3] Добавить contract-тест ingestion summary полей лимитов в `tests/contract/test_run_limits_ingestion_summary_contract.py`
- [X] T026 [P] [US3] Добавить integration-тест отчетности при одновременном достижении лимитов в `tests/integration/test_run_limits_summary_reporting.py`

### Implementation for User Story 3

- [X] T027 [US3] Добавить applied limits и limit skip breakdown в full-scan summary response в `services/mcp-server/src/full_scan_state.py` и `services/file-indexer/src/scan_models.py`
- [X] T028 [US3] Добавить applied limits и limit skip breakdown в ingestion summary response в `services/mcp-server/src/ingestion_state.py` и `services/file-indexer/src/ingestion_pipeline/run_summary.py`
- [X] T029 [US3] Обновить API выдачу summary payload в `services/mcp-server/src/system_status_handler.py`
- [X] T030 [US3] Синхронизировать сервисные OpenAPI контракты в `services/mcp-server/openapi/full-scan-indexing.openapi.yaml` и `services/mcp-server/openapi/chunking-embeddings.openapi.yaml`
- [X] T031 [US3] Синхронизировать feature-контракт в `specs/014-indexing-run-limits/contracts/indexing-run-limits.openapi.yaml`

**Checkpoint**: US3 завершена, оператор получает прозрачную диагностику лимитов по summary.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная стабилизация, документация и прогон quality gates.

- [X] T032 [P] Обновить пользовательскую документацию лимитов в `README.md`, `docs/configuration.md`, `specs/014-indexing-run-limits/quickstart.md`
- [X] T033 Добавить/обновить smoke-сценарии лимитов в `scripts/tests/us2_full_scan_filtering.ps1` и `scripts/tests/us2_quality_search_flow.ps1`
- [X] T034 Выполнить полный quality suite и зафиксировать артефакты в `tests/artifacts/quality-stability/quality-run-report.json` и `tests/artifacts/quality-stability/final-regression-log.md`
- [X] T035 [P] Обновить changelog релиза в `CHANGELOG.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
- User story фазы стартуют только после завершения Foundational (Phase 2)
- US2 зависит от общих ограничителей и поведения US1
- US3 зависит от реализации summary payload в US1/US2

### User Story Dependency Graph

- US1 -> US2 -> US3

---

## Parallel Execution Examples

### US1

- Параллельно запускать `T010`, `T011`, `T012` (разные тестовые файлы).
- После `T013` параллельно выполнять `T014` и `T015`.

### US2

- Параллельно запускать `T017`, `T018`, `T019`.
- После `T020` параллельно выполнять `T022` и `T023`.

### US3

- Параллельно запускать `T024`, `T025`, `T026`.
- После `T029` параллельно выполнять `T030` и `T031`.

---

## Implementation Strategy

### MVP First (US1)

1. Завершить Setup и Foundational (Phase 1-2).
2. Реализовать US1 (Phase 3) и подтвердить независимым integration-test.
3. Зафиксировать MVP как минимально полезный инкремент для контроля blast radius одного запуска.

### Incremental Delivery

1. Добавить US2 для единообразия между full-scan и ingestion.
2. Добавить US3 для операционной прозрачности summary.
3. Завершить polish-фазой с документацией и quality suite.

