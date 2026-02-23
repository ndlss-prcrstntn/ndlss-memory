# Changelog

## 0.2.8 - 2026-02-23

- Tuned default docs hybrid/reranking profile for medium-to-large repositories:
  - `DOCS_HYBRID_VECTOR_WEIGHT=0.55`
  - `DOCS_HYBRID_BM25_WEIGHT=0.45`
  - `DOCS_HYBRID_MAX_CANDIDATES=160`
  - `DOCS_RERANK_MAX_CANDIDATES=100`
- Added docs lexical content caching for stable warm-query performance:
  - new `DOCS_SOURCE_CACHE_SIZE` env knob (default `4096`)
  - LRU cache used in docs lexical/rerank content reads.
- Improved docs search pipeline efficiency:
  - reduced duplicate candidate mapping work
  - improved candidate-id reuse between vector and lexical stages.
- Synced runtime env propagation for docs hybrid/rerank settings in both compose files:
  - `docker-compose.yml`
  - `infra/docker/docker-compose.yml`
- Updated documentation and tests for new defaults and lexical fallback behavior.

## 0.2.7 - 2026-02-23

- Added docs-only reranking stage on top of hybrid candidate retrieval for markdown search:
  - `POST /v1/search/docs/query` now returns `appliedStrategy=bm25_plus_vector_rerank_docs_only`;
  - response now includes `fallbackApplied`;
  - docs result items now include `rankingSignals.rerank` along with lexical/semantic signals.
- Added reranking reliability controls:
  - `DOCS_RERANK_ENABLED`
  - `DOCS_RERANK_FAIL_OPEN`
  - `DOCS_RERANK_MAX_CANDIDATES`
  - `DOCS_RERANK_FORCE_FAILURE` (test/degradation simulation flag)
- Added controlled degradation behavior:
  - fail-open path returns valid docs payload with `fallbackApplied=true`;
  - fail-closed path returns `DOCS_RERANKING_UNAVAILABLE` (HTTP 503).
- Preserved backward compatibility for non-docs search:
  - `POST /v1/search/semantic` contract remains unchanged.
- Updated OpenAPI, docs, and feature artifacts for reranking behavior:
  - `services/mcp-server/openapi/mcp-search-tools.openapi.yaml`
  - `README.md`, `docs/configuration.md`, `docs/quickstart.md`
  - `specs/017-md-hybrid-reranking/*`
- Added/updated coverage for reranking scoring, fallback, scope isolation, and contract payloads:
  - `tests/unit/mcp_server/test_search_repository_docs.py`
  - `tests/unit/mcp_server/test_docs_hybrid_search_service.py`
  - `tests/unit/mcp_server/test_mcp_docs_search_tool.py`
  - `tests/contract/test_docs_search_contract.py`
  - `tests/integration/test_docs_search_hybrid.py`
  - `tests/integration/test_docs_search_baseline.py`
  - `tests/artifacts/hybrid-reranking/verification-report.md`

## 0.2.6 - 2026-02-23

- Added hybrid docs search (BM25 + vector) only for markdown docs collection:
  - `POST /v1/search/docs/query` now returns `appliedStrategy=bm25_plus_vector_docs_only`;
  - docs result items now include `rankingSignals.lexical` and `rankingSignals.semantic`;
  - deterministic tie-break for equal scores (`documentPath`, then `chunkIndex`).
- Added docs hybrid ranking controls in environment/config docs:
  - `DOCS_HYBRID_VECTOR_WEIGHT`
  - `DOCS_HYBRID_BM25_WEIGHT`
  - `DOCS_HYBRID_MAX_CANDIDATES`
- Extended error contract for docs search with `DOCS_COLLECTION_UNAVAILABLE` (HTTP 503).
- Preserved backward compatibility for non-docs search:
  - `POST /v1/search/semantic` response shape unchanged.
- Added/updated tests for hybrid behavior, scope isolation, deterministic ranking, and error payloads:
  - `tests/unit/mcp_server/test_docs_hybrid_search_service.py`
  - `tests/integration/test_docs_search_hybrid.py`
  - updates in docs-search unit/contract/integration suites.
- Updated docs and feature artifacts:
  - `README.md`, `docs/configuration.md`, `docs/quickstart.md`
  - `specs/016-md-hybrid-search/*`
  - `tests/artifacts/hybrid-search/verification-report.md`

