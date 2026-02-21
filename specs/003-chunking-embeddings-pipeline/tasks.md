# Tasks: Пайплайн чанкинга и эмбеддингов

**Input**: Документы из `/specs/003-chunking-embeddings-pipeline/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты включены, так как конституция требует проверок индексации,
контрактов MCP/API, compose запуска и регрессий обоих режимов индексатора.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: можно выполнять параллельно (разные файлы, нет блокирующих зависимостей)
- **[Story]**: метка user story (`[US1]`, `[US2]`, `[US3]`)
- В каждой задаче указан точный путь к файлу

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить каркас пайплайна chunking/embeddings и тестового окружения

- [X] T001 Создать каркас модуля ingestion pipeline в `services/file-indexer/src/ingestion_pipeline/__init__.py`
- [X] T002 [P] Добавить шаблон фикстур для chunking/embedding тестов в `tests/fixtures/chunking-embeddings/fixture-manifest.md`
- [X] T003 [P] Добавить скрипт подготовки фикстур ingestion-тестов в `scripts/tests/ingestion_test_env.ps1`
- [X] T004 [P] Добавить env-переменные chunking/retry в `.env.example`
- [X] T005 [P] Обновить документацию параметров пайплайна в `docs/configuration.md`
- [X] T006 [P] Создать базовый контрактный smoke-сценарий ingestion API в `tests/contract/ingestion_pipeline_contract_smoke.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты, блокирующие все user stories

- [X] T007 Расширить runtime-схему параметров chunking/retry в `services/file-indexer/config/runtime-config.schema.json`
- [X] T008 Реализовать валидацию параметров chunk_size/overlap/retry в `services/file-indexer/scripts/validate-config.sh`
- [X] T009 [P] Подключить env-параметры ingestion pipeline в `infra/docker/docker-compose.yml`
- [X] T010 Реализовать модели `ChunkingConfig` и `ChunkRecord` в `services/file-indexer/src/ingestion_pipeline/chunk_models.py`
- [X] T011 [P] Реализовать модели `EmbeddingTask` и `VectorRecord` в `services/file-indexer/src/ingestion_pipeline/embedding_models.py`
- [X] T012 Реализовать in-memory состояние ingestion run в `services/mcp-server/src/ingestion_state.py`
- [X] T013 [P] Реализовать общий error-model ingestion API в `services/mcp-server/src/ingestion_errors.py`
- [X] T014 Добавить каркас ingestion endpoints в `services/mcp-server/src/system_status_handler.py`
- [X] T015 Синхронизировать runtime OpenAPI ingestion контракта в `services/mcp-server/openapi/chunking-embeddings.openapi.yaml`

**Checkpoint**: После T007-T015 можно независимо реализовывать user stories

---

## Phase 3: User Story 1 - Управляемый чанкинг документов (Priority: P1) MVP

**Goal**: Пользователь получает стабильный детерминированный chunking файлов по
настраиваемым параметрам размера и overlap

**Independent Test**: На фиксированном наборе файлов система создает
последовательные чанки, соблюдая chunk_size и overlap

### Tests for User Story 1

- [X] T016 [P] [US1] Описать интеграционный сценарий детерминированного chunking в `tests/integration/us1_chunking_deterministic.md`
- [X] T017 [US1] Реализовать integration-скрипт проверки chunking параметров в `scripts/tests/us1_chunking_deterministic.ps1`
- [X] T018 [P] [US1] Добавить unit-тесты chunker логики в `tests/unit/file_indexer/test_chunker.py`

### Implementation for User Story 1

