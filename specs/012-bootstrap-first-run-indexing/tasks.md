# Tasks: Bootstrap первого запуска индексации

**Input**: Документы из `/specs/012-bootstrap-first-run-indexing/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/first-run-bootstrap.openapi.yaml`, `quickstart.md`

**Tests**: Добавлены обязательные unit/integration/contract проверки для требований конституции и критериев успеха фичи.

**Organization**: Задачи сгруппированы по user story, чтобы каждая история реализовывалась и тестировалась независимо.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить среду и общие артефакты для реализации bootstrap.

- [X] T001 Добавить переменные bootstrap-конфигурации в `docker-compose.yml`
- [X] T002 [P] Добавить переменные bootstrap-конфигурации в `deploy/compose-images/generic.yml`
- [X] T003 [P] Добавить переменные bootstrap-конфигурации в `deploy/compose-images/typescript.yml`
- [X] T004 [P] Добавить переменные bootstrap-конфигурации в `deploy/compose-images/csharp.yml`
- [X] T005 Обновить примеры переменных bootstrap в `.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать базовые компоненты bootstrap, используемые всеми user story.

- [X] T006 Создать модель состояния bootstrap в `services/mcp-server/src/bootstrap_state.py`
- [X] T007 Создать репозиторий marker-состояния bootstrap в `services/mcp-server/src/bootstrap_state_repository.py`
- [X] T008 Создать сервис проверки/создания коллекции в `services/mcp-server/src/bootstrap_collection_service.py`
- [X] T009 Создать координатор первого запуска в `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T010 Интегрировать bootstrap-конфиг в runtime-конфигурацию в `services/mcp-server/src/system_status_handler.py`
- [X] T011 [P] Добавить unit-тесты для bootstrap моделей и репозитория в `tests/unit/mcp_server/test_bootstrap_state.py`
- [X] T012 [P] Добавить unit-тесты ensure-collection логики в `tests/unit/mcp_server/test_bootstrap_collection_service.py`

**Checkpoint**: Базовая инфраструктура bootstrap готова для реализации пользовательских сценариев.

---

## Phase 3: User Story 1 - Поиск готов после первого старта (Priority: P1)

**Goal**: На новом workspace индекс становится пригодным к поиску без ручного вызова ingestion.

**Independent Test**: Запустить стек на пустой среде и убедиться, что коллекция создана, bootstrap выполнен и semantic search возвращает результат без ручного `POST /v1/indexing/ingestion/jobs`.

### Tests for User Story 1

- [X] T013 [P] [US1] Добавить contract-тест startup readiness bootstrap блока в `tests/contract/test_startup_readiness_bootstrap_contract.py`
- [X] T014 [P] [US1] Добавить integration-тест auto-bootstrap первого запуска в `tests/integration/test_first_run_bootstrap.py`
- [X] T015 [P] [US1] Добавить smoke-сценарий compose first-run bootstrap в `scripts/tests/startup_bootstrap_smoke.ps1`

### Implementation for User Story 1

- [X] T016 [US1] Подключить авто-bootstrap на старте приложения в `services/mcp-server/src/system_status_handler.py`
- [X] T017 [US1] Реализовать авто-старт ingestion из bootstrap coordinator в `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T018 [US1] Расширить статус ingestion bootstrap-контекстом в `services/mcp-server/src/ingestion_state.py`
- [X] T019 [US1] Добавить bootstrap-поля в `/v1/indexing/ingestion/jobs/{runId}` и `/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T020 [US1] Обновить OpenAPI контракты bootstrap endpoint в `services/mcp-server/openapi/compose-observability.openapi.yaml`
- [X] T021 [US1] Синхронизировать feature-контракт bootstrap в `specs/012-bootstrap-first-run-indexing/contracts/first-run-bootstrap.openapi.yaml`

**Checkpoint**: Первый запуск без ручного ingestion работает и подтверждается контрактом/интеграцией.

---

## Phase 4: User Story 2 - Идемпотентный перезапуск (Priority: P2)

**Goal**: Повторные рестарты не запускают дорогой bootstrap заново и не создают дубли.

**Independent Test**: Выполнить несколько рестартов без изменений и подтвердить `bootstrap.decision=skip-already-completed` и отсутствие роста `points/count` из-за повторного полного bootstrap.

### Tests for User Story 2