## 0.2.5 - 2026-02-23

- Added isolated docs indexing and search baseline:
  - separate docs collection (`QDRANT_DOCS_COLLECTION_NAME`) without mixing code chunks;
  - docs indexing config (`DOCS_INDEX_FILE_TYPES`, `DOCS_INDEX_EXCLUDE_PATTERNS`);
  - docs indexing APIs:
    - `POST /v1/indexing/docs/jobs`
    - `GET /v1/indexing/docs/jobs/{runId}/summary`
  - docs search API:
    - `POST /v1/search/docs/query`
- Added docs-specific MCP search tool:
  - `search_docs` available in MCP `tools/list`;
  - integrated into MCP transport handlers and adapter flow.
- Added deterministic docs chunk identity and metadata improvements:
  - stable docs chunk key by `path + chunkIndex`;
  - `chunkIndex` exposed in metadata/search payloads for traceability.
- Added docs collection bootstrap/runtime resilience:
  - startup bootstrap now ensures docs collection exists;
  - runtime self-heal for missing collections remains active in upsert paths.
- Added test coverage for docs scope:
  - unit/integration/contract tests for docs indexing, docs search API, and MCP docs tool;
  - quality suite artifacts refreshed and passed.
- Updated OpenAPI and user docs for 0.2.5 docs capabilities.

## 0.2.4 - 2026-02-22

- Added indexing run limits for blast-radius control in large repositories:
  - `maxTraversalDepth` and `maxFilesPerRun` accepted by full-scan and ingestion start APIs;
  - environment defaults via `INDEX_MAX_TRAVERSAL_DEPTH` and `INDEX_MAX_FILES_PER_RUN`;
  - deterministic candidate ordering with consistent limit application.
- Added limit-aware summary diagnostics:
  - `appliedLimits` block in full-scan and ingestion summary payloads;
  - explicit skip reasons `LIMIT_DEPTH_EXCEEDED` and `LIMIT_MAX_FILES_REACHED`.
- Updated runtime/config/openapi surfaces:
  - compose/env propagation across local and image-based presets;
  - validation/default handling in `file-indexer` startup scripts;
  - synchronized OpenAPI contracts (`mcp-server` + feature contract).
- Added regression coverage for limits:
  - unit tests for deterministic selection with depth/max-files limits;
  - integration tests for full-scan/ingestion consistency, backward compatibility, and summary reporting;
  - contract tests for ingestion validation and full-scan/ingestion summary payloads.
- Updated docs and quality scripts:
  - `README.md`, `docs/configuration.md`, and feature quickstart;
  - smoke scripts `us2_full_scan_filtering.ps1` and `us2_quality_search_flow.ps1` now verify applied limits.

## 0.2.3 - 2026-02-22

- Added continuous watch indexing mode (`INDEX_MODE=watch`) with incremental create/update/delete processing:
  - watcher runtime models/state/coalescing/orchestration in `mcp-server`;
  - runtime validation and compose/env support for watch-specific settings;
  - compatibility preserved for `full-scan` and `delta-after-commit` modes.
- Added watch-mode observability APIs and contract updates:
  - `GET /v1/indexing/watch/status` and `GET /v1/indexing/watch/summary`;
  - expanded readiness/status summaries with watch activity fields;
  - synchronized OpenAPI docs for service and feature contracts.
- Added watch-mode quality coverage:
  - unit tests for watch state and retry policy;
  - integration tests for incremental updates, deletes, burst handling, recovery, observability, and regression compatibility;
  - contract tests for watch status/summary endpoints.
- Stabilized compose-based quality runs by isolating test ports and hardening startup smoke scripts:
  - centralized test port defaults (`TEST_MCP_PORT=18080`, `TEST_QDRANT_PORT=16333`);
  - removed hardcoded `localhost:8080/6333` usage in quality scripts;
  - improved `startup_preflight_smoke` compose invocation handling to prevent false failures.

## 0.2.2 - 2026-02-22

- Added first-run bootstrap indexing for fresh workspaces:
  - auto-creates collection when missing;
  - auto-starts initial ingestion on startup;
  - persists bootstrap markers and skips expensive re-bootstrap on restart.
- Extended startup/readiness observability with bootstrap diagnostics:
  - `bootstrap`, `collection`, and `bootstrapFailure` blocks in readiness/status payloads;
  - structured bootstrap lifecycle logs (`started`, `skipped`, `failed`, `finished`).
