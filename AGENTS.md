# ndlss-memory Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-21

## Active Technologies
- Python 3.12 (mcp-server), POSIX shell (file-indexer runtime), Docker Compose v2 + Flask API (`mcp-server`), Qdrant HTTP API, Docker Compose CLI (002-full-scan)
- Qdrant storage, workspace filesystem mount (read-only), runtime scan job reports (002-full-scan)
- Python 3.12 for service runtime, Docker Compose v2 for orchestration + Flask API service, Qdrant HTTP API, embedding provider adapter, file-indexing pipeline modules (003-chunking-embeddings-pipeline)
- Qdrant vector collections, workspace file mount, ingestion run state in service memory with summary persistence (003-chunking-embeddings-pipeline)
- Python 3.12 (`mcp-server`, модули ingestion), POSIX shell для runtime entrypoint + Flask API (`mcp-server`), встроенные Python-модули `hashlib`/`pathlib`, Qdrant HTTP API, Docker Compose v2 (004-indexing-idempotency)
- Qdrant коллекции чанков, runtime in-memory state для запусков синхронизации, workspace bind mount (004-indexing-idempotency)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` workers), Docker Compose v2 + Git CLI (`git diff --name-status --find-renames`), Flask, PyYAML, Qdrant HTTP API (005-delta-after-commit)
- Qdrant коллекция `workspace_chunks`, in-memory runtime state для job status, workspace bind mount (005-delta-after-commit)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), Docker Compose v2 + Flask, PyYAML, Qdrant HTTP API, существующие ingestion/idempotency state-модули (006-mcp-search-tools)
- Qdrant коллекция `workspace_chunks`, in-memory state для MCP job/request tracking, bind-mounted workspace (006-mcp-search-tools)
- Python 3.12 (`mcp-server`), POSIX shell runtime в контейнере + Flask, PyYAML, стандартные средства управления процессами и таймаутами, Docker Compose policy (007-secure-mcp-commands)
- in-memory state для статусов выполнения + append-only аудит в файловом хранилище контейнера (007-secure-mcp-commands)
- Python 3.12 (сервисы и unit-проверки), PowerShell 7+ (compose/e2e orchestration) + pytest, Flask, PyYAML, Docker Compose CLI v2 (008-quality-stability-tests)
- Qdrant (`qdrant_data` volume), файловые fixtures и markdown-отчеты в `tests/` (008-quality-stability-tests)

- Docker Compose Specification (CLI v2), YAML 1.2 + Docker Engine, Docker Compose CLI, контейнерные образы `qdrant`, `file-indexer`, `mcp-server` (001-base-docker-compose)

## Project Structure

```text
src/
tests/
```

## Commands

# Add commands for Docker Compose Specification (CLI v2), YAML 1.2

## Code Style

Docker Compose Specification (CLI v2), YAML 1.2: Follow standard conventions

## Recent Changes
- 008-quality-stability-tests: Added Python 3.12 (сервисы и unit-проверки), PowerShell 7+ (compose/e2e orchestration) + pytest, Flask, PyYAML, Docker Compose CLI v2
- 007-secure-mcp-commands: Added Python 3.12 (`mcp-server`), POSIX shell runtime в контейнере + Flask, PyYAML, стандартные средства управления процессами и таймаутами, Docker Compose policy
- 006-mcp-search-tools: Added Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), Docker Compose v2 + Flask, PyYAML, Qdrant HTTP API, существующие ingestion/idempotency state-модули


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->


