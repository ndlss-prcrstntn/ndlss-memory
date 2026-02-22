# Changelog

## 0.1.7 - 2026-02-22

- Fixed MCP ingestion persistence reliability:
  - enabled HTTP upsert defaults for MCP ingestion flow
  - ingestion now surfaces persistence failures as `INGESTION_PERSISTENCE_FAILED`
  - ingestion status/summary now include persistence diagnostics
- Fixed Qdrant networking model for multi-project stacks:
  - introduced `QDRANT_API_PORT` for internal service traffic
  - kept `QDRANT_PORT` for host mapping only
  - updated compose presets (`deploy/compose-images/*`, `deploy/compose/*`) and local compose files
- Added regression coverage:
  - `scripts/tests/us1_ingestion_collection_creation.ps1`
  - `scripts/tests/us2_custom_qdrant_external_port.ps1`
  - integrated new stages into quality runner/suite
- Added/updated tests:
  - search repository internal-port resolution tests
  - vector upsert repository env-resolution tests (`mcp-server`, `file-indexer`)
- Updated docs and release checklist:
  - `README.md`, `docs/quickstart.md`, `docs/configuration.md`, `docs/compose-presets.md`
  - `docs/release-checklist.md`

## 0.1.6 - 2026-02-22

- Added full MCP transport compatibility surface:
  - `POST /mcp` (streamable HTTP JSON-RPC)
  - `GET /sse` and `POST /messages` (legacy SSE fallback)
  - `GET /.well-known/mcp` discovery endpoint
- Added MCP method support:
  - `initialize`, `notifications/initialized`, `ping`
  - `tools/list`, `tools/call`
- Added MCP tool registry and adapters for:
  - `semantic_search`
  - `get_source_by_id`
  - `get_metadata_by_id`
  - `start_ingestion`
  - `get_ingestion_status`
- Added JSON-RPC error mapping with machine-readable `errorCode/details/retryable`.
- Added MCP transport unit, contract, and integration artifacts.
- Added MCP transport compatibility smoke script and quality-gate integration.
- Updated onboarding/docs to use MCP endpoint `http://localhost:8080/mcp`.

## 0.1.5 - 2026-02-22

- Added `GET /` root endpoint in `mcp-server` that returns a structured catalog of all available API commands.
- Added unit tests for the root command catalog endpoint to prevent regressions.

## 0.1.4 - 2026-02-22

- Fixed ingestion runtime in containerized `mcp-server` images:
  - bundled `ingestion_pipeline` and `delta_after_commit` modules into `mcp-server` image
  - updated Dockerfile to copy full `src/` tree
- Fixed no-clone compose startup validation by adding missing command runtime defaults to all presets:
  - `COMMAND_ALLOWLIST`
  - `COMMAND_TIMEOUT_SECONDS`

## 0.1.3 - 2026-02-22

- Changed default Docker Hub namespace in image presets to `ndlss`.
- Updated quickstart/preset examples to use `ndlss` namespace by default.
- Added release bump and workflow input examples for `0.1.3`.

## 0.1.2 - 2026-02-22

- Added image-based compose presets (`deploy/compose-images/*`) as the default no-clone startup path.
- Added Docker Hub publishing workflow (`.github/workflows/docker-release.yml`) for `file-indexer` and `mcp-server`.
- Added language and stack coverage improvements:
  - new presets: `typescript`, `csharp`
  - updated docs for multi-project parallel compose usage (`-p` + custom ports)
- Updated quickstart and preset documentation to use image defaults (`latest`) with optional tag pinning.

## 0.1.1 - 2026-02-22

- Added no-clone onboarding: users can start the stack in any project folder with one command.
- Added remote-compose presets for multiple stacks:
  - `generic`
  - `python`
  - `typescript`
  - `javascript`
  - `java-kotlin`
  - `csharp`
  - `go`
- Added preset documentation and runtime source pinning (`NDLSS_GIT_REF`) for reproducible startup.
- Switched the primary `README.md` to English and added localized READMEs (RU, FR, DE, ZH-CN, KO, JA).

## 0.1.0 - 2026-02-22

- Initial public baseline of `ndlss-memory`.
- Docker Compose stack with `qdrant`, `file-indexer`, and `mcp-server`.
- Indexing capabilities: full-scan, chunking + embeddings, idempotency, delta-after-commit.
- MCP features: semantic search tools, source/metadata retrieval, secure command execution runtime.
- Quality and stability coverage: unit, integration, contract, and e2e test suites.
