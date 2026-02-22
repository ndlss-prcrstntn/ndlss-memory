# Changelog

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
