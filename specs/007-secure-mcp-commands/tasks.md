# Tasks: Безопасный запуск команд через MCP

**Input**: Документы из `/specs/007-secure-mcp-commands/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/mcp-command-security.openapi.yaml`

**Tests**: Тестовые задачи включены (unit + contract + integration), так как требования спецификации и конституции требуют формализованных MCP-контрактов, проверки compose и регрессий.

**Organization**: Задачи сгруппированы по user stories для независимой реализации и проверки.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить каркас артефактов и точки интеграции для secure command runtime.

- [X] T001 Синхронизировать контракт MCP command security в `services/mcp-server/openapi/mcp-command-security.openapi.yaml`
- [X] T002 Подготовить базовый конфиг политики команд и таймаутов в `.env.example`
- [X] T003 [P] Создать contract checklist для secure command runtime в `tests/contract/mcp_command_security_contract.md`
- [X] T004 [P] Создать integration smoke сценарий secure command runtime в `tests/integration/mcp_command_security_smoke.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты, которые блокируют все user stories.

- [X] T005 Реализовать загрузку и валидацию command policy в `services/mcp-server/src/command_security_policy.py`
- [X] T006 Реализовать state-хранилище execution-запросов в `services/mcp-server/src/command_execution_state.py`
- [X] T007 [P] Реализовать append-only аудит и базовый retention механизм в `services/mcp-server/src/command_audit_store.py`
- [X] T008 [P] Реализовать машиночитаемую модель ошибок command runtime в `services/mcp-server/src/command_execution_errors.py`
- [X] T009 Реализовать DTO/валидацию для execution request/result/audit в `services/mcp-server/src/command_execution_models.py`
- [X] T010 Реализовать process runner с поддержкой timeout/termination hooks в `services/mcp-server/src/command_process_runner.py`
- [X] T011 Подключить bootstrap secure command runtime в `services/mcp-server/src/system_status_handler.py`

**Checkpoint**: После Phase 2 можно независимо реализовывать user stories.

---

## Phase 3: User Story 1 - Безопасный запуск разрешенных команд (Priority: P1) MVP

**Goal**: Пользователь запускает только allowlist-команды с контролем времени и получает структурированный результат.

**Independent Test**: Выполнить 3 запроса (`allowed`, `denied`, `timeout`) и проверить, что разрешенный запрос выполняется, неразрешенный блокируется до запуска, а timeout завершается предсказуемым статусом.

### Tests for User Story 1

- [X] T012 [P] [US1] Добавить contract-кейсы allowlist/timeout для `POST /v1/commands/execute` в `tests/contract/mcp_command_security_contract.md`
- [X] T013 [P] [US1] Добавить unit-тесты policy-check и timeout-веток в `tests/unit/mcp_server/test_command_execution_policy.py`
- [X] T014 [P] [US1] Добавить integration-сценарий allow/deny/timeout в `tests/integration/mcp_command_execution_flow.md`

### Implementation for User Story 1

- [X] T015 [US1] Реализовать сервис выполнения команд с allowlist и timeout enforcement в `services/mcp-server/src/command_execution_service.py`
- [X] T016 [US1] Добавить endpoint `POST /v1/commands/execute` и `GET /v1/commands/executions/{requestId}` в `services/mcp-server/src/system_status_handler.py`
- [X] T017 [US1] Интегрировать structured success/error response mapping в `services/mcp-server/src/command_execution_models.py`

**Checkpoint**: US1 завершена и демонстрирует MVP безопасного запуска команд.

---

## Phase 4: User Story 2 - Изоляция и ограничение ресурсов (Priority: P2)

**Goal**: Команды выполняются в изолированной рабочей директории, без повышенных прав и с лимитами ресурсов.

**Independent Test**: Проверить запуск внутри workspace, блокировку выхода за границы директории, и применение CPU/Memory/non-root ограничений.

### Tests for User Story 2

- [X] T018 [P] [US2] Добавить contract-кейсы для workspace isolation и resource violation в `tests/contract/mcp_command_security_contract.md`
- [X] T019 [P] [US2] Добавить unit-тесты canonical-path изоляции в `tests/unit/mcp_server/test_command_workspace_isolation.py`
- [X] T020 [P] [US2] Добавить integration-сценарий non-root и resource limits в `tests/integration/mcp_command_resource_isolation.md`

### Implementation for User Story 2

- [X] T021 [US2] Реализовать guard изоляции рабочей директории в `services/mcp-server/src/command_workspace_guard.py`
- [X] T022 [US2] Реализовать применение CPU/Memory лимитов при запуске процесса в `services/mcp-server/src/command_process_runner.py`
- [X] T023 [US2] Настроить non-root runtime для mcp-server контейнера в `services/mcp-server/Dockerfile`
- [X] T024 [US2] Зафиксировать runtime лимиты и security-параметры сервиса в `infra/docker/docker-compose.yml`

**Checkpoint**: US2 завершена и не нарушает сценарии US1.

---

## Phase 5: User Story 3 - Наблюдаемость и аудит вызовов (Priority: P3)

**Goal**: Оператор получает единые машиночитаемые ошибки и аудит всех вызовов команд.

**Independent Test**: Выполнить успешный и ошибочный вызовы, затем получить список аудита и убедиться, что записи и error-коды консистентны.

### Tests for User Story 3

- [X] T025 [P] [US3] Добавить contract-кейсы structured errors и `GET /v1/commands/audit` в `tests/contract/mcp_command_security_contract.md`
- [X] T026 [P] [US3] Добавить unit-тесты lifecycle аудита и retention в `tests/unit/mcp_server/test_command_audit_store.py`
- [X] T027 [P] [US3] Добавить integration-сценарий аудита и диагностики ошибок в `tests/integration/mcp_command_audit_observability.md`

### Implementation for User Story 3

- [X] T028 [US3] Реализовать итоговую модель audit record и фильтрацию выдачи в `services/mcp-server/src/command_audit_store.py`
- [X] T029 [US3] Добавить endpoint `GET /v1/commands/audit` и статус-фильтры в `services/mcp-server/src/system_status_handler.py`
- [X] T030 [US3] Унифицировать error envelope и error-code mapping в `services/mcp-server/src/command_execution_errors.py`

**Checkpoint**: US3 завершена и обеспечивает операционную наблюдаемость.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная документация, контрактная синхронизация и проверка в compose-среде.

- [X] T031 [P] Обновить разделы по secure command runtime и API в `README.md`
- [X] T032 [P] Обновить параметры политики безопасности в `docs/configuration.md`
- [X] T033 [P] Актуализировать feature quickstart сценарии в `specs/007-secure-mcp-commands/quickstart.md`
- [X] T034 Синхронизировать финальный OpenAPI контракт в `services/mcp-server/openapi/mcp-command-security.openapi.yaml`
- [X] T035 Выполнить и зафиксировать compose smoke/regression прогон в `tests/integration/mcp_command_security_smoke.md`

---

## Dependencies & Execution Order

- Phase order: Setup -> Foundational -> US1 -> (US2 + US3) -> Polish.
- US1 (MVP) обязательна перед US2 и US3, так как дает базовый execution-path и requestId lifecycle.
- US2 и US3 могут выполняться параллельно после завершения Foundational и US1.
- Внутри каждой user story: тесты -> реализация -> интеграция.

## Dependency Graph (User Stories)

- US1 (P1) -> US2 (P2)
- US1 (P1) -> US3 (P3)

## Parallel Execution Examples

- US1: выполнять T012 + T013 + T014 параллельно, затем T015 -> T016 -> T017.
- US2: выполнять T018 + T019 + T020 параллельно, затем T021 -> T022 -> T023 -> T024.
- US3: выполнять T025 + T026 + T027 параллельно, затем T028 -> T029 -> T030.

## Implementation Strategy

- MVP first: завершить Phase 1-3 и получить рабочий безопасный `POST /v1/commands/execute`.
- Increment 2: добавить изоляцию и ресурсные ограничения (US2) без регрессии MVP.
- Increment 3: добавить полный аудит и наблюдаемость (US3), затем пройти polish и compose verification.

