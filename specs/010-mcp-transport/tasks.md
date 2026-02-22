# Tasks: MCP Ingestion Reliability

**Input**: Documents from `/specs/010-mcp-transport/`
**Prerequisites**: `plan.md` (required), `spec.md` (required), `research.md`, `data-model.md`, `contracts/`

**Tests**: Include regression/contract/integration tests required by the specification and constitution gates.

**Organization**: Tasks are grouped by user story so each story can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align baseline configuration and test scaffolding for this feature.

- [X] T001 Update environment baseline for Qdrant internal/external ports in `.env.example` and `.env.minimal.example`
- [X] T002 Align compose image presets defaults in `deploy/compose-images/generic.yml`, `deploy/compose-images/python.yml`, `deploy/compose-images/javascript.yml`, `deploy/compose-images/typescript.yml`, `deploy/compose-images/csharp.yml`, `deploy/compose-images/go.yml`, and `deploy/compose-images/java-kotlin.yml`
- [X] T003 Align compose source-build presets defaults in `deploy/compose/generic.yml`, `deploy/compose/python.yml`, `deploy/compose/javascript.yml`, `deploy/compose/typescript.yml`, `deploy/compose/csharp.yml`, `deploy/compose/go.yml`, and `deploy/compose/java-kotlin.yml`
- [X] T004 [P] Add feature-specific contract and integration placeholders in `tests/contract/qdrant_ingestion_reliability_contract.md` and `tests/integration/qdrant_ingestion_reliability.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Introduce shared runtime behavior required by all stories.

- [X] T005 Implement internal Qdrant port resolver for search repository in `services/mcp-server/src/search_repository.py`
- [X] T006 [P] Implement internal Qdrant port resolver in vector upsert repositories `services/mcp-server/src/ingestion_pipeline/vector_upsert_repository.py` and `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T007 Expose internal/external Qdrant runtime values in `services/mcp-server/src/system_status_handler.py`
- [X] T008 [P] Add unit tests for search repository port resolution in `tests/unit/mcp_server/test_search_repository_missing_collection.py`
- [X] T009 [P] Add unit tests for vector upsert repository env resolution in `tests/unit/mcp_server/test_vector_upsert_repository_config.py` and `tests/unit/file_indexer/test_vector_upsert_repository_config.py`
- [X] T010 Update shared regression helpers for `QDRANT_API_PORT` handling in `scripts/tests/quality_stage_helpers.ps1`

**Checkpoint**: Foundational networking and config behavior is ready for story work.

---

## Phase 3: User Story 1 - Guaranteed Persistent Ingestion (Priority: P1) MVP

**Goal**: MCP-started ingestion must create/update persistent Qdrant data and not report false success.

**Independent Test**: Start ingestion from MCP on a fresh stack and verify `workspace_chunks` exists with `points/count > 0`.

### Tests for User Story 1

- [X] T011 [P] [US1] Add MCP ingestion collection-creation regression script in `scripts/tests/us1_ingestion_collection_creation.ps1`
- [X] T012 [P] [US1] Add contract assertions for ingestion status and collection count in `tests/contract/qdrant_ingestion_reliability_contract.md`
- [X] T013 [P] [US1] Add integration walkthrough for ingestion persistence in `tests/integration/qdrant_ingestion_reliability.md`

### Implementation for User Story 1

