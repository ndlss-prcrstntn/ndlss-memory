# Tasks: MCP Transport Compatibility

**Input**: Документы из `Z:/WORK/ndlss-memory/specs/009-mcp-transport/`
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`

**Tests**: Тесты обязательны, так как спецификация требует MCP-контракты, transport smoke и регрессионные проверки.

**Organization**: Задачи сгруппированы по user story для независимой реализации и проверки.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить структуру MCP transport реализации и базовые артефакты.

- [X] T001 Create MCP transport OpenAPI skeleton in `services/mcp-server/openapi/mcp-transport.openapi.yaml`
- [X] T002 Create MCP transport package scaffold in `services/mcp-server/src/mcp_transport/__init__.py`
- [X] T003 [P] Create MCP transport protocol model scaffold in `services/mcp-server/src/mcp_transport/protocol_models.py`
- [X] T004 [P] Create MCP transport session state scaffold in `services/mcp-server/src/mcp_transport/session_state.py`
- [X] T005 [P] Create MCP tool registry scaffold in `services/mcp-server/src/mcp_transport/tool_registry.py`
- [X] T006 Create MCP transport test scaffold in `tests/unit/mcp_server/test_mcp_transport_handshake.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать общие компоненты transport-слоя, обязательные для всех user stories.

- [X] T007 Implement JSON-RPC request/response validation models in `services/mcp-server/src/mcp_transport/protocol_models.py`
- [X] T008 [P] Implement MCP session lifecycle store in `services/mcp-server/src/mcp_transport/session_state.py`
- [X] T009 [P] Implement MCP error mapping (`internal -> JSON-RPC`) in `services/mcp-server/src/mcp_transport/error_mapper.py`
- [X] T010 Implement MCP request dispatcher core in `services/mcp-server/src/mcp_transport/dispatcher.py`
- [X] T011 [P] Implement shared MCP handler context adapter to existing services in `services/mcp-server/src/mcp_transport/service_adapter.py`
- [X] T012 Integrate MCP transport routes bootstrap in `services/mcp-server/src/system_status_handler.py`
- [X] T013 [P] Add unit tests for protocol model validation in `tests/unit/mcp_server/test_mcp_transport_protocol_models.py`
- [X] T014 [P] Add unit tests for session state transitions in `tests/unit/mcp_server/test_mcp_transport_session_state.py`
- [X] T015 [P] Add unit tests for JSON-RPC error mapping in `tests/unit/mcp_server/test_mcp_transport_error_mapper.py`

**Checkpoint**: Базовый transport foundation готов, можно реализовывать пользовательские истории.

---

## Phase 3: User Story 1 - MCP Handshake & Transport Endpoints (Priority: P1) MVP

**Goal**: MCP-клиент может подключиться к серверу и пройти `initialize`/`notifications/initialized`/`ping` через transport endpoint-ы.

**Independent Test**: Клиент выполняет handshake через `POST /mcp`; discovery и SSE endpoint-ы доступны; протокольные ошибки возвращаются в JSON-RPC формате.

### Tests for User Story 1

- [X] T016 [P] [US1] Add contract test for MCP transport handshake in `tests/contract/mcp_transport_handshake_contract.md`
- [X] T017 [P] [US1] Add integration smoke scenario for `/mcp` and `/sse` availability in `tests/integration/mcp_transport_handshake_smoke.md`
- [X] T018 [P] [US1] Add unit tests for initialize/initialized/ping handlers in `tests/unit/mcp_server/test_mcp_transport_handshake.py`

### Implementation for User Story 1

- [X] T019 [US1] Implement streamable HTTP MCP endpoint handler (`POST /mcp`) in `services/mcp-server/src/mcp_transport/http_transport.py`
- [X] T020 [US1] Implement SSE connect endpoint handler (`GET /sse`) in `services/mcp-server/src/mcp_transport/sse_transport.py`
- [X] T021 [US1] Implement SSE message endpoint handler (`POST /messages`) in `services/mcp-server/src/mcp_transport/sse_transport.py`
- [X] T022 [US1] Implement MCP discovery endpoint (`GET /.well-known/mcp`) in `services/mcp-server/src/mcp_transport/discovery.py`
- [X] T023 [US1] Register MCP transport routes in Flask app wiring in `services/mcp-server/src/system_status_handler.py`
- [X] T024 [US1] Sync transport handshake contract to runtime OpenAPI in `services/mcp-server/openapi/mcp-transport.openapi.yaml`

**Checkpoint**: User Story 1 работает независимо и покрывает подключение MCP клиентов.

---

## Phase 4: User Story 2 - MCP Tools List/Call Integration (Priority: P2)

**Goal**: Клиент получает список инструментов через `tools/list` и вызывает ключевые операции через `tools/call`.

**Independent Test**: После handshake `tools/list` возвращает каталог, а `tools/call` для search/source/metadata/ingestion start/status возвращает структурированные ответы и валидные JSON-RPC ошибки.

### Tests for User Story 2

