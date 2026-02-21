# Tasks: Базовый Docker Compose стек

**Input**: Документы из `/specs/001-base-docker-compose/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Тесты включены, так как конституция требует проверки compose запуска,
контрактов и регрессионных сценариев.

**Organization**: Задачи сгруппированы по user story для независимой реализации.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: можно выполнять параллельно
- **[Story]**: метка user story (`[US1]`, `[US2]`, `[US3]`)
- В каждой задаче указан точный путь к файлу

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить каркас репозитория и базовые артефакты инфраструктуры

- [X] T001 Создать каркас Docker Compose файла в `infra/docker/docker-compose.yml`
- [X] T002 [P] Создать Dockerfile для индексатора в `services/file-indexer/Dockerfile`
- [X] T003 [P] Создать Dockerfile для MCP сервера в `services/mcp-server/Dockerfile`
- [X] T004 [P] Создать шаблон переменных окружения в `.env.example`
- [X] T005 [P] Создать каркас тестовых сценариев в `tests/integration/compose_startup_smoke_test.md`
- [X] T006 [P] Создать каркас контрактных проверок в `tests/contract/compose_observability_contract_test.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать обязательные общие компоненты до начала user stories

- [X] T007 Настроить три обязательных сервиса, сети и restart policy в `infra/docker/docker-compose.yml`
- [X] T008 Настроить healthcheck для `qdrant`, `file-indexer`, `mcp-server` в `infra/docker/docker-compose.yml`
- [X] T009 Настроить persistent volume для Qdrant в `infra/docker/docker-compose.yml`
- [X] T010 Настроить bind mount рабочей директории для индексатора в `infra/docker/docker-compose.yml`
- [X] T011 Реализовать схему runtime-конфигурации индексатора в `services/file-indexer/config/runtime-config.schema.json`
- [X] T012 Реализовать проверку `INDEX_MODE` и типов файлов в `services/file-indexer/scripts/validate-config.sh`
- [X] T013 Реализовать базовую политику `command_allowlist` и timeout в `services/mcp-server/config/security-policy.yaml`
- [X] T014 Реализовать endpoint `/health` и `/v1/system/status` в `services/mcp-server/src/system_status_handler.py`
- [X] T015 Синхронизировать runtime-контракт статуса в `services/mcp-server/openapi/compose-observability.openapi.yaml`

**Checkpoint**: После T007-T015 можно независимо выполнять user stories

---

## Phase 3: User Story 1 - Запуск стека одной командой (Priority: P1) MVP

**Goal**: Пользователь запускает полный стек одной командой и получает `healthy`
состояние всех обязательных сервисов

**Independent Test**: Запуск на чистой машине дает `Up (healthy)` для `qdrant`,
`file-indexer`, `mcp-server` без ручной правки compose-файла

### Tests for User Story 1

- [X] T016 [P] [US1] Описать acceptance smoke-сценарий запуска в `tests/integration/us1_compose_up_healthy.md`
- [X] T017 [US1] Реализовать автоматизированный smoke-скрипт в `scripts/tests/us1_compose_up_healthy.ps1`
- [X] T018 [US1] Зафиксировать проверку статуса API `/health` в `tests/contract/us1_health_endpoint_check.md`

### Implementation for User Story 1

- [X] T019 [US1] Добавить единый dev-запуск стека в `scripts/dev/up.ps1`
- [X] T020 [US1] Добавить единый dev-останов стека в `scripts/dev/down.ps1`
- [X] T021 [US1] Обновить сценарий быстрого запуска в `README.md`

**Checkpoint**: US1 демонстрирует MVP-ценность и готов к показу

---

## Phase 4: User Story 2 - Понятная первичная конфигурация (Priority: P2)

**Goal**: Пользователь меняет параметры в `.env` и запускает стек без изменений кода

**Independent Test**: Изменение порта/режима индексатора в `.env` применяется после
перезапуска и отражается в runtime-конфигурации

### Tests for User Story 2

- [X] T022 [P] [US2] Добавить сценарий проверки переопределения env-параметров в `tests/integration/us2_env_override.md`
- [X] T023 [US2] Реализовать скрипт проверки env-конфигурации в `scripts/tests/us2_env_override.ps1`

### Implementation for User Story 2