- [X] T014 [US1] Enforce HTTP upsert defaults for MCP ingestion in `services/mcp-server/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T015 [US1] Propagate persistence failures as ingestion errors in `services/mcp-server/src/ingestion_pipeline/ingestion_service.py` and `services/mcp-server/src/ingestion_errors.py`
- [X] T016 [US1] Include persistence diagnostics in ingestion status responses in `services/mcp-server/src/system_status_handler.py`
- [X] T017 [US1] Register US1 regression stage in `scripts/tests/run_quality_stability_suite.ps1` and `scripts/tests/quality_gate_runner.ps1`

**Checkpoint**: US1 is done when MCP ingestion reliably produces persistent searchable data.

---

## Phase 4: User Story 2 - Qdrant Port Isolation (Priority: P2)

**Goal**: Custom external `QDRANT_PORT` must not break internal service-to-service connectivity.

**Independent Test**: Run stack with non-default external `QDRANT_PORT` and validate ingestion and semantic search complete without connection-refused errors.

### Tests for User Story 2

- [X] T018 [P] [US2] Add non-default external port regression script in `scripts/tests/us2_custom_qdrant_external_port.ps1`
- [X] T019 [P] [US2] Add integration scenario for parallel stacks with different host ports in `tests/integration/qdrant_external_port_isolation.md`

### Implementation for User Story 2

- [X] T020 [US2] Inject `QDRANT_API_PORT` into all image presets in `deploy/compose-images/generic.yml`, `deploy/compose-images/python.yml`, `deploy/compose-images/javascript.yml`, `deploy/compose-images/typescript.yml`, `deploy/compose-images/csharp.yml`, `deploy/compose-images/go.yml`, and `deploy/compose-images/java-kotlin.yml`
- [X] T021 [US2] Inject `QDRANT_API_PORT` into all source-build presets in `deploy/compose/generic.yml`, `deploy/compose/python.yml`, `deploy/compose/javascript.yml`, `deploy/compose/typescript.yml`, `deploy/compose/csharp.yml`, `deploy/compose/go.yml`, and `deploy/compose/java-kotlin.yml`
- [X] T022 [US2] Ensure all runtime Qdrant URLs use `QDRANT_API_PORT` for internal traffic in `services/mcp-server/src/search_repository.py`, `services/mcp-server/src/ingestion_pipeline/vector_upsert_repository.py`, and `services/file-indexer/src/ingestion_pipeline/vector_upsert_repository.py`
- [X] T023 [US2] Register US2 port-isolation regression in `scripts/tests/quality_stability_e2e.ps1` and `scripts/tests/run_quality_stability_suite.ps1`

**Checkpoint**: US2 is done when external port changes do not affect internal Qdrant connectivity.

---

## Phase 5: User Story 3 - Onboarding and Regression Transparency (Priority: P3)

**Goal**: Users should configure MCP endpoint and ports correctly on first run, with automated regressions guarding behavior.

**Independent Test**: Follow quickstart on clean Docker host and complete run -> ingestion -> search using documented MCP endpoint and port settings.

### Tests for User Story 3

- [X] T024 [P] [US3] Add MCP endpoint smoke checks (`/mcp`, `/.well-known/mcp`) in `scripts/tests/mcp_transport_compatibility_smoke.ps1`
- [X] T025 [P] [US3] Extend quality suite artifact output for new regression scenarios in `scripts/tests/run_quality_stability_suite.ps1` and `tests/artifacts/quality-stability/.gitkeep`

### Implementation for User Story 3

- [X] T026 [US3] Update onboarding docs with MCP endpoint and Qdrant port semantics in `README.md`, `docs/quickstart.md`, `docs/configuration.md`, and `docs/compose-presets.md`
- [X] T027 [US3] Update MCP client example config to transport endpoint `/mcp` in `docs/mcp-client-config.example.json`
- [X] T028 [US3] Update release checklist for patch validation and image publication checks in `docs/release-checklist.md`
- [X] T029 [US3] Add release notes entry for this feature in `CHANGELOG.md`

**Checkpoint**: US3 is done when onboarding and regression docs accurately reflect runtime behavior.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency checks and release readiness.

- [X] T030 [P] Run full quality stability suite and archive outputs in `scripts/tests/run_quality_stability_suite.ps1` and `tests/artifacts/quality-stability/`
- [X] T031 Verify OpenAPI contract alignment with implemented behavior in `services/mcp-server/openapi/mcp-transport.openapi.yaml` and `specs/010-mcp-transport/contracts/qdrant-ingestion-reliability.openapi.yaml`
- [X] T032 [P] Validate quickstart commands against compose image preset defaults in `docs/quickstart.md` and `deploy/compose-images/generic.yml`
- [X] T033 Prepare release version bump and patch tag notes in `VERSION` and `CHANGELOG.md`

---

## Dependencies & Execution Order

- Setup (Phase 1) -> Foundational (Phase 2) -> US1 (Phase 3) -> US2 (Phase 4) -> US3 (Phase 5) -> Polish (Phase 6)
- US1 is the MVP and should be delivered first.
- US2 depends on Foundational and benefits from US1 persistence behavior.
- US3 depends on finalized behavior from US1 and US2.

## Dependency Graph

- `US1 -> US2 -> US3`

## Parallel Execution Examples

- **US1**: Run `T011`, `T012`, and `T013` in parallel, then execute `T014`-`T017` sequentially.
- **US2**: Run `T018` and `T019` in parallel, then execute `T020` and `T021` in parallel before `T022` and `T023`.
- **US3**: Run `T024` and `T025` in parallel, then execute `T026`-`T029`.

## Implementation Strategy

1. Deliver MVP by finishing Phase 1, Phase 2, and US1.
2. Add resilient multi-project networking behavior with US2.
3. Finalize onboarding, release notes, and regression transparency with US3.
4. Complete polish phase and release checks.