- [X] T025 [P] [US2] Add contract test for `tools/list` and `tools/call` envelopes in `tests/contract/mcp_transport_tools_contract.md`
- [X] T026 [P] [US2] Add integration scenario for MCP tools flow in `tests/integration/mcp_transport_tools_flow.md`
- [X] T027 [P] [US2] Add unit tests for MCP tool registry and dispatch in `tests/unit/mcp_server/test_mcp_tool_registry.py`
- [X] T028 [P] [US2] Add unit tests for MCP search tool adapters in `tests/unit/mcp_server/test_mcp_tool_adapters_search.py`

### Implementation for User Story 2

- [X] T029 [US2] Implement MCP tool catalog schemas in `services/mcp-server/src/mcp_transport/tool_registry.py`
- [X] T030 [US2] Implement `tools/list` method handler in `services/mcp-server/src/mcp_transport/method_handlers.py`
- [X] T031 [US2] Implement `tools/call` method handler in `services/mcp-server/src/mcp_transport/method_handlers.py`
- [X] T032 [P] [US2] Implement semantic search/source/metadata MCP adapters in `services/mcp-server/src/mcp_transport/tools_search.py`
- [X] T033 [P] [US2] Implement ingestion start/status MCP adapters in `services/mcp-server/src/mcp_transport/tools_indexing.py`
- [X] T034 [US2] Implement JSON-RPC error payload enrichment (`errorCode`, `details`, `retryable`) in `services/mcp-server/src/mcp_transport/error_mapper.py`
- [X] T035 [US2] Handle "collection missing => empty result" path in MCP search adapter in `services/mcp-server/src/mcp_transport/tools_search.py`
- [X] T036 [US2] Sync MCP tools contract to runtime OpenAPI in `services/mcp-server/openapi/mcp-transport.openapi.yaml`

**Checkpoint**: User Story 2 завершена и пригодна для самостоятельной демонстрации клиенту.

---

## Phase 5: User Story 3 - Client Onboarding & Compatibility Gates (Priority: P3)

**Goal**: Пользователь подключает VS Code/Claude/Cline по готовой конфигурации, а совместимость transport подтверждается smoke/contract проверками.

**Independent Test**: Новый пользователь по документации подключает MCP-клиент без ручного подбора endpoint, а CI smoke/contract для transport проходит.

### Tests for User Story 3

- [X] T037 [P] [US3] Add contract test for discovery and client config expectations in `tests/contract/mcp_transport_discovery_contract.md`
- [X] T038 [P] [US3] Add MCP compatibility smoke script for compose stack in `scripts/tests/mcp_transport_compatibility_smoke.ps1`
- [X] T039 [P] [US3] Add integration troubleshooting scenario for 404/405 transport misconfiguration in `tests/integration/mcp_transport_troubleshooting.md`

### Implementation for User Story 3

- [X] T040 [US3] Add VS Code/Claude/Cline MCP config examples in `docs/mcp-client-config.example.json`
- [X] T041 [US3] Update public onboarding for MCP transport in `docs/quickstart.md`
- [X] T042 [US3] Update multi-project preset guidance for MCP transport endpoints in `docs/compose-presets.md`
- [X] T043 [US3] Update primary project documentation for MCP transport usage in `README.md`
- [X] T044 [US3] Add dedicated MCP transport troubleshooting guide in `docs/configuration.md`

**Checkpoint**: User Story 3 дает готовый production-like onboarding для внешних пользователей.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальные проверки, регрессии и release-readiness.

- [X] T045 [P] Add concurrency regression tests for multi-session MCP transport in `tests/unit/mcp_server/test_mcp_transport_concurrency.py`
- [X] T046 [P] Add invalid-method and malformed-envelope regression tests in `tests/unit/mcp_server/test_mcp_transport_negative_cases.py`
- [X] T047 Integrate MCP transport checks into quality suite pipeline in `scripts/tests/run_quality_stability_suite.ps1`
- [X] T048 Validate spec/runtime OpenAPI parity for MCP transport in `services/mcp-server/openapi/mcp-transport.openapi.yaml`
- [X] T049 [P] Update release notes for MCP transport feature completion in `CHANGELOG.md`
- [X] T050 Validate UTF-8 Markdown compliance after docs updates in `scripts/tests/validate_markdown_encoding.ps1`

---

## Dependencies & Execution Order

- Phase order: Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6.
- User story dependency graph: US1 -> US2 -> US3.
- US2 depends on US1 because tool calls require initialized MCP transport handshake.
- US3 depends on US1 and US2 because client configs and smoke tests require final transport + tools behavior.
- Within each user story: tests first, then implementation, then contract/runtime synchronization.

## Parallel Execution Examples

- US1 parallel set: `T016`, `T017`, `T018` can run together; `T019` and `T020` can run in parallel after `T015`.
- US2 parallel set: `T025`, `T026`, `T027`, `T028` can run together; `T032` and `T033` can run together after `T031`.
- US3 parallel set: `T037`, `T038`, `T039` can run together; `T041`, `T042`, `T044` can run together after `T040`.
- Polish parallel set: `T045`, `T046`, `T049`, `T050` can run together after story phases are complete.

## Implementation Strategy

- MVP first: deliver only Phase 3 (US1) to unblock MCP client connectivity.
- Increment 2: deliver Phase 4 (US2) to provide practical MCP tool value.
- Increment 3: deliver Phase 5 (US3) for production-grade onboarding and compatibility confidence.
- Final hardening: run Phase 6 to lock regression coverage and release readiness.
