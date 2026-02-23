# Tasks: Hybrid search (BM25 + vector) только для md коллекции

**Input**: Документы из `/specs/016-md-hybrid-search/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Тесты включены, так как фича меняет MCP/API-контракт поиска и должна пройти конституционные quality gates.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет зависимости по незавершенной задаче)
- **[Story]**: Привязка к user story (`[US1]`, `[US2]`, `[US3]`)
- Каждая задача содержит точные абсолютные пути к файлам

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить конфигурацию и базовые артефакты для внедрения hybrid docs-search.

- [X] T001 Добавить переменные окружения для hybrid docs-search в `Z:\WORK\ndlss-memory\.env.example`
- [X] T002 Добавить dev-значения переменных hybrid docs-search в `Z:\WORK\ndlss-memory\.env.mcp-dev`
- [X] T003 [P] Обновить описание параметров hybrid docs-search в `Z:\WORK\ndlss-memory\docs\configuration.md`
- [X] T004 [P] Подготовить базовый OpenAPI каркас hybrid docs-search в `Z:\WORK\ndlss-memory\services\mcp-server\openapi\mcp-search-tools.openapi.yaml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты ранжирования и контрактов, блокирующие все user story.

- [X] T005 Реализовать общий модуль fusion/tie-break логики в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_hybrid.py`
- [X] T006 [P] Подключить конфигурацию hybrid ранжирования в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T007 [P] Расширить машиночитаемые ошибки docs-search в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_errors.py`
- [X] T008 Добавить модели hybrid docs response в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`
- [X] T009 [P] Синхронизировать feature-контракт с базовыми схемами в `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\contracts\md-hybrid-search.openapi.yaml`

**Checkpoint**: Общая основа готова, можно реализовывать user stories независимо.

---

## Phase 3: User Story 1 - Найти релевантный markdown-контент по сложному запросу (Priority: P1) MVP

**Goal**: Пользователь получает релевантный hybrid-результат по docs-запросу за счет объединения BM25 и vector сигналов.

**Independent Test**: На контрольных markdown-запросах релевантные результаты стабильно попадают в top выдачи и содержат признаки обоих сигналов ранжирования.

### Tests for User Story 1

- [X] T010 [P] [US1] Добавить unit-тесты fusion-ранжирования и весов сигналов в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`
- [X] T011 [P] [US1] Добавить unit-тесты envelope hybrid-ответа (`appliedStrategy`, `rankingSignals`) в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_docs_hybrid_search_service.py`
- [X] T012 [P] [US1] Добавить integration-тест позитивного hybrid docs-search сценария в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 1

- [X] T013 [US1] Реализовать получение и объединение lexical/vector кандидатов для docs-поиска в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T014 [US1] Реализовать формирование hybrid результата с `rankingSignals` в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`
- [X] T015 [US1] Реализовать возврат hybrid envelope (`appliedStrategy`, `total`, `results`) в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_service.py`
- [X] T016 [US1] Актуализировать endpoint `/v1/search/docs/query` под hybrid ответ в `Z:\WORK\ndlss-memory\services\mcp-server\src\system_status_handler.py`
- [X] T017 [US1] Обновить MCP docs-search tool на hybrid-поля ответа в `Z:\WORK\ndlss-memory\services\mcp-server\src\mcp_transport\tools_search.py`

**Checkpoint**: US1 завершена, hybrid docs-search дает релевантные результаты в целевой форме ответа.

---

## Phase 4: User Story 2 - Ограничить гибридный режим только markdown-областью (Priority: P2)

**Goal**: Гибридный режим работает только для docs-поиска и не меняет поведение non-docs поиска.

**Independent Test**: Запросы в `/v1/search/docs/query` используют hybrid docs-flow, а `/v1/search/semantic` и прочие non-docs сценарии остаются без поведенческих изменений.

### Tests for User Story 2

- [X] T018 [P] [US2] Добавить unit-регрессию неизменности non-docs semantic search в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_semantic_search_service.py`
- [X] T019 [P] [US2] Добавить contract-тест изоляции docs-only scope для `/v1/search/docs/query` в `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`
- [X] T020 [P] [US2] Добавить integration-тест совместимости docs и semantic endpoint-ов в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 2

