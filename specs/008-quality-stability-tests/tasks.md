# Tasks: Качество и стабильность

**Input**: Документы из `Z:\WORK\ndlss-memory\specs\008-quality-stability-tests\`
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты обязательны для этой фичи (unit, integration, contract, E2E) по требованиям спецификации и конституции.

**Organization**: Задачи сгруппированы по user story (US1, US2, US3) для независимой реализации и проверки.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Инициализация общего каркаса запуска и хранения артефактов.

- [X] T001 Создать документ набора quality-проверок в `docs/testing/quality-stability.md`
- [X] T002 Создать директорию артефактов качества в `tests/artifacts/quality-stability/.gitkeep`
- [X] T003 [P] Создать конфигурацию pytest-маркеров для quality-ранов в `pytest.ini`
- [X] T004 [P] Создать entrypoint запуска quality-suite в `scripts/tests/run_quality_stability_suite.ps1`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Блокирующие компоненты, общие для всех user stories.

- [X] T005 Описать stage-result контракт для quality-run в `tests/contract/quality_stage_result_contract.md`
- [X] T006 Реализовать общие функции записи stage-результатов в `scripts/tests/quality_stage_helpers.ps1`
- [X] T007 [P] Синхронизировать runtime OpenAPI-контракт в `services/mcp-server/openapi/quality-stability-tests.openapi.yaml`
- [X] T008 [P] Уточнить feature OpenAPI-схему в `specs/008-quality-stability-tests/contracts/quality-stability-tests.openapi.yaml`
- [X] T009 Реализовать проверку контрактов quality-run в `scripts/tests/contract_quality_stability.ps1`
- [X] T010 Реализовать оркестратор порядка `unit -> integration -> contract -> e2e` в `scripts/tests/quality_gate_runner.ps1`

**Checkpoint**: Общий каркас quality-run готов, можно реализовывать user stories независимо.

---

## Phase 3: User Story 1 - Базовое покрытие критичной логики (Priority: P1) MVP

**Goal**: Закрыть базовое покрытие логики индексации и идемпотентности повторного запуска.

**Independent Test**: Запуск `pytest tests/unit/file_indexer` и `scripts/tests/us1_idempotent_repeat_run.ps1` дает PASS и формирует артефакт идемпотентности.

### Tests for User Story 1

- [X] T011 [P] [US1] Добавить edge-cases чанкинга в `tests/unit/file_indexer/test_chunker.py`
- [X] T012 [P] [US1] Добавить проверки стабильности hash и unchanged-input в `tests/unit/file_indexer/test_file_fingerprint.py`
- [X] T013 [P] [US1] Добавить edge-cases фильтрации путей и типов файлов в `tests/unit/file_indexer/test_file_filters.py`
- [X] T014 [US1] Усилить проверки repeat-run для идемпотентности в `scripts/tests/us1_idempotent_repeat_run.ps1`

### Implementation for User Story 1

- [X] T015 [US1] Встроить этап US1 и его failure-codes в `scripts/tests/quality_gate_runner.ps1`
- [X] T016 [US1] Сохранять артефакт итогов US1 в `tests/artifacts/quality-stability/us1-idempotency-summary.json`
- [X] T017 [US1] Обновить сценарий независимой проверки US1 в `tests/integration/us1_idempotent_repeat_run.md`

**Checkpoint**: US1 завершена и демонстрируется отдельно как MVP.

---

## Phase 4: User Story 2 - Проверка межсервисных сценариев (Priority: P2)

**Goal**: Валидировать интеграцию записи в Qdrant и поиска через MCP на реальном compose-стеке.

**Independent Test**: `scripts/tests/ingestion_compose_regression.ps1` и US2 search flow завершаются PASS и создают integration-артефакт.

### Tests for User Story 2

- [X] T018 [P] [US2] Добавить проверки доступности записанных чанков в `scripts/tests/ingestion_compose_regression.ps1`
- [X] T019 [P] [US2] Добавить сценарий проверки `semantic search` в `scripts/tests/us2_quality_search_flow.ps1`
- [X] T020 [P] [US2] Расширить контракт `empty/non-empty results` в `tests/contract/mcp_search_tools_contract.md`

### Implementation for User Story 2

- [X] T021 [US2] Обновить интеграционный сценарий межсервисного поиска в `tests/integration/mcp_search_tools_smoke.md`
- [X] T022 [US2] Встроить этап US2 и mapping кодов ошибок в `scripts/tests/quality_gate_runner.ps1`
- [X] T023 [US2] Сохранять артефакт этапа US2 в `tests/artifacts/quality-stability/us2-integration-summary.json`

**Checkpoint**: US2 завершена и проверяется независимо от US3.

---

## Phase 5: User Story 3 - Сквозная регрессия перед релизом (Priority: P3)

**Goal**: Реализовать единый E2E quality-прогон от compose startup до повторной проверки стабильности.

**Independent Test**: E2E-скрипт выполняет `docker compose up`, `full-scan`, `delta-after-commit`, `semantic search`, повторный запуск и возвращает PASS/FAIL.

### Tests for User Story 3

- [X] T024 [P] [US3] Создать E2E smoke-скрипт полного цикла в `scripts/tests/quality_stability_e2e.ps1`
- [X] T025 [P] [US3] Описать E2E acceptance-сценарии в `tests/integration/quality_stability_e2e.md`
- [X] T026 [P] [US3] Добавить контракт E2E stage transitions в `tests/contract/quality_stability_e2e_contract.md`

### Implementation for User Story 3

- [X] T027 [US3] Встроить этап US3 в агрегатор качества в `scripts/tests/quality_gate_runner.ps1`
- [X] T028 [US3] Добавить проверку repeat-run consistency в `scripts/tests/quality_stability_e2e.ps1`
- [X] T029 [US3] Сохранять итоговый отчет QualityRun в `tests/artifacts/quality-stability/quality-run-report.json`

**Checkpoint**: US3 завершена, полная сквозная регрессия выполняется автоматически.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная стабилизация, документация и проверка качества релизного набора.

- [X] T030 [P] Обновить quickstart фичи с финальными командами в `specs/008-quality-stability-tests/quickstart.md`
- [X] T031 [P] Обновить пользовательское описание quality-gates и roadmap-статусы в `README.md`
- [X] T032 Добавить скрипт проверки UTF-8 для markdown-артефактов в `scripts/tests/validate_markdown_encoding.ps1`
- [X] T033 Выполнить полный quality-run и зафиксировать регрессионный отчет в `tests/artifacts/quality-stability/final-regression-log.md`
- [X] T034 Зафиксировать результаты contract-check запуска в `tests/artifacts/quality-stability/contract-check-summary.md`

---

## Dependencies & Execution Order

- Setup: `T001-T004` -> Foundational: `T005-T010` -> US1: `T011-T017` -> US2: `T018-T023` -> US3: `T024-T029` -> Polish: `T030-T034`
- Story completion order: `US1 -> US2 -> US3`
- Внутри каждой истории: тестовые задачи выполняются до задач интеграции этапа в `quality_gate_runner`.

## Parallel Execution Examples

- US1: `T011`, `T012`, `T013` можно выполнять параллельно.
- US2: `T018`, `T019`, `T020` можно выполнять параллельно.
- US3: `T024`, `T025`, `T026` можно выполнять параллельно.
- Polish: `T030`, `T031` можно выполнять параллельно.

## Implementation Strategy

- MVP: завершить Setup + Foundational + **US1** (до `T017`).
- Increment 2: добавить межсервисные проверки **US2** (`T018-T023`).
- Increment 3: закрыть E2E-регрессию **US3** (`T024-T029`).
- Finalize: выполнить polish-задачи и зафиксировать отчеты (`T030-T034`).

