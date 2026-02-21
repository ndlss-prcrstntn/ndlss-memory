# Tasks: Режим Full Scan

**Input**: Документы из `/specs/002-full-scan/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты включены, так как конституция требует проверки compose-запуска,
MCP-контрактов, идемпотентности и регрессии режимов индексатора.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: можно выполнять параллельно (разные файлы, нет блокирующих зависимостей)
- **[Story]**: метка user story (`[US1]`, `[US2]`, `[US3]`)
- В каждой задаче указан точный путь к файлу

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить каркас реализации Full Scan и тестового окружения

- [X] T001 Создать каркас модулей индексатора в `services/file-indexer/src/__init__.py`
- [X] T002 [P] Подготовить манифест тестовых фикстур Full Scan в `tests/fixtures/full-scan/fixture-manifest.md`
- [X] T003 [P] Добавить общий скрипт подготовки full-scan тестового окружения в `scripts/tests/full_scan_test_env.ps1`
- [X] T004 [P] Добавить переменные `INDEX_MAX_FILE_SIZE_BYTES` и `INDEX_PROGRESS_INTERVAL_SECONDS` в `.env.example`
- [X] T005 [P] Обновить описание новых env-параметров в `docs/configuration.md`
- [X] T006 [P] Создать базовый контрактный сценарий задач Full Scan в `tests/contract/full_scan_jobs_contract.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать базовые компоненты, блокирующие все user stories

- [X] T007 Расширить схему runtime-конфигурации Full Scan в `services/file-indexer/config/runtime-config.schema.json`
- [X] T008 Реализовать валидацию лимита размера и интервала прогресса в `services/file-indexer/scripts/validate-config.sh`
- [X] T009 [P] Подключить новые env-переменные в `infra/docker/docker-compose.yml`
- [X] T010 Реализовать модели `ScanJob`, `ScanProgress`, `ScanSummary` в `services/file-indexer/src/scan_models.py`
- [X] T011 [P] Реализовать классификатор причин пропуска в `services/file-indexer/src/skip_reasons.py`
- [X] T012 Реализовать хранилище состояния задач Full Scan в `services/mcp-server/src/full_scan_state.py`
- [X] T013 [P] Реализовать модель машиночитаемых ошибок Full Scan в `services/mcp-server/src/full_scan_errors.py`
- [X] T014 Добавить каркас маршрутов Full Scan в `services/mcp-server/src/system_status_handler.py`
- [X] T015 Синхронизировать runtime OpenAPI-контракт в `services/mcp-server/openapi/full-scan-indexing.openapi.yaml`

**Checkpoint**: После T007-T015 можно независимо реализовывать пользовательские истории

---

## Phase 3: User Story 1 - Полная индексация директории (Priority: P1) MVP

**Goal**: Пользователь запускает Full Scan и получает обработку всех поддерживаемых
файлов из директории и вложенных папок

**Independent Test**: Запуск Full Scan на тестовом дереве возвращает обработку
всех поддерживаемых файлов и рабочий API прогресса задачи

### Tests for User Story 1

- [X] T016 [P] [US1] Описать интеграционный сценарий рекурсивного обхода в `tests/integration/us1_full_scan_recursive_indexing.md`
- [X] T017 [US1] Реализовать интеграционный smoke-скрипт запуска и завершения задачи в `scripts/tests/us1_full_scan_recursive_indexing.ps1`
- [X] T018 [P] [US1] Добавить контрактные проверки `POST/GET` задач Full Scan в `tests/contract/us1_full_scan_jobs_contract.md`

### Implementation for User Story 1