- [X] T022 [P] [US2] Добавить unit-тесты decision-логики skip/retry в `tests/unit/mcp_server/test_bootstrap_orchestrator.py`
- [X] T023 [P] [US2] Добавить integration-тест restart-идемпотентности bootstrap в `tests/integration/test_bootstrap_restart_idempotency.py`
- [X] T024 [P] [US2] Добавить integration-тест нестандартного внешнего Qdrant порта в `tests/integration/test_bootstrap_with_custom_qdrant_port.py`

### Implementation for User Story 2

- [X] T025 [US2] Реализовать персистентный bootstrap-marker и статус `completed` в `services/mcp-server/src/bootstrap_state_repository.py`
- [X] T026 [US2] Реализовать skip повторного bootstrap при restart в `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T027 [US2] Добавить защиту от конкурентного повторного auto-bootstrap в `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T028 [US2] Добавить bootstrap-decision в startup readiness summary в `services/mcp-server/src/startup_readiness_summary.py`
- [X] T029 [US2] Обновить Quickstart проверкой restart-идемпотентности в `specs/012-bootstrap-first-run-indexing/quickstart.md`

**Checkpoint**: Рестарты не дублируют expensive bootstrap и это подтверждено автотестами.

---

## Phase 5: User Story 3 - Прозрачный статус bootstrap (Priority: P3)

**Goal**: Оператор видит явный bootstrap-статус и причины сбоев в логах и endpoint.

**Independent Test**: Смоделировать сбой bootstrap и проверить, что API и логи возвращают структурированную ошибку и actionable-причину.

### Tests for User Story 3

- [X] T030 [P] [US3] Добавить contract-тесты bootstrap failure report в `tests/contract/test_bootstrap_failure_contract.py`
- [X] T031 [P] [US3] Добавить integration-тест fail-fast bootstrap диагностики в `tests/integration/test_bootstrap_failfast_observability.py`

### Implementation for User Story 3

- [X] T032 [US3] Добавить structured logging событий bootstrap в `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T033 [US3] Расширить `/v1/system/startup/readiness` bootstrap failure деталями в `services/mcp-server/src/system_status_handler.py`
- [X] T034 [US3] Обновить ошибки bootstrap и actionable-поля в `services/mcp-server/src/startup_preflight_errors.py`
- [X] T035 [US3] Обновить документацию bootstrap статусов в `docs/configuration.md`
- [X] T036 [US3] Обновить пользовательский quickstart в `README.md`

**Checkpoint**: Наблюдаемость bootstrap прозрачна для оператора в логах и API.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Завершить интеграцию, регрессии и документацию перед релизом.

- [X] T037 [P] Добавить регрессионный запуск bootstrap-suite в `scripts/tests/run_quality_stability_suite.ps1`
- [X] T038 Синхронизировать roadmap статусы по фиче в `docs/roadmaps/0.3.0.md`
- [X] T039 [P] Обновить changelog для bootstrap-фичи в `CHANGELOG.md`
- [X] T040 Проверить UTF-8 кодировку markdown/yaml артефактов в `scripts/tests/verify_utf8_encoding.ps1`
- [X] T041 Выполнить финальный quickstart smoke и зафиксировать результат в `specs/012-bootstrap-first-run-indexing/quickstart.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
- US1 (Phase 3) является MVP и может быть выпущена отдельно после прохождения ее тестов.
- US2 зависит от базовой логики US1 (bootstrap run + summary), поэтому идет после US1.
- US3 зависит от US1/US2 только в части готовых bootstrap-событий и failure-модели.

## User Story Dependency Graph

- US1 -> US2 -> US3

## Parallel Execution Examples

### US1

- Запустить параллельно `T013`, `T014`, `T015` (разные тестовые файлы/скрипт).
- После `T016` параллельно выполнять `T018` и `T020`.

### US2

- Запустить параллельно `T022`, `T023`, `T024`.
- После `T025` параллельно выполнять `T028` и `T029`.

### US3

- Запустить параллельно `T030` и `T031`.
- После `T032` параллельно выполнять `T035` и `T036`.

## Implementation Strategy

### MVP First (US1)

1. Завершить Phase 1 и Phase 2.
2. Полностью реализовать Phase 3 (US1) и убедиться, что fresh workspace становится searchable без ручного API.
3. При необходимости выпустить инкремент как MVP.

### Incremental Delivery

1. Добавить US2 для исключения повторного дорогого bootstrap на рестартах.
2. Добавить US3 для полной наблюдаемости и fail-fast диагностики.
3. Завершить polish, регрессии и документацию.

