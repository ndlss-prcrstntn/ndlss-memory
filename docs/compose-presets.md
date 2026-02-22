# Compose Presets (No Clone Required)

These presets are intended for users who want to run `ndlss-memory` in any existing project directory without cloning this repository.

All presets:
- Build services directly from remote git contexts.
- Mount your current folder as `/workspace` (read-only).
- Start `qdrant`, `file-indexer`, and `mcp-server`.
- Support source pinning via `NDLSS_GIT_REF` (`main`, tag, or commit SHA).

## Presets

- `deploy/compose/generic.yml`: best default for mixed/polyglot repos.
- `deploy/compose/python.yml`: Python and notebooks.
- `deploy/compose/typescript.yml`: TypeScript-first repositories.
- `deploy/compose/javascript.yml`: JavaScript/TypeScript web repos.
- `deploy/compose/java-kotlin.yml`: Java/Kotlin repos.
- `deploy/compose/csharp.yml`: .NET/C# repositories.
- `deploy/compose/go.yml`: Go repos.

## One-line start (PowerShell)

```powershell
$preset = "python"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d --build
```

## One-line start (bash)

```bash
preset=python; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d --build
```

## Configuration overrides

You can still override any setting at runtime, for example:

```powershell
$env:INDEX_FILE_TYPES=".md,.txt,.py,.sql"
$env:INDEX_EXCLUDE_PATTERNS=".git,node_modules,.venv"
docker compose -f ndlss-compose.yml up -d --build
```

## Stop

```powershell
docker compose -f ndlss-compose.yml down
```