- [X] T019 [P] [US1] Реализовать рекурсивный обход директории в `services/file-indexer/src/full_scan_walker.py`
- [X] T020 [US1] Реализовать фильтр поддерживаемых расширений без учета регистра в `services/file-indexer/src/file_type_filter.py`
- [X] T021 [US1] Реализовать исполнение Full Scan с подсчетом обработанных/проиндексированных файлов в `services/file-indexer/src/full_scan_service.py`
- [X] T022 [US1] Реализовать endpoint запуска задачи `POST /v1/indexing/full-scan/jobs` в `services/mcp-server/src/system_status_handler.py`
- [X] T023 [US1] Реализовать endpoint прогресса `GET /v1/indexing/full-scan/jobs/{jobId}` в `services/mcp-server/src/system_status_handler.py`
- [X] T024 [US1] Подключить запуск worker Full Scan в `services/file-indexer/scripts/entrypoint.sh`

**Checkpoint**: US1 дает MVP-ценность и готова к демонстрации отдельно

---

## Phase 4: User Story 2 - Управляемая фильтрация файлов (Priority: P2)

**Goal**: Пользователь управляет составом индексируемых файлов через include/exclude правила

**Independent Test**: Изменение `INDEX_FILE_TYPES` и `INDEX_EXCLUDE_PATTERNS`
приводит к ожидаемому составу включенных/пропущенных файлов

### Tests for User Story 2

- [X] T025 [P] [US2] Описать интеграционный сценарий фильтрации типов и паттернов в `tests/integration/us2_full_scan_filtering.md`
- [X] T026 [US2] Реализовать интеграционный скрипт проверки include/exclude правил в `scripts/tests/us2_full_scan_filtering.ps1`
- [X] T027 [P] [US2] Добавить unit-тесты фильтрации файлов в `tests/unit/file_indexer/test_file_filters.py`

### Implementation for User Story 2

- [X] T028 [US2] Реализовать pre-read фильтр исключающих паттернов в `services/file-indexer/src/path_exclude_filter.py`
- [X] T029 [US2] Интегрировать цепочку фильтрации типов и паттернов в `services/file-indexer/src/full_scan_service.py`
- [X] T030 [US2] Добавить причины пропуска `UNSUPPORTED_TYPE` и `EXCLUDED_BY_PATTERN` в `services/file-indexer/src/skip_reasons.py`
- [X] T031 [US2] Отразить активные фильтры в runtime-конфиге API в `services/mcp-server/src/system_status_handler.py`
- [X] T032 [US2] Обновить quickstart по правилам фильтрации в `specs/002-full-scan/quickstart.md`

**Checkpoint**: US2 полностью проверяема отдельно от US3 при наличии базового US1

---

## Phase 5: User Story 3 - Прозрачный прогресс и устойчивость (Priority: P3)

**Goal**: Пользователь получает стабильный Full Scan с продолжением при ошибках,
лимитом размера и итоговым отчетом причин пропуска

**Independent Test**: При наличии поврежденных и слишком больших файлов Full Scan
завершается, а итоговый отчет содержит корректные причины пропуска

### Tests for User Story 3

- [X] T033 [P] [US3] Описать интеграционный troubleshooting-сценарий устойчивости в `tests/integration/us3_full_scan_resilience.md`
- [X] T034 [US3] Реализовать интеграционный скрипт проверки continue-on-error и summary в `scripts/tests/us3_full_scan_resilience.ps1`
- [X] T035 [P] [US3] Добавить контрактные проверки summary endpoint в `tests/contract/us3_full_scan_summary_contract.md`

### Implementation for User Story 3

