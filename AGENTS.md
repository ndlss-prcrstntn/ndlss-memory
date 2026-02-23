# ndlss-memory Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-21

## Active Technologies
- Python 3.12 (mcp-server), POSIX shell (file-indexer runtime), Docker Compose v2 + Flask API (`mcp-server`), Qdrant HTTP API, Docker Compose CLI (002-full-scan)
- Qdrant storage, workspace filesystem mount (read-only), runtime scan job reports (002-full-scan)
- Python 3.12 for service runtime, Docker Compose v2 for orchestration + Flask API service, Qdrant HTTP API, embedding provider adapter, file-indexing pipeline modules (003-chunking-embeddings-pipeline)
- Qdrant vector collections, workspace file mount, ingestion run state in service memory with summary persistence (003-chunking-embeddings-pipeline)
- Python 3.12 (`mcp-server`, ������ ingestion), POSIX shell ��� runtime entrypoint + Flask API (`mcp-server`), ���������� Python-������ `hashlib`/`pathlib`, Qdrant HTTP API, Docker Compose v2 (004-indexing-idempotency)
- Qdrant ��������� ������, runtime in-memory state ��� �������� �������������, workspace bind mount (004-indexing-idempotency)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` workers), Docker Compose v2 + Git CLI (`git diff --name-status --find-renames`), Flask, PyYAML, Qdrant HTTP API (005-delta-after-commit)
- Qdrant ��������� `workspace_chunks`, in-memory runtime state ��� job status, workspace bind mount (005-delta-after-commit)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), Docker Compose v2 + Flask, PyYAML, Qdrant HTTP API, ������������ ingestion/idempotency state-������ (006-mcp-search-tools)
- Qdrant ��������� `workspace_chunks`, in-memory state ��� MCP job/request tracking, bind-mounted workspace (006-mcp-search-tools)
- Python 3.12 (`mcp-server`), POSIX shell runtime � ���������� + Flask, PyYAML, ����������� �������� ���������� ���������� � ����������, Docker Compose policy (007-secure-mcp-commands)
- in-memory state ��� �������� ���������� + append-only ����� � �������� ��������� ���������� (007-secure-mcp-commands)
- Python 3.12 (������� � unit-��������), PowerShell 7+ (compose/e2e orchestration) + pytest, Flask, PyYAML, Docker Compose CLI v2 (008-quality-stability-tests)
- Qdrant (`qdrant_data` volume), �������� fixtures � markdown-������ � `tests/` (008-quality-stability-tests)
- Python 3.12 (`mcp-server` runtime) + Flask, PyYAML, ����������� Python JSON/HTTP ���������, Docker Compose v2 (009-mcp-transport)
- Qdrant ��������� `workspace_chunks`; in-memory ��������� MCP-������/��������; ������������ runtime state-������ (009-mcp-transport)
- Python 3.12 (runtime � �������� �������), PowerShell 7+ (orchestration/���������), Docker Compose Specification v2 + Flask, PyYAML, ���������� Python urllib/json/hashlib, Docker Compose CLI, Qdrant HTTP API (010-mcp-transport)
- Qdrant ��������� `workspace_chunks`, ��������� workspace ����� ����� bind mount, in-memory runtime state ��� job tracking (010-mcp-transport)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` entrypoint/runtime), Docker Compose v2 + Flask, PyYAML, ���������� Python-������ (`pathlib`, `subprocess`, `urllib`/HTTP-������), Docker Compose runtime env (011-startup-preflight-summary)
- Qdrant (`workspace_chunks`), bind mount workspace (`/workspace`), in-memory runtime state ��� job/status (011-startup-preflight-summary)
- Python 3.12 (`mcp-server` и ingestion runtime), POSIX shell runtime в контейнере (`file-indexer`) + Flask, PyYAML, существующие модули `ingestion_pipeline/*`, `idempotency_state`, `ingestion_state`, файловый watcher-адаптер в Python runtime (013-watch-mode-indexing)
- Qdrant (`workspace_chunks`, служебные коллекции состояния), bind-mounted workspace (`/workspace`), in-memory состояние watch-run и очереди событий (013-watch-mode-indexing)
- Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), PowerShell 7+ (test orchestration) + Flask API, PyYAML, существующие модули индексации (`full-scan`, `ingestion`), Docker Compose v2, Qdrant HTTP API (014-indexing-run-limits)
- Qdrant коллекции (`workspace_chunks`), bind-mounted workspace (`/workspace`), runtime summary/state в памяти сервиса (014-indexing-run-limits)
- Python 3.12 (`mcp-server`, `file-indexer`), POSIX shell runtime, PowerShell 7+ для e2e/quality orchestration + Flask API, PyYAML, существующие модули `ingestion_pipeline/*`, runtime bootstrap services, Docker Compose v2, Qdrant HTTP API (015-docs-index-baseline)
- Qdrant коллекции (`workspace_chunks` + новая docs-коллекция), bind-mounted workspace (`/workspace`), in-memory run state/summaries (015-docs-index-baseline)

- Docker Compose Specification (CLI v2), YAML 1.2 + Docker Engine, Docker Compose CLI, ������������ ������ `qdrant`, `file-indexer`, `mcp-server` (001-base-docker-compose)

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
- 015-docs-index-baseline: Added Python 3.12 (`mcp-server`, `file-indexer`), POSIX shell runtime, PowerShell 7+ для e2e/quality orchestration + Flask API, PyYAML, существующие модули `ingestion_pipeline/*`, runtime bootstrap services, Docker Compose v2, Qdrant HTTP API
- 014-indexing-run-limits: Added Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), PowerShell 7+ (test orchestration) + Flask API, PyYAML, существующие модули индексации (`full-scan`, `ingestion`), Docker Compose v2, Qdrant HTTP API
- 013-watch-mode-indexing: Added Python 3.12 (`mcp-server` и ingestion runtime), POSIX shell runtime в контейнере (`file-indexer`) + Flask, PyYAML, существующие модули `ingestion_pipeline/*`, `idempotency_state`, `ingestion_state`, файловый watcher-адаптер в Python runtime


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->


