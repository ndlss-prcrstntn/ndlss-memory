# Tasks: Reranking поверх hybrid только для markdown-коллекции

**Input**: Документы из `/specs/017-md-hybrid-reranking/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Тесты включены, так как фича меняет публичные search/MCP контракты и должна пройти конституционные quality gates.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет зависимости по незавершенной задаче)
- **[Story]**: Привязка к user story (`[US1]`, `[US2]`, `[US3]`)
- Каждая задача содержит точные абсолютные пути к файлам

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить окружение и контрактные артефакты для docs-only reranking.

- [X] T001 Обновить параметры reranking в `Z:\WORK\ndlss-memory\.env.example`
- [X] T002 Обновить dev-профиль reranking параметрами в `Z:\WORK\ndlss-memory\.env.mcp-dev`
- [X] T003 [P] Обновить документацию конфигурации reranking в `Z:\WORK\ndlss-memory\docs\configuration.md`
- [X] T004 [P] Подготовить baseline контракт reranking в `Z:\WORK\ndlss-memory\services\mcp-server\openapi\mcp-search-tools.openapi.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты reranking, блокирующие все user story.

- [X] T005 Реализовать общий модуль reranking policy и score fusion в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_hybrid.py`
- [X] T006 [P] Подключить reranking configuration/env resolution в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T007 [P] Расширить машиночитаемые коды ошибок reranking в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_errors.py`
- [X] T008 Реализовать response models для reranking полей в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`
- [X] T009 [P] Синхронизировать feature-контракт с базовыми схемами в `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\contracts\md-hybrid-reranking.openapi.yaml`

**Checkpoint**: Базовая reranking-инфраструктура готова, можно реализовывать user stories независимо.

---

## Phase 3: User Story 1 - Улучшить релевантность docs-поиска вторым этапом ранжирования (Priority: P1) MVP

**Goal**: Повысить релевантность top-выдачи docs-search за счет reranking поверх hybrid-кандидатов.

**Independent Test**: На контрольных docs-запросах top-выдача после reranking демонстрирует улучшенный порядок релевантности относительно baseline hybrid.

### Tests for User Story 1

- [X] T010 [P] [US1] Добавить unit-тесты reranking score/fusion в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`
- [X] T011 [P] [US1] Добавить unit-тесты docs reranking response envelope в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_docs_hybrid_search_service.py`
- [X] T012 [P] [US1] Добавить integration-тест reranking positive flow в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 1

- [X] T013 [US1] Реализовать построение candidate-set и reranking stage в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T014 [US1] Реализовать `rankingSignals.rerank` и итоговый score в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`
- [X] T015 [US1] Реализовать docs response strategy marker для reranking в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_service.py`
- [X] T016 [US1] Обновить endpoint docs-search под reranking контракт в `Z:\WORK\ndlss-memory\services\mcp-server\src\system_status_handler.py`
- [X] T017 [US1] Обновить MCP `search_docs` tool под reranking поля ответа в `Z:\WORK\ndlss-memory\services\mcp-server\src\mcp_transport\tools_search.py`

**Checkpoint**: US1 завершена, reranking поверх hybrid работает и улучшает приоритизацию docs-результатов.

---

## Phase 4: User Story 2 - Ограничить reranking только markdown-потоком (Priority: P2)

**Goal**: Обеспечить docs-only scope для reranking без изменений в non-docs поиске.

**Independent Test**: `/v1/search/docs/query` использует reranking, а `/v1/search/semantic` и related non-docs пути сохраняют прежний формат и поведение.

### Tests for User Story 2

- [X] T018 [P] [US2] Добавить unit-регрессию non-docs контракта в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_semantic_search_service.py`
- [X] T019 [P] [US2] Добавить contract-тест docs-only scope для docs-search endpoint в `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`
- [X] T020 [P] [US2] Добавить integration-тест совместимости docs/non-docs поиска в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 2

