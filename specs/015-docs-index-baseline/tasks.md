# Tasks: Docs collection indexing + baseline docs search

**Input**: Документы из `/specs/015-docs-index-baseline/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Тесты включены, так как фича меняет критичный индексатор, MCP-инструменты и публичные API-контракты.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет зависимости по незавершенной задаче)
- **[Story]**: Привязка к user story (`[US1]`, `[US2]`)
- Каждая задача содержит точные пути к файлам

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить конфигурацию окружения и compose-пресеты для docs-коллекции и docs-поиска.

- [X] T001 Добавить переменные docs-индексации и docs-коллекции в `.env.example`
- [X] T002 Добавить проброс docs-переменных в `infra/docker/docker-compose.yml`
- [X] T003 [P] Добавить проброс docs-переменных в `deploy/compose/generic.yml`, `deploy/compose/python.yml`, `deploy/compose/typescript.yml`, `deploy/compose/javascript.yml`, `deploy/compose/java-kotlin.yml`, `deploy/compose/csharp.yml`, `deploy/compose/go.yml`
- [X] T004 [P] Добавить проброс docs-переменных в `deploy/compose-images/generic.yml`, `deploy/compose-images/python.yml`, `deploy/compose-images/typescript.yml`, `deploy/compose-images/javascript.yml`, `deploy/compose-images/java-kotlin.yml`, `deploy/compose-images/csharp.yml`, `deploy/compose-images/go.yml`
- [X] T005 [P] Добавить валидацию docs-переменных в `services/file-indexer/scripts/validate-config.sh` и `services/file-indexer/scripts/entrypoint.sh`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты docs-коллекции, блокирующие обе user story.

- [X] T006 Реализовать конфигурацию docs-коллекции и ее резолвинг из окружения в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py` и `services/mcp-server/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T007 [P] Реализовать bootstrap-создание docs-коллекции на старте в `services/mcp-server/src/bootstrap_collection_service.py` и `services/mcp-server/src/bootstrap_orchestrator.py`
- [X] T008 [P] Реализовать runtime self-heal docs-коллекции при `404` в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py` и `services/mcp-server/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T009 Реализовать общий формат состояния/summary docs-индексации в `services/file-indexer/src/ingestion_pipeline/run_summary.py` и `services/mcp-server/src/ingestion_state.py`
- [X] T010 [P] Добавить docs-коды причин пропуска и ошибки в `services/file-indexer/src/skip_reasons.py` и `services/mcp-server/src/ingestion_errors.py`
- [X] T011 [P] Добавить docs-команды в корневой API-каталог в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: Базовые компоненты docs-коллекции готовы, можно реализовывать user stories.

---

## Phase 3: User Story 1 - Изолированная индексация документации (Priority: P1) MVP

**Goal**: Индексировать markdown-документацию в отдельную коллекцию без смешивания с кодовыми чанками.

**Independent Test**: На смешанном репозитории docs-индексация включает только markdown-документы, повторный запуск без изменений не создает дубликаты.

### Tests for User Story 1

- [X] T012 [P] [US1] Добавить unit-тесты отбора markdown и ключей `path + stable chunk index` в `tests/unit/file_indexer/test_docs_index_selection.py`
- [X] T013 [P] [US1] Добавить integration-тест изолированной docs-индексации в `tests/integration/test_docs_indexing_full_scan_isolation.py`
- [X] T014 [P] [US1] Добавить integration-тест идемпотентности docs-индексации при повторном запуске в `tests/integration/test_docs_indexing_repeat_idempotency.py`
- [X] T015 [P] [US1] Добавить contract-тесты API docs-индексации (`start/summary`) в `tests/contract/test_docs_indexing_contract.py`

### Implementation for User Story 1

- [X] T016 [US1] Реализовать markdown-only отбор документов для docs-режима в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T017 [US1] Реализовать правила уникальности документа и чанка (`normalized path`, `path + stable chunk index`) в `services/file-indexer/src/ingestion_pipeline/chunk_identity.py` и `services/mcp-server/src/ingestion_pipeline/chunk_identity.py`
- [X] T018 [US1] Реализовать запуск docs-индексации через API endpoint в `services/mcp-server/src/system_status_handler.py`
- [X] T019 [US1] Реализовать endpoint получения summary docs-индексации в `services/mcp-server/src/system_status_handler.py`
- [X] T020 [US1] Реализовать подсчет `processed/indexed/updated/skipped/deleted` и skip breakdown для docs-запусков в `services/file-indexer/src/ingestion_pipeline/run_summary.py` и `services/mcp-server/src/ingestion_state.py`
- [X] T021 [US1] Реализовать защиту backward compatibility для существующих `full-scan` и `ingestion` эндпоинтов в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US1 завершена, docs-индексация работает отдельно и идемпотентно.

---

## Phase 4: User Story 2 - Базовый поиск только по документации (Priority: P2)

**Goal**: Добавить отдельный baseline docs-поиск и MCP-доступ к нему без влияния на существующий code-search.

**Independent Test**: Docs-запросы возвращают только документацию, пустые запросы/результаты обрабатываются корректно, top-k стабилен при неизменных данных.

### Tests for User Story 2

- [X] T022 [P] [US2] Добавить unit-тесты docs-репозитория поиска (docs collection + deterministic order) в `tests/unit/mcp_server/test_search_repository_docs.py`
- [X] T023 [P] [US2] Добавить integration-тесты docs-поиска (positive + empty) в `tests/integration/test_docs_search_baseline.py`
- [X] T024 [P] [US2] Добавить contract-тесты endpoint `/v1/search/docs/query` и error payload в `tests/contract/test_docs_search_contract.py`
- [X] T025 [P] [US2] Добавить unit-тесты регистрации/вызова MCP tool для docs-поиска в `tests/unit/mcp_server/test_mcp_docs_search_tool.py`

### Implementation for User Story 2

- [X] T026 [US2] Реализовать модели запроса/ответа docs-поиска в `services/mcp-server/src/search_models.py`
- [X] T027 [US2] Реализовать docs-only поисковый запрос в отдельную коллекцию в `services/mcp-server/src/search_repository.py`
- [X] T028 [US2] Реализовать сервисную логику baseline docs-поиска в `services/mcp-server/src/search_service.py`
- [X] T029 [US2] Реализовать HTTP endpoint `/v1/search/docs/query` и машиночитаемые ошибки в `services/mcp-server/src/system_status_handler.py` и `services/mcp-server/src/search_errors.py`
- [X] T030 [US2] Зарегистрировать MCP инструмент docs-поиска в `services/mcp-server/src/mcp_transport/tool_registry.py` и `services/mcp-server/src/mcp_transport/tools_search.py`
- [X] T031 [US2] Подключить docs-поиск в MCP adapter/dispatcher в `services/mcp-server/src/mcp_transport/service_adapter.py` и `services/mcp-server/src/mcp_transport/method_handlers.py`

**Checkpoint**: US2 завершена, docs-поиск доступен по API и MCP, основной code-search не затронут.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Синхронизировать контракты, документацию и quality gates для релизной готовности.

- [X] T032 [P] Синхронизировать сервисные OpenAPI спецификации в `services/mcp-server/openapi/chunking-embeddings.openapi.yaml` и `services/mcp-server/openapi/mcp-search-tools.openapi.yaml`
- [X] T033 [P] Синхронизировать feature-контракт и quickstart в `specs/015-docs-index-baseline/contracts/docs-index-baseline.openapi.yaml` и `specs/015-docs-index-baseline/quickstart.md`
- [X] T034 Обновить пользовательскую документацию в `README.md`, `docs/configuration.md`, `docs/quickstart.md`, `docs/compose-presets.md`
- [X] T035 Выполнить quality suite и зафиксировать артефакты в `tests/artifacts/quality-stability/quality-run-report.json` и `tests/artifacts/quality-stability/final-regression-log.md`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5
- User stories стартуют только после завершения Foundational (Phase 2)
- US2 зависит от US1, так как baseline docs-поиск требует готовой docs-коллекции и данных
- Внутри каждой user story: тесты до финальной интеграции и документации

### User Story Dependency Graph

- US1 -> US2

---

## Parallel Execution Examples

### US1

- Параллельно запускать `T012`, `T013`, `T014`, `T015` (разные тестовые файлы).
- После `T016` параллельно выполнять `T018` и `T020`.

### US2

- Параллельно запускать `T022`, `T023`, `T024`, `T025`.
- После `T027` параллельно выполнять `T029` и `T030`.

---

## Implementation Strategy

### MVP First (US1)

1. Завершить Setup и Foundational (Phase 1-2).
2. Реализовать US1 (Phase 3) и подтвердить независимыми unit/integration/contract тестами.
3. Зафиксировать MVP как отдельную docs-индексацию с идемпотентностью и предсказуемым summary.

### Incremental Delivery

1. Добавить US2 (baseline docs-поиск по API и MCP).
2. Синхронизировать OpenAPI/документацию и пройти quality suite.
3. Подготовить базу для следующего этапа (hybrid + rerank только для docs-коллекции).
