# Tasks: Предполетные проверки старта и сводка готовности

**Input**: Documents from `/specs/011-startup-preflight-summary/`
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Включены unit/integration/contract задачи, т.к. фича меняет startup-критичный путь и системные контракты.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить общие заготовки для preflight/release-проверок.

- [X] T001 Подготовить feature test-каркас в `tests/contract/startup_preflight_readiness_contract.md` и `tests/integration/startup_preflight_readiness.md`
- [X] T002 [P] Добавить startup preflight переменные в `.env.example` и `.env.minimal.example`
- [X] T003 [P] Добавить шаблон smoke-скрипта preflight в `scripts/tests/startup_preflight_smoke.ps1`
- [X] T004 Обновить сценарий quality-артефактов для новой фичи в `tests/artifacts/quality-stability/.gitkeep`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ввести общие модели и проверки, блокирующие все user stories.

- [X] T005 Создать модели preflight/readiness в `services/mcp-server/src/startup_preflight_models.py`
- [X] T006 [P] Реализовать проверки Qdrant/workspace/git в `services/mcp-server/src/startup_preflight_checks.py`
- [X] T007 Реализовать fail-fast ошибки preflight в `services/mcp-server/src/startup_preflight_errors.py`
- [X] T008 Реализовать runtime-state preflight/readiness в `services/mcp-server/src/startup_preflight_state.py`
- [X] T009 [P] Добавить shell preflight-проверки для индексатора в `services/file-indexer/scripts/startup-preflight.sh`
- [X] T010 Интегрировать вызов preflight в startup индексатора в `services/file-indexer/scripts/entrypoint.sh`
- [X] T011 [P] Добавить unit-тесты для базовых preflight сущностей в `tests/unit/mcp_server/test_startup_preflight_models.py`

**Checkpoint**: Общий preflight-слой готов для story-реализаций.

---

## Phase 3: User Story 1 - Проверка готовности окружения до старта (Priority: P1) MVP

**Goal**: Блокировать запуск при недоступных критичных зависимостях и возвращать структурированную fail-fast ошибку.

**Independent Test**: Запуск с недоступным Qdrant/невалидным workspace/git в delta-режиме завершается до ready с машиночитаемой ошибкой.

### Tests for User Story 1

- [X] T012 [P] [US1] Добавить unit-тесты preflight-провалов в `tests/unit/mcp_server/test_startup_preflight_checks.py`
- [X] T013 [P] [US1] Добавить integration-сценарии fail-fast в `tests/integration/startup_preflight_readiness.md`
- [X] T014 [P] [US1] Добавить contract-проверки error model в `tests/contract/startup_preflight_readiness_contract.md`

### Implementation for User Story 1

- [X] T015 [US1] Подключить preflight до старта API в `services/mcp-server/src/system_status_handler.py`
- [X] T016 [US1] Добавить формирование `StartupFailureReport` в `services/mcp-server/src/startup_preflight_errors.py` и `services/mcp-server/src/system_status_handler.py`
- [X] T017 [US1] Добавить определение git-required режима в `services/mcp-server/src/startup_preflight_checks.py`
- [X] T018 [US1] Добавить fail-fast поведение для индексатора при провале preflight в `services/file-indexer/scripts/startup-preflight.sh` и `services/file-indexer/scripts/entrypoint.sh`
- [X] T019 [US1] Добавить сценарий запуска US1 smoke-скрипта в `scripts/tests/startup_preflight_smoke.ps1`

**Checkpoint**: US1 завершена, если невалидное окружение не проходит в рабочий режим.

---

## Phase 4: User Story 2 - Единая сводка готовности после успешного старта (Priority: P2)

**Goal**: После успешного старта выдавать единую, стабильную startup-ready сводку в API и логах.

**Independent Test**: В валидной среде endpoint readiness и логи возвращают полный набор полей (`serviceReadiness`, `workspacePath`, `indexMode`, `mcpEndpoint`, `collectionName`).

### Tests for User Story 2

- [X] T020 [P] [US2] Добавить unit-тесты сборки startup summary в `tests/unit/mcp_server/test_startup_readiness_summary.py`
- [X] T021 [P] [US2] Добавить integration-проверки ready summary endpoint/logs в `tests/integration/startup_preflight_readiness.md`
- [X] T022 [P] [US2] Добавить contract-проверки `/v1/system/startup/readiness` в `tests/contract/startup_preflight_readiness_contract.md`