- [X] T021 [US2] Зафиксировать docs-only маршрутизацию в docs collection для hybrid-поиска в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T022 [US2] Сохранить backward compatibility adapter-потока semantic/docs в `Z:\WORK\ndlss-memory\services\mcp-server\src\mcp_transport\service_adapter.py`
- [X] T023 [US2] Уточнить публичный каталог API о docs-only hybrid scope в `Z:\WORK\ndlss-memory\services\mcp-server\src\system_status_handler.py`
- [X] T024 [US2] Обновить сервисный OpenAPI-контракт по области действия docs-only hybrid в `Z:\WORK\ndlss-memory\services\mcp-server\openapi\mcp-search-tools.openapi.yaml`

**Checkpoint**: US2 завершена, граница применения hybrid режима строго ограничена markdown-коллекцией.

---

## Phase 5: User Story 3 - Предсказуемость и прозрачность результата для пользователя (Priority: P3)

**Goal**: Поиск стабилен при повторе запроса и корректно обрабатывает пустые/невалидные сценарии без деградации UX.

**Independent Test**: При неизменных данных повторный docs-запрос возвращает стабильный top-k, пустой результат и ошибки валидации возвращаются в предсказуемом формате.

### Tests for User Story 3

- [X] T025 [P] [US3] Добавить unit-тесты deterministic tie-break (`documentPath`, `chunkIndex`) в `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`
- [X] T026 [P] [US3] Добавить contract-тесты 400/503 error payload для docs-search в `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`
- [X] T027 [P] [US3] Добавить integration-тест repeatable top-k и empty response в `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`

### Implementation for User Story 3

- [X] T028 [US3] Реализовать стабильный tie-break и детерминированную сортировку равных score в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_repository.py`
- [X] T029 [US3] Реализовать контролируемые empty/availability ответы docs-search в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_service.py`
- [X] T030 [US3] Обновить маппинг кодов ошибок docs-search для API и MCP в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_errors.py`
- [X] T031 [US3] Синхронизировать валидацию `query`/`limit` и формат ошибок в `Z:\WORK\ndlss-memory\services\mcp-server\src\search_models.py`

**Checkpoint**: US3 завершена, выдача и ошибки предсказуемы и стабильны.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Завершить документацию, контракты и quality-gate артефакты.

- [X] T032 [P] Обновить пользовательскую документацию по hybrid docs-search в `Z:\WORK\ndlss-memory\README.md`
- [X] T033 [P] Обновить шаги проверки hybrid docs-search в `Z:\WORK\ndlss-memory\docs\quickstart.md`
- [X] T034 [P] Синхронизировать feature quickstart с финальными сценариями в `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\quickstart.md`
- [X] T035 Зафиксировать итоговую валидацию quality gates в `Z:\WORK\ndlss-memory\tests\artifacts\hybrid-search\verification-report.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
- User stories стартуют только после завершения Phase 2
- US2 зависит от US1 (использует реализованный hybrid docs-flow)
- US3 зависит от US1 (использует реализованный hybrid scoring pipeline)
- US2 и US3 могут выполняться параллельно после US1 при разделении задач по файлам

### User Story Dependency Graph

- US1 -> US2
- US1 -> US3

---

## Parallel Execution Examples

### US1

- Параллельно выполнять `T010`, `T011`, `T012` (разные тестовые файлы).
- После `T013` параллельно выполнять `T014` и `T017`.

### US2

- Параллельно выполнять `T018`, `T019`, `T020` (unit/contract/integration).
- После `T021` параллельно выполнять `T022` и `T024`.

### US3

- Параллельно выполнять `T025`, `T026`, `T027`.
- После `T028` параллельно выполнять `T030` и `T031`.

---

## Implementation Strategy

### MVP First (US1)

1. Завершить Setup и Foundational (Phase 1-2).
2. Реализовать US1 и подтвердить релевантность/формат hybrid ответа тестами `T010-T012`.
3. Зафиксировать MVP как рабочий hybrid docs-search для markdown-коллекции.

### Incremental Delivery

1. Добавить US2 (строгая изоляция docs-only, без регрессий non-docs).
2. Добавить US3 (детерминизм, прозрачные empty/error сценарии).
3. Завершить polish (документация, quickstart, quality-gate отчет).

### Validation Focus

1. Контрактные проверки: `Z:\WORK\ndlss-memory\tests\contract\test_docs_search_contract.py`.
2. Интеграционные проверки: `Z:\WORK\ndlss-memory\tests\integration\test_docs_search_hybrid.py`.
3. Unit-регрессии ранжирования: `Z:\WORK\ndlss-memory\tests\unit\mcp_server\test_search_repository_docs.py`.