- [X] T019 [P] [US1] Реализовать chunker с поддержкой chunk_size/overlap в `services/file-indexer/src/ingestion_pipeline/chunker.py`
- [X] T020 [US1] Реализовать валидацию overlap границ в `services/file-indexer/src/ingestion_pipeline/chunking_validation.py`
- [X] T021 [US1] Реализовать сбор `ChunkRecord` с порядком чанков в `services/file-indexer/src/ingestion_pipeline/chunk_record_builder.py`
- [X] T022 [US1] Реализовать endpoint запуска ingestion run `POST /v1/indexing/ingestion/jobs` в `services/mcp-server/src/system_status_handler.py`
- [X] T023 [US1] Реализовать endpoint прогресса ingestion run `GET /v1/indexing/ingestion/jobs/{runId}` в `services/mcp-server/src/system_status_handler.py`
- [X] T024 [US1] Подключить вызов chunking pipeline в рантайм индексатора в `services/file-indexer/scripts/entrypoint.sh`

**Checkpoint**: US1 дает MVP-ценность и проверяется независимо

---

## Phase 4: User Story 2 - Надежная генерация эмбеддингов и upsert (Priority: P2)

**Goal**: Для каждого чанка генерируется эмбеддинг с retry при транзиентных
ошибках и выполняется upsert в векторное хранилище

**Independent Test**: При искусственных транзиентных ошибках эмбеддингов
повторные попытки отрабатывают до лимита, а успешные чанки попадают в upsert

### Tests for User Story 2

- [X] T025 [P] [US2] Описать интеграционный сценарий retry эмбеддингов в `tests/integration/us2_embedding_retry.md`
- [X] T026 [US2] Реализовать integration-скрипт retry + upsert проверки в `scripts/tests/us2_embedding_retry_upsert.ps1`
- [X] T027 [P] [US2] Добавить unit-тесты retry-политики эмбеддингов в `tests/unit/file_indexer/test_embedding_retry.py`

### Implementation for User Story 2

- [X] T028 [US2] Реализовать adapter генерации эмбеддингов в `services/file-indexer/src/ingestion_pipeline/embedding_provider.py`
- [X] T029 [US2] Реализовать retry-оркестратор эмбеддингов в `services/file-indexer/src/ingestion_pipeline/embedding_retry.py`
- [X] T030 [US2] Реализовать upsert-репозиторий в Qdrant в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T031 [US2] Интегрировать chunk->embedding->upsert пайплайн в `services/file-indexer/src/ingestion_pipeline/ingestion_service.py`
- [X] T032 [US2] Отразить счетчики retry и ошибок в ingestion status API в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: US2 проверяема отдельно после US1 и не блокирует метаданные US3

---

## Phase 5: User Story 3 - Трассируемые метаданные чанков (Priority: P3)

**Goal**: Каждая векторная запись содержит обязательные метаданные источника и
pipeline формирует итоговую сводку run с покрытием метаданных

**Independent Test**: После run summary и выборка записей показывают полный набор
метаданных (`path`, `fileName`, `fileType`, `contentHash`, `timestamp`)

### Tests for User Story 3

- [X] T033 [P] [US3] Описать интеграционный сценарий валидации метаданных в `tests/integration/us3_metadata_traceability.md`
- [X] T034 [US3] Реализовать integration-скрипт проверки metadata coverage в `scripts/tests/us3_metadata_traceability.ps1`
- [X] T035 [P] [US3] Добавить контрактные тесты summary endpoint в `tests/contract/us3_ingestion_summary_contract.md`

### Implementation for User Story 3