- [X] T021 [US2] Зафиксировать scope rule reranking только для docs collection в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T022 [US2] Сохранить backward compatibility semantic/docs adapter flow в `Z:\WORK\ndlss-memory\services\mcp-server\src\mcp_transport\service_adapter.py`
- [X] T023 [US2] Уточнить публичный API каталог по docs-only reranking в `Z:\WORK\ndlss-memory\services\mcp-server\src\system_status_handler.py`
- [X] T024 [US2] Обновить сервисный OpenAPI контракт docs-search scope в `Z:\WORK\ndlss-memory\services\mcp-server\openapi\mcp-search-tools.openapi.yaml`

**Checkpoint**: US2 завершена, reranking применяется строго в markdown docs-потоке.

---

## Phase 5: User Story 3 - Стабильный и надежный пользовательский опыт при reranking (Priority: P3)

**Goal**: Обеспечить deterministic выдачу и контролируемый fallback при деградации reranking.

**Independent Test**: Повторные запросы к неизменным данным дают стабильный top-k; при недоступности reranking возвращается валидный fallback-ответ.

### Tests for User Story 3

- [X] T025 [P] [US3] Добавить unit-тесты deterministic tie-break после reranking в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`
- [X] T026 [P] [US3] Добавить contract-тесты fallback и 503 error payload в `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`
- [X] T027 [P] [US3] Добавить integration-тест repeatability и fallback поведения в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 3

- [X] T028 [US3] Реализовать fallback policy при деградации reranking в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_service.py`
- [X] T029 [US3] Реализовать машиночитаемую ошибку `DOCS_RERANKING_UNAVAILABLE` в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_errors.py`
- [X] T030 [US3] Реализовать deterministic sorting policy для reranked результатов в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T031 [US3] Обновить валидацию/форму docs reranking ответа (`fallbackApplied`, strategy marker) в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`

**Checkpoint**: US3 завершена, reranking выдача стабильна и отказоустойчива.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Завершить документацию, quickstart и quality-gate артефакты релизной готовности.

- [X] T032 [P] Обновить пользовательскую документацию reranking в `Z:\WORK\ndlss-memory\README.md`
- [X] T033 [P] Обновить quickstart по reranking flow в `Z:\WORK\ndlss-memory\docs\quickstart.md`
- [X] T034 [P] Синхронизировать feature quickstart с финальными сценариями в `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\quickstart.md`
- [X] T035 Зафиксировать результаты quality verification в `Z:\WORK\ndlss-memory\tests\artifacts\hybrid-reranking\verification-report.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
- User stories стартуют только после завершения Foundational (Phase 2)
- US2 зависит от US1 (использует реализованный reranking pipeline)
- US3 зависит от US1 (использует реализованный reranking scoring/fallback контур)
- После завершения US1 фазы US2 и US3 могут выполняться параллельно по независимым задачам

### User Story Dependency Graph

- US1 -> US2
- US1 -> US3

---

## Parallel Execution Examples

### US1

- Параллельно выполнять `T010`, `T011`, `T012` (разные тестовые файлы).
- После `T013` параллельно выполнять `T014` и `T017`.

### US2

- Параллельно выполнять `T018`, `T019`, `T020`.
- После `T021` параллельно выполнять `T022` и `T024`.

### US3

- Параллельно выполнять `T025`, `T026`, `T027`.
- После `T028` параллельно выполнять `T029` и `T031`.

---

## Implementation Strategy

### MVP First (US1)

1. Завершить Setup и Foundational (Phase 1-2).
2. Реализовать US1 reranking flow и подтвердить quality на тестах `T010-T012`.
3. Зафиксировать MVP как docs-only reranking поверх hybrid candidate retrieval.

### Incremental Delivery

1. Добавить US2 для строгого scope isolation и backward compatibility non-docs.
2. Добавить US3 для deterministic/fallback надежности.
3. Завершить polish: docs, quickstart, verification report.

### Validation Focus

1. Контрактные проверки: `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`.
2. Интеграционные проверки: `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`.
3. Unit-проверки reranking/tie-break: `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`.
