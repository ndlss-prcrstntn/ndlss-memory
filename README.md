# ndlss-memory

Language versions: [English](README.md) | [Russian](docs/i18n/README.ru.md) | [French](docs/i18n/README.fr.md) | [German](docs/i18n/README.de.md) | [Chinese](docs/i18n/README.zh-CN.md) | [Korean](docs/i18n/README.ko.md) | [Japanese](docs/i18n/README.ja.md)

`ndlss-memory` is a local memory layer for MCP agents.
It indexes files from your workspace, stores vectors and metadata in Qdrant, and exposes search + operational APIs via `mcp-server`.

## One-command start (no repository clone)

Run inside any project directory.

### PowerShell

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d --build
```

### bash

```bash
preset=generic; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d --build
```

- Replace `generic` with `python`, `javascript`, `java-kotlin`, or `go`.
- Optional: pin remote source with `NDLSS_GIT_REF` (for example `v1.0.0`).
- Full guide: `docs/quickstart.md`
- Preset details: `docs/compose-presets.md`

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

This gives a good out-of-box setup for different codebases while keeping one runtime architecture.

## Preset matrix

| Preset | Best for | Main indexed types |
|---|---|---|
| `generic` | polyglot repos | `.md,.txt,.json,.yml,.yaml,.py,.js,.ts,.tsx,.java,.kt,.go,...` |
| `python` | Python apps, notebooks | `.py,.ipynb,.md,.txt,.json,.yaml,.toml,...` |
| `javascript` | Node/TS web apps | `.js,.jsx,.ts,.tsx,.mjs,.cjs,.json,.md,...` |
| `java-kotlin` | JVM projects | `.java,.kt,.kts,.xml,.properties,.gradle,...` |
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

- `docs/quickstart.md`
- `docs/compose-presets.md`
- `docs/configuration.md`
- `docs/release-checklist.md`
- `CONTRIBUTING.md`

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

All milestones `0` through `10` are currently implemented.