- [X] T036 [US3] Реализовать маппер обязательных метаданных в `services/file-indexer/src/ingestion_pipeline/metadata_mapper.py`
- [X] T037 [US3] Реализовать content hash builder для источников чанков в `services/file-indexer/src/ingestion_pipeline/content_hash.py`
- [X] T038 [US3] Реализовать сбор `IngestionRunSummary` и metadataCoverage в `services/file-indexer/src/ingestion_pipeline/run_summary.py`
- [X] T039 [US3] Реализовать endpoint итоговой сводки `GET /v1/indexing/ingestion/jobs/{runId}/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T040 [US3] Синхронизировать quickstart по метаданным и summary в `specs/003-chunking-embeddings-pipeline/quickstart.md`
- [X] T041 [US3] Добавить troubleshooting раздел по метаданным и retry в `README.md`

**Checkpoint**: US3 завершает требования трассируемости и наблюдаемости пайплайна

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная проверка регрессий, контрактов и документации

- [X] T042 [P] Валидировать соответствие контрактов ingestion API в `specs/003-chunking-embeddings-pipeline/contracts/chunking-embeddings.openapi.yaml`
- [X] T043 Проверить регрессию `full-scan` после внедрения ingestion pipeline в `tests/integration/regression_full_scan_after_ingestion.md`
- [X] T044 [P] Проверить регрессию `delta-after-commit` после внедрения ingestion pipeline в `tests/integration/regression_delta_after_commit_after_ingestion.md`
- [X] T045 [P] Добавить сценарий идемпотентного повторного ingestion run в `tests/integration/ingestion_idempotency_cycle.md`
- [X] T046 Реализовать compose regression-скрипт chunking/embedding pipeline в `scripts/tests/ingestion_compose_regression.ps1`
- [X] T047 [P] Обновить roadmap-статусы по section 4 в `README.md`
- [X] T048 Обновить release-checklist фичи в `specs/003-chunking-embeddings-pipeline/release-checklist.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): старт сразу
- Foundational (Phase 2): зависит от Setup, блокирует все user stories
- User Stories (Phase 3-5): стартуют после Foundational
- Polish (Phase 6): после завершения целевых user stories

### User Story Dependencies

- US1 (P1): зависит только от Foundational, формирует MVP chunking
- US2 (P2): зависит от US1 (требует готовые chunk records)
- US3 (P3): зависит от US2 (метаданные и summary по результатам upsert/embedding)

### Dependency Graph

- `US1 -> MVP`
- `US2 -> US1`
- `US3 -> US2`
- Рекомендуемый порядок поставки: `P1 -> P2 -> P3`

---

## Parallel Execution Examples

### US1

```text
- [ ] T016 [P] [US1] Описать интеграционный сценарий детерминированного chunking в `tests/integration/us1_chunking_deterministic.md`
- [ ] T018 [P] [US1] Добавить unit-тесты chunker логики в `tests/unit/file_indexer/test_chunker.py`
- [ ] T019 [P] [US1] Реализовать chunker с поддержкой chunk_size/overlap в `services/file-indexer/src/ingestion_pipeline/chunker.py`
```

### US2

```text
- [ ] T025 [P] [US2] Описать интеграционный сценарий retry эмбеддингов в `tests/integration/us2_embedding_retry.md`
- [ ] T027 [P] [US2] Добавить unit-тесты retry-политики эмбеддингов в `tests/unit/file_indexer/test_embedding_retry.py`
- [ ] T030 [US2] Реализовать upsert-репозиторий в Qdrant в `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
```

### US3

```text
- [ ] T033 [P] [US3] Описать интеграционный сценарий валидации метаданных в `tests/integration/us3_metadata_traceability.md`
- [ ] T035 [P] [US3] Добавить контрактные тесты summary endpoint в `tests/contract/us3_ingestion_summary_contract.md`
- [ ] T038 [US3] Реализовать сбор `IngestionRunSummary` и metadataCoverage в `services/file-indexer/src/ingestion_pipeline/run_summary.py`
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать US1 (T016-T024)
3. Проверить независимый acceptance тест US1
4. Зафиксировать MVP baseline

### Incremental Delivery

1. MVP chunking (US1)
2. Добавить надежный embedding+upsert (US2)
3. Добавить трассируемые метаданные и summary (US3)
4. Выполнить Phase 6 и финальную приемку

### Format Validation

- Все задачи соответствуют формату: `- [ ] T### [P?] [US?] Описание с путем`
- Для задач user story всегда указан story label (`[US1]`, `[US2]`, `[US3]`)
- Для Setup/Foundational/Polish story label не используется
- Каждая задача содержит явный путь к файлу

