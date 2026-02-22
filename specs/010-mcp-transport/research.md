# Research: MCP Ingestion and Qdrant Port Reliability

## Decision 1: Separate Internal and External Qdrant Ports

- **Decision**: Introduce explicit internal service port variable (`QDRANT_API_PORT`, default `6333`) and keep `QDRANT_PORT` only for host exposure (`host:container` mapping).
- **Rationale**: In Docker Compose, service-to-service communication must use container network coordinates. Reusing host port overrides for internal traffic creates connection failures when users run multiple stacks with custom external ports.
- **Alternatives considered**:
  - Keep single `QDRANT_PORT` for both internal and external use.
    - Rejected: breaks internal connectivity for non-default host ports.
  - Hardcode internal `6333` without separate variable.
    - Rejected: less explicit and harder to reason about in docs/config inspection.

## Decision 2: Force HTTP Upsert for MCP-Initiated Ingestion

- **Decision**: Ensure `mcp-server` runtime environment enables HTTP upsert path for ingestion (`INGESTION_ENABLE_QDRANT_HTTP=1`) with explicit timeout and vector-size defaults.
- **Rationale**: Current behavior may report successful ingestion while storing vectors only in in-memory repository, which does not create persistent Qdrant collection and leads to empty search results.
- **Alternatives considered**:
  - Keep default off and ask users to set env manually.
    - Rejected: violates quickstart reproducibility and causes recurring support issues.
  - Trigger a post-run sync to Qdrant from in-memory state.
    - Rejected: adds complexity and new failure mode.

## Decision 3: Add Regression Gates for Collection Creation and Custom External Port

- **Decision**: Add automated quality checks:
  - ingestion via MCP must create `workspace_chunks` when missing and yield `points/count > 0`;
  - ingestion/search must stay healthy with non-default external `QDRANT_PORT`.
- **Rationale**: These two scenarios directly map to observed production-like failures and need permanent CI protection.
- **Alternatives considered**:
  - Only test default port path.
    - Rejected: misses the multi-project parallel usage risk.
  - Only unit-test URL composition logic.
    - Rejected: does not validate real container-network behavior.

## Decision 4: Clarify Public Onboarding for MCP Endpoint and Port Semantics

- **Decision**: Update `README.md`, `docs/quickstart.md`, `docs/compose-presets.md`, and `docs/configuration.md` to explicitly state:
  - MCP transport endpoint is `/mcp`;
  - `QDRANT_PORT` is external host port;
  - internal service port uses `QDRANT_API_PORT` (default `6333`);
  - ingestion persistence requires HTTP upsert enabled in runtime.
- **Rationale**: Most user failures came from ambiguous endpoint/port assumptions, not from missing runtime capabilities.
- **Alternatives considered**:
  - Keep details only in troubleshooting section.
    - Rejected: too late in user journey; should be visible in primary quickstart.