### Implementation for User Story 2

- [X] T023 [US2] Реализовать сборщик `StartupReadinessSummary` в `services/mcp-server/src/startup_readiness_summary.py`
- [X] T024 [US2] Добавить endpoint `GET /v1/system/startup/readiness` в `services/mcp-server/src/system_status_handler.py`
- [X] T025 [US2] Расширить `GET /v1/system/config` startup-диагностикой в `services/mcp-server/src/system_status_handler.py`
- [X] T026 [US2] Добавить единый startup-ready лог в `services/mcp-server/src/system_status_handler.py` и `services/file-indexer/scripts/entrypoint.sh`

**Checkpoint**: US2 завершена, если оператор видит готовность в одном месте без дополнительных запросов.

---

## Phase 5: User Story 3 - Обратная совместимость существующих сценариев запуска (Priority: P3)

**Goal**: Сохранить работу текущих preset-сценариев и существующих API после внедрения preflight/readiness.

**Independent Test**: Запуск по текущим compose preset успешен, базовые endpoint (`/health`, `/v1/system/status`, `/v1/system/config`, `/v1/search/semantic`) не ломаются.

### Tests for User Story 3

- [X] T027 [P] [US3] Добавить regression-сценарий совместимости preset-запуска в `tests/integration/startup_preflight_readiness.md`
- [X] T028 [P] [US3] Добавить smoke-скрипт совместимости endpoint в `scripts/tests/us3_startup_backward_compat.ps1`

### Implementation for User Story 3

- [X] T029 [US3] Прокинуть preflight env-параметры в `docker-compose.yml`, `deploy/compose/generic.yml`, `deploy/compose/python.yml`, `deploy/compose/javascript.yml`, `deploy/compose/typescript.yml`, `deploy/compose/csharp.yml`, `deploy/compose/go.yml`, `deploy/compose/java-kotlin.yml`
- [X] T030 [US3] Синхронизировать image-presets по preflight env в `deploy/compose-images/generic.yml`, `deploy/compose-images/python.yml`, `deploy/compose-images/javascript.yml`, `deploy/compose-images/typescript.yml`, `deploy/compose-images/csharp.yml`, `deploy/compose-images/go.yml`, `deploy/compose-images/java-kotlin.yml`
- [X] T031 [US3] Обновить API контракт наблюдаемости старта в `services/mcp-server/openapi/compose-observability.openapi.yaml` и `specs/011-startup-preflight-summary/contracts/startup-preflight-readiness.openapi.yaml`
- [X] T032 [US3] Обновить пользовательскую документацию запуска в `README.md`, `docs/quickstart.md`, `docs/configuration.md`, `docs/compose-presets.md`

**Checkpoint**: US3 завершена, если существующий пользовательский запуск работает без миграции.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Закрыть регрессию, quality gates и релизную готовность.

- [X] T033 [P] Добавить запуск startup preflight smoke в `scripts/tests/run_quality_stability_suite.ps1`
- [X] T034 Добавить gate-проверку startup preflight в `scripts/tests/quality_gate_runner.ps1`
- [X] T035 [P] Обновить feature quickstart в `specs/011-startup-preflight-summary/quickstart.md`
- [X] T036 Подготовить changelog запись по фиче в `CHANGELOG.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 (US1) -> Phase 4 (US2) -> Phase 5 (US3) -> Phase 6
- US1 является MVP и обязательна перед US2/US3.
- US2 зависит от результатов US1 (preflight state + fail-fast модель).
- US3 зависит от стабилизации US1 и US2.

## Dependency Graph

- `US1 -> US2 -> US3`

## Parallel Execution Examples

- **US1**: выполнять `T012`, `T013`, `T014` параллельно; затем `T015`-`T019` последовательно.
- **US2**: выполнять `T020`, `T021`, `T022` параллельно; затем `T023`-`T026` последовательно.
- **US3**: выполнять `T027` и `T028` параллельно; затем `T029` и `T030` параллельно; затем `T031` и `T032`.

## Implementation Strategy

1. Доставить MVP: завершить Phase 1-2 и US1.
2. Добавить наблюдаемость готовности: реализовать US2.
3. Зафиксировать обратную совместимость preset и API: реализовать US3.
4. Закрыть quality gates и релизные хвосты в Polish phase.
