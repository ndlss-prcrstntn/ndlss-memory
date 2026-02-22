# ndlss-memory

Language versions: [English](README.md) | [Russian](docs/i18n/README.ru.md) | [French](docs/i18n/README.fr.md) | [German](docs/i18n/README.de.md) | [Chinese](docs/i18n/README.zh-CN.md) | [Korean](docs/i18n/README.ko.md) | [Japanese](docs/i18n/README.ja.md)

`ndlss-memory` is a local memory layer for MCP agents.
It indexes files from your workspace, stores vectors and metadata in Qdrant, and exposes search + operational APIs via `mcp-server`.

## One-command start (no repository clone)

Run inside any project directory.

### PowerShell

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

### bash

```bash
preset=generic; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d
```

- Replace `generic` with `python`, `typescript`, `javascript`, `java-kotlin`, `csharp`, or `go`.
- Optional: pin image version with `NDLSS_IMAGE_TAG` (default is `latest`).
- Optional: change Docker Hub namespace with `NDLSS_DOCKERHUB_NAMESPACE` (default: `ndlss`).
- Source-build presets are still available in [`deploy/compose/`](deploy/compose/) when you explicitly want to build from source.
- Full guide: [Quickstart](docs/quickstart.md)
- Preset details: [Compose presets](docs/compose-presets.md)

### Run multiple stacks in parallel (different projects)

Use a unique compose project name and unique host ports per project:

```powershell
$env:MCP_PORT="18080"
$env:QDRANT_PORT="16333"
$env:QDRANT_API_PORT="6333"
docker compose -p ndlss-project-a -f ndlss-compose.yml up -d
```

For another project:

```powershell
$env:MCP_PORT="28080"
$env:QDRANT_PORT="26333"
$env:QDRANT_API_PORT="6333"
docker compose -p ndlss-project-b -f ndlss-compose.yml up -d
```

This keeps containers, networks, and volumes isolated between projects.
`QDRANT_PORT` controls host exposure only; internal service traffic uses `QDRANT_API_PORT` (default `6333`).

## How indexing works across different projects

The indexer behavior is preset-driven and still fully configurable:

- `INDEX_FILE_TYPES`: which file extensions are indexed.
- `INDEX_EXCLUDE_PATTERNS`: directories/files to skip.
- `INDEX_MODE=full-scan`: indexes the current workspace.
- `INDEX_MODE=delta-after-commit`: for git repos, indexes only changed files.

Practical model:

- Choose the closest preset for your stack.
- Start with defaults.
- Override environment variables only where needed.
- Keep `INGESTION_ENABLE_QDRANT_HTTP=1` to persist ingestion results in Qdrant.

This gives a good out-of-box setup for different codebases while keeping one runtime architecture.

## Startup preflight

By default, both `mcp-server` and `file-indexer` run startup preflight checks before entering ready state:

- Qdrant reachability (`QDRANT_HOST` + `QDRANT_API_PORT`)
- workspace path existence/readability (`WORKSPACE_PATH`)
- git availability for `INDEX_MODE=delta-after-commit`

Relevant environment flags:

- `STARTUP_PREFLIGHT_ENABLED` (default `1`)
- `STARTUP_PREFLIGHT_TIMEOUT_SECONDS` (default `3`)
- `STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA` (default `1`)
- `STARTUP_READY_SUMMARY_LOG_ENABLED` (default `1`)
- `MCP_ENDPOINT_PATH` (default `/mcp`)

## Preset matrix

| Preset | Best for | Main indexed types |
|---|---|---|
| `generic` | polyglot repos | `.md,.txt,.json,.yml,.yaml,.py,.js,.ts,.tsx,.java,.kt,.go,...` |
| `python` | Python apps, notebooks | `.py,.ipynb,.md,.txt,.json,.yaml,.toml,...` |
| `typescript` | TypeScript-first repos | `.ts,.tsx,.mts,.cts,.js,.jsx,.json,.md,...` |
| `javascript` | Node/TS web apps | `.js,.jsx,.ts,.tsx,.mjs,.cjs,.json,.md,...` |
| `java-kotlin` | JVM projects | `.java,.kt,.kts,.xml,.properties,.gradle,...` |
| `csharp` | .NET/C# solutions | `.cs,.csproj,.sln,.props,.targets,.json,.md,...` |
| `go` | Go services/tools | `.go,.mod,.sum,.md,.json,.yml,.yaml` |

## Services

- `qdrant`: vector storage + payload metadata.
- `file-indexer`: full-scan, ingestion, idempotency, delta-after-commit.
- `mcp-server`: status, indexing APIs, semantic search APIs, secure command runtime.

## Core API

System:

- `GET /health`
- `GET /v1/system/status`
- `GET /v1/system/config`
- `GET /v1/system/startup/readiness`

MCP transport:

- `POST /mcp` (JSON-RPC streamable HTTP)
- `GET /sse` and `POST /messages?sessionId=...` (legacy SSE fallback)
- `GET /.well-known/mcp` (discovery)

Search:

- `POST /v1/search/semantic`
- `GET /v1/search/results/{resultId}/source`
- `GET /v1/search/results/{resultId}/metadata`

Indexing:

- `POST /v1/indexing/full-scan/jobs`
- `POST /v1/indexing/ingestion/jobs`
- `POST /v1/indexing/idempotency/jobs`
- `POST /v1/indexing/delta-after-commit/jobs`

## User documentation

- [Quickstart](docs/quickstart.md)
- [Compose presets](docs/compose-presets.md)
- [MCP client config example](docs/mcp-client-config.example.json)
- [Configuration](docs/configuration.md)
- [Release checklist](docs/release-checklist.md)
- [Roadmaps index](docs/roadmaps/README.md)
- [Roadmap 0.2.1](docs/roadmaps/0.2.1.md)
- [Roadmap 0.2.0](docs/roadmaps/0.2.0.md)
- [Contributing](CONTRIBUTING.md)

## Local development (clone-based)

If you are developing `ndlss-memory` itself:

```powershell
powershell -File scripts/dev/up.ps1
```

Run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit
powershell -File scripts/tests/run_quality_stability_suite.ps1
```

## Roadmap status

Roadmap snapshots are versioned in [docs/roadmaps](docs/roadmaps/README.md).
Current baseline release roadmap: [0.2.1](docs/roadmaps/0.2.1.md).
Next planned roadmap: [0.3.0](docs/roadmaps/0.3.0.md).
