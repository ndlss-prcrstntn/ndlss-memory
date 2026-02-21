# ndlss-memory Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-21

## Active Technologies
- Python 3.12 (mcp-server), POSIX shell (file-indexer runtime), Docker Compose v2 + Flask API (`mcp-server`), Qdrant HTTP API, Docker Compose CLI (002-full-scan)
- Qdrant storage, workspace filesystem mount (read-only), runtime scan job reports (002-full-scan)
- Python 3.12 for service runtime, Docker Compose v2 for orchestration + Flask API service, Qdrant HTTP API, embedding provider adapter, file-indexing pipeline modules (003-chunking-embeddings-pipeline)
- Qdrant vector collections, workspace file mount, ingestion run state in service memory with summary persistence (003-chunking-embeddings-pipeline)
- Python 3.12 (`mcp-server`, модули ingestion), POSIX shell для runtime entrypoint + Flask API (`mcp-server`), встроенные Python-модули `hashlib`/`pathlib`, Qdrant HTTP API, Docker Compose v2 (004-indexing-idempotency)
- Qdrant коллекции чанков, runtime in-memory state для запусков синхронизации, workspace bind mount (004-indexing-idempotency)

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
- 004-indexing-idempotency: Added Python 3.12 (`mcp-server`, модули ingestion), POSIX shell для runtime entrypoint + Flask API (`mcp-server`), встроенные Python-модули `hashlib`/`pathlib`, Qdrant HTTP API, Docker Compose v2
- 003-chunking-embeddings-pipeline: Added Python 3.12 for service runtime, Docker Compose v2 for orchestration + Flask API service, Qdrant HTTP API, embedding provider adapter, file-indexing pipeline modules
- 002-full-scan: Added Python 3.12 (mcp-server), POSIX shell (file-indexer runtime), Docker Compose v2 + Flask API (`mcp-server`), Qdrant HTTP API, Docker Compose CLI


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->