- Added bootstrap regression coverage and tooling:
  - unit tests for orchestrator skip/retry/concurrency behavior;
  - integration/contract tests for readiness bootstrap payloads and fail-fast diagnostics;
  - `scripts/tests/startup_bootstrap_smoke.ps1`;
  - UTF-8 validation utility `scripts/tests/verify_utf8_encoding.ps1`;
  - quality gate stage `startup_bootstrap`.

## 0.2.1 - 2026-02-22

- Added startup preflight checks for `mcp-server` and `file-indexer`:
  - Qdrant reachability check
  - workspace existence/readability check
  - git availability check for `INDEX_MODE=delta-after-commit`
- Added fail-fast startup behavior with structured failure reports:
  - `errorCode`, `message`, `details`, `failedChecks`, `recommendedActions`
- Added startup readiness observability:
  - new endpoint `GET /v1/system/startup/readiness`
  - startup readiness snapshot embedded into `GET /v1/system/config`
  - unified startup-ready log records in `mcp-server` and `file-indexer`
- Added startup preflight configuration knobs in env/compose presets:
  - `STARTUP_PREFLIGHT_ENABLED`
  - `STARTUP_PREFLIGHT_TIMEOUT_SECONDS`
  - `STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA`
  - `STARTUP_READY_SUMMARY_LOG_ENABLED`
  - `MCP_ENDPOINT_PATH`
- Added tests and smoke scripts:
  - unit tests for preflight models/checks/readiness endpoint
  - `scripts/tests/startup_preflight_smoke.ps1`
  - `scripts/tests/us3_startup_backward_compat.ps1`
- Extended quality pipeline with `startup_preflight` stage in
  `scripts/tests/quality_gate_runner.ps1` and suite output wiring.
- Updated docs and OpenAPI contracts:
  - [README](README.md)
  - [Quickstart](docs/quickstart.md)
  - [Configuration](docs/configuration.md)
  - [Compose presets](docs/compose-presets.md)
  - `services/mcp-server/openapi/compose-observability.openapi.yaml`
  - `specs/011-startup-preflight-summary/contracts/startup-preflight-readiness.openapi.yaml`
- Stabilized integration regression orchestration:
  - fixed env-ordering race in `scripts/tests/ingestion_compose_regression.ps1`
  - added resilient compose startup retries for flaky Docker health timing
  - ensured `quality_gate_runner` completes with all stages passed
- Updated [Roadmap 0.3.0](docs/roadmaps/0.3.0.md) to mark completed startup preflight/readiness items.

## 0.2.0 - 2026-02-22

- Promoted `ndlss-memory` baseline to `0.2.0`.
- Added versioned roadmap documentation:
  - [Roadmaps index](docs/roadmaps/README.md)
  - [Roadmap 0.2.0](docs/roadmaps/0.2.0.md)
- Formalized roadmap `0..10` completion snapshot for the `0.2.0` release line.
- Consolidated production-ready stack capabilities from `0.1.x`:
  - no-clone startup with image presets (`generic`, `python`, `typescript`, `javascript`, `java-kotlin`, `csharp`, `go`)
  - indexing pipelines (`full-scan`, `ingestion`, `idempotency`, `delta-after-commit`)
  - MCP transport (`/mcp`, `/.well-known/mcp`, legacy SSE fallback)
  - secure MCP command execution runtime
  - Qdrant persistence reliability (`QDRANT_API_PORT`, ingestion HTTP upsert defaults)
  - quality/stability coverage (unit, integration, contract, E2E smoke flows)
- Updated README links to include roadmap docs for release tracking.

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
  - [README](README.md), [Quickstart](docs/quickstart.md), [Configuration](docs/configuration.md), [Compose presets](docs/compose-presets.md)
  - [Release checklist](docs/release-checklist.md)

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
- Switched the primary [README](README.md) to English and added localized READMEs (RU, FR, DE, ZH-CN, KO, JA).

## 0.1.0 - 2026-02-22

- Initial public baseline of `ndlss-memory`.
- Docker Compose stack with `qdrant`, `file-indexer`, and `mcp-server`.
- Indexing capabilities: full-scan, chunking + embeddings, idempotency, delta-after-commit.
- MCP features: semantic search tools, source/metadata retrieval, secure command execution runtime.
- Quality and stability coverage: unit, integration, contract, and e2e test suites.
