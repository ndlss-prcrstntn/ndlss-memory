# Tasks: MCP-инструменты поиска

**Input**: Документы из `/specs/006-mcp-search-tools/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/mcp-search-tools.openapi.yaml`

**Tests**: Для этой фичи тестовые задачи включены (contract + unit + integration), так как в спецификации есть отдельные acceptance-сценарии и измеримые критерии качества.

**Organization**: Задачи сгруппированы по user stories для независимой реализации и проверки.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить артефакты и каркас для MCP search tools.

- [X] T001 Подготовить каркас search-модулей в `services/mcp-server/src/search_models.py`
- [X] T002 Синхронизировать OpenAPI-контракт MCP поиска в `services/mcp-server/openapi/mcp-search-tools.openapi.yaml`
- [X] T003 [P] Добавить contract checklist для MCP search tools в `tests/contract/mcp_search_tools_contract.md`
- [X] T004 [P] Добавить интеграционный сценарий запуска MCP search tools в `tests/integration/mcp_search_tools_smoke.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты, блокирующие все user stories.

- [X] T005 Реализовать модели запросов/ответов search tools в `services/mcp-server/src/search_models.py`
- [X] T006 Реализовать машиночитаемые ошибки search tools в `services/mcp-server/src/search_errors.py`
- [X] T007 [P] Реализовать репозиторий чтения из Qdrant для search tools в `services/mcp-server/src/search_repository.py`
- [X] T008 [P] Реализовать стабильный разбор `resultId` и связи с источником в `services/mcp-server/src/search_result_ref.py`
- [X] T009 Реализовать общий SearchService для semantic/source/metadata операций в `services/mcp-server/src/search_service.py`
- [X] T010 Подключить базовый wiring search tools в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: После T010 можно независимо реализовывать user stories.

---

## Phase 3: User Story 1 - Семантический поиск по индексу (Priority: P1) MVP

**Goal**: Пользователь получает структурированный semantic search ответ с релевантными результатами и ограничением `limit`.

**Independent Test**: Выполнить `POST /v1/search/semantic` с валидным `query` и проверить, что ответ содержит `status`, `results`, `meta`, а число результатов не превышает limit.

### Tests for User Story 1

- [X] T011 [P] [US1] Добавить контрактные проверки semantic search в `tests/contract/mcp_search_tools_contract.md`
- [X] T012 [P] [US1] Добавить unit-тесты semantic search service (ранжирование и limit) в `tests/unit/mcp_server/test_semantic_search_service.py`
- [X] T013 [P] [US1] Добавить integration-сценарий semantic search в `tests/integration/mcp_search_semantic_flow.md`

### Implementation for User Story 1

- [X] T014 [US1] Реализовать semantic search логику в `services/mcp-server/src/search_service.py`
- [X] T015 [US1] Реализовать Qdrant semantic query + mapping в `services/mcp-server/src/search_repository.py`
- [X] T016 [US1] Добавить endpoint `POST /v1/search/semantic` в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US1 готова как MVP и проверяется отдельно.

---

## Phase 4: User Story 2 - Получение источника и метаданных по ID (Priority: P2)

**Goal**: Пользователь получает source/metadata по `resultId` с предсказуемыми полями и машиночитаемыми ошибками.

**Independent Test**: Взять `resultId` из semantic search и успешно получить `/source` и `/metadata`; при невалидном ID получить корректный error code.

### Tests for User Story 2

- [X] T017 [P] [US2] Добавить контрактные проверки source/metadata endpoints в `tests/contract/mcp_search_tools_contract.md`
- [X] T018 [P] [US2] Добавить unit-тесты resolution и not-found ошибок в `tests/unit/mcp_server/test_search_result_resolution.py`
- [X] T019 [P] [US2] Добавить integration-сценарий поиска по цепочке `search -> source -> metadata` в `tests/integration/mcp_search_traceability_flow.md`

### Implementation for User Story 2

- [X] T020 [US2] Реализовать получение source/metadata по `resultId` в `services/mcp-server/src/search_service.py`
- [X] T021 [US2] Реализовать repository lookup source/metadata в `services/mcp-server/src/search_repository.py`
- [X] T022 [US2] Добавить endpoints `GET /v1/search/results/{resultId}/source` и `GET /v1/search/results/{resultId}/metadata` в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US2 завершена и не ломает MVP semantic search.

---

## Phase 5: User Story 3 - Фильтрация и устойчивость ответов (Priority: P3)

**Goal**: Semantic search поддерживает фильтры `path/folder/fileType` (логическое И) и корректно возвращает `status=empty` при пустой выдаче.

**Independent Test**: Запустить поиск с фильтрами и отдельный запрос без совпадений; убедиться в корректной фильтрации и пустом структурированном ответе без internal error.

### Tests for User Story 3

- [X] T023 [P] [US3] Добавить контрактные проверки фильтров и пустой выдачи в `tests/contract/mcp_search_tools_contract.md`
- [X] T024 [P] [US3] Добавить unit-тесты валидации/комбинации фильтров в `tests/unit/mcp_server/test_semantic_search_filters.py`
- [X] T025 [P] [US3] Добавить integration-сценарий фильтрации и empty-response в `tests/integration/mcp_search_filters_and_empty.md`

### Implementation for User Story 3

- [X] T026 [US3] Реализовать парсинг и валидацию фильтров запроса в `services/mcp-server/src/search_models.py`
- [X] T027 [US3] Реализовать применение фильтров `path/folder/fileType` в Qdrant lookup в `services/mcp-server/src/search_repository.py`
- [X] T028 [US3] Реализовать ответ `status=empty` без error для пустой выдачи в `services/mcp-server/src/search_service.py`

**Checkpoint**: US3 завершена и работает совместно с US1/US2.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная валидация и документация для релиза фичи.

- [X] T029 [P] Обновить пользовательскую документацию MCP search tools в `README.md`
- [X] T030 [P] Актуализировать быстрый сценарий запуска и проверки в `specs/006-mcp-search-tools/quickstart.md`
- [X] T031 Зафиксировать итоговый контракт в общем наборе проверок в `tests/contract/mcp_search_tools_contract.md`
- [X] T032 Выполнить и задокументировать регрессионный прогон фичи в `tests/integration/mcp_search_tools_smoke.md`

---

## Dependencies & Execution Order

- Phase order: Setup -> Foundational -> US1 -> (US2 + US3) -> Polish.
- US1 (MVP) обязательна перед US2 и US3, так как дает базовый `resultId` поток.
- US2 и US3 можно выполнять параллельно после завершения US1 и общих foundational задач.
- Внутри каждой user story: сначала тестовые задачи, затем реализация и интеграция.

## Dependency Graph (User Stories)

- US1 (P1) -> US2 (P2)
- US1 (P1) -> US3 (P3)

## Parallel Execution Examples

- US1: выполнять T011 + T012 + T013 параллельно, затем T014 -> T015 -> T016.
- US2: выполнять T017 + T018 + T019 параллельно, затем T020 -> T021 -> T022.
- US3: выполнять T023 + T024 + T025 параллельно, затем T026 -> T027 -> T028.

## Implementation Strategy

- MVP first: завершить Phase 1-3 (через US1) и получить рабочий semantic search.
- Increment 2: добавить traceability по `resultId` (US2) без изменения внешнего контракта US1.
- Increment 3: добавить фильтры и empty-result поведение (US3), затем пройти общий polish/regression.