- [X] T024 [US2] Расширить и документировать обязательные переменные в `.env.example`
- [X] T025 [P] [US2] Добавить загрузку env-параметров индексатора в `services/file-indexer/scripts/entrypoint.sh`
- [X] T026 [P] [US2] Добавить загрузку env-параметров MCP сервера в `services/mcp-server/scripts/entrypoint.sh`
- [X] T027 [US2] Подключить env-переменные к сервисам в `infra/docker/docker-compose.yml`
- [X] T028 [US2] Добавить пользовательское описание параметров в `docs/configuration.md`

**Checkpoint**: US2 готова и проверяется отдельно от US1

---

## Phase 5: User Story 3 - Базовая эксплуатационная прозрачность (Priority: P3)

**Goal**: Пользователь может диагностировать проблемы запуска и восстановить стек
по документированному сценарию

**Independent Test**: При падении одного сервиса пользователь определяет причину и
выполняет восстановление по инструкции

### Tests for User Story 3

- [X] T029 [P] [US3] Добавить контрактный тест статуса сервисов в `tests/contract/us3_system_status_contract.md`
- [X] T030 [US3] Добавить интеграционный сценарий troubleshooting в `tests/integration/us3_troubleshooting.md`

### Implementation for User Story 3

- [X] T031 [US3] Реализовать CLI-утилиту диагностики стека в `scripts/ops/stack-status.ps1`
- [X] T032 [US3] Реализовать обработку ошибки `service not found` в `services/mcp-server/src/system_status_handler.py`
- [X] T033 [US3] Обновить руководство troubleshooting в `specs/001-base-docker-compose/quickstart.md`
- [X] T034 [US3] Добавить раздел диагностики и recovery в `README.md`

**Checkpoint**: US3 полностью независима и демонстрируема отдельно

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Довести качество, безопасность и документацию до release-ready состояния

- [X] T035 [P] Проверить соответствие OpenAPI контракту в `specs/001-base-docker-compose/contracts/compose-observability.openapi.yaml`
- [X] T036 Проверить сценарий перезапуска и сохранение данных Qdrant в `tests/integration/qdrant_persistence_cycle.md`
- [X] T037 [P] Финализировать quickstart после всех изменений в `specs/001-base-docker-compose/quickstart.md`
- [X] T038 [P] Синхронизировать архитектурное описание в `README.md`
- [X] T039 Провести финальную проверку compose-команд и задокументировать результат в `specs/001-base-docker-compose/release-checklist.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): старт сразу
- Foundational (Phase 2): зависит от Setup, блокирует все user stories
- User stories (Phase 3-5): стартуют после Foundational
- Polish (Phase 6): после завершения выбранных user stories

### User Story Dependencies

- US1 (P1): зависит только от Foundational
- US2 (P2): зависит от Foundational, не блокирует US1
- US3 (P3): зависит от Foundational, может идти после US1/US2 или параллельно

### Dependency Graph

- `US1 -> MVP`
- `US2 -> configurable runtime`
- `US3 -> operational diagnostics`
- `US1`, `US2`, `US3` не требуют последовательной функциональной зависимости,
  но рекомендуемый порядок поставки: P1 -> P2 -> P3

---

## Parallel Execution Examples

### US1

```text
- [X] T016 [P] [US1] ... tests/integration/us1_compose_up_healthy.md
- [X] T019 [US1] ... scripts/dev/up.ps1
- [X] T020 [US1] ... scripts/dev/down.ps1
```

### US2

```text
- [X] T025 [P] [US2] ... services/file-indexer/scripts/entrypoint.sh
- [X] T026 [P] [US2] ... services/mcp-server/scripts/entrypoint.sh
- [X] T022 [P] [US2] ... tests/integration/us2_env_override.md
```

### US3

```text
- [X] T029 [P] [US3] ... tests/contract/us3_system_status_contract.md
- [X] T031 [US3] ... scripts/ops/stack-status.ps1
- [X] T033 [US3] ... specs/001-base-docker-compose/quickstart.md
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Завершить Phase 1 и Phase 2
2. Реализовать US1 (T016-T021)
3. Проверить независимый acceptance тест US1
4. Зафиксировать MVP baseline

### Incremental Delivery

1. MVP (US1)
2. Добавить конфигурируемость (US2)
3. Добавить эксплуатационную диагностику (US3)
4. Выполнить Phase 6 и финальную приемку

### Format Validation

- Все задачи соответствуют формату: `- [ ] T### [P?] [US?] Описание с путем`
- Для задач user story всегда указан `[US1]/[US2]/[US3]`
- Для Setup/Foundational/Polish story label не используется