- [X] T036 [US3] Реализовать проверку лимита размера файла в `services/file-indexer/src/file_size_guard.py`
- [X] T037 [US3] Реализовать обработку ошибок чтения с продолжением сканирования в `services/file-indexer/src/full_scan_service.py`
- [X] T038 [US3] Реализовать периодический emitter прогресса в `services/file-indexer/src/progress_reporter.py`
- [X] T039 [US3] Реализовать endpoint отчета `GET /v1/indexing/full-scan/jobs/{jobId}/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T040 [US3] Добавить структурированные логи прогресса Full Scan в `services/file-indexer/src/progress_reporter.py`
- [X] T041 [US3] Добавить troubleshooting раздел по ошибкам Full Scan в `README.md`

**Checkpoint**: US3 завершает эксплуатационную прозрачность и recovery-поток

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финализация качества, контрактов, регрессий и документации

- [X] T042 [P] Валидировать соответствие контрактов в `specs/002-full-scan/contracts/full-scan-indexing.openapi.yaml`
- [X] T043 Проверить регрессию режима `delta-after-commit` после изменений Full Scan в `tests/integration/regression_delta_after_commit.md`
- [X] T044 [P] Добавить сценарий идемпотентного повторного Full Scan без дубликатов в `tests/integration/full_scan_idempotency_cycle.md`
- [X] T045 [P] Реализовать compose regression-скрипт для full-scan и переключения режимов в `scripts/tests/full_scan_compose_regression.ps1`
- [X] T046 Обновить release-checklist фичи в `specs/002-full-scan/release-checklist.md`
- [X] T047 [P] Обновить roadmap-статусы после implementation в `README.md`
- [X] T048 Синхронизировать итоговый quickstart с реализованным поведением в `specs/002-full-scan/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): можно начинать сразу
- Foundational (Phase 2): зависит от Setup, блокирует все user stories
- User Stories (Phase 3-5): стартуют после Foundational
- Polish (Phase 6): после завершения целевых user stories

### User Story Dependencies

- US1 (P1): зависит только от Foundational, формирует MVP
- US2 (P2): зависит от базового потока US1, добавляет управляемую фильтрацию
- US3 (P3): зависит от базового потока US1, расширяет устойчивость и наблюдаемость

### Dependency Graph

- `US1 -> MVP`
- `US2 -> US1` (расширение фильтрации поверх базового Full Scan)
- `US3 -> US1` (расширение прогресса/ошибок поверх базового Full Scan)
- Рекомендуемый порядок поставки: `P1 -> P2 -> P3`

---

## Parallel Execution Examples

### US1

```text
- [ ] T016 [P] [US1] Описать интеграционный сценарий рекурсивного обхода в `tests/integration/us1_full_scan_recursive_indexing.md`
- [ ] T018 [P] [US1] Добавить контрактные проверки `POST/GET` задач Full Scan в `tests/contract/us1_full_scan_jobs_contract.md`
- [ ] T019 [P] [US1] Реализовать рекурсивный обход директории в `services/file-indexer/src/full_scan_walker.py`
```

### US2

```text
- [ ] T025 [P] [US2] Описать интеграционный сценарий фильтрации типов и паттернов в `tests/integration/us2_full_scan_filtering.md`
- [ ] T027 [P] [US2] Добавить unit-тесты фильтрации файлов в `tests/unit/file_indexer/test_file_filters.py`
- [ ] T032 [US2] Обновить quickstart по правилам фильтрации в `specs/002-full-scan/quickstart.md`
```

### US3

```text
- [ ] T033 [P] [US3] Описать интеграционный troubleshooting-сценарий устойчивости в `tests/integration/us3_full_scan_resilience.md`
- [ ] T035 [P] [US3] Добавить контрактные проверки summary endpoint в `tests/contract/us3_full_scan_summary_contract.md`
- [ ] T038 [US3] Реализовать периодический emitter прогресса в `services/file-indexer/src/progress_reporter.py`
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать US1 (T016-T024)
3. Проверить независимый acceptance тест US1
4. Зафиксировать MVP baseline

### Incremental Delivery

1. MVP (US1)
2. Добавить управляемую фильтрацию (US2)
3. Добавить устойчивость и прозрачный прогресс (US3)
4. Выполнить Phase 6 и финальную приемку

### Format Validation

- Все задачи соответствуют формату: `- [ ] T### [P?] [US?] Описание с путем`
- Для задач user story всегда указан story label (`[US1]`, `[US2]`, `[US3]`)
- Для Setup/Foundational/Polish story label не используется
- Каждая задача содержит явный путь к файлу

