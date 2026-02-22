# Compose Presets (No Clone Required)

These presets are intended for users who want to run `ndlss-memory` in any existing project directory without cloning this repository.

Image presets:
- Pull prebuilt images from Docker Hub.
- Mount your current folder as `/workspace` (read-only).
- Start `qdrant`, `file-indexer`, and `mcp-server`.
- Support image pinning via `NDLSS_IMAGE_TAG` (default: `latest`).
- Do not hardcode compose project name (supports running many stacks in parallel).

Source-build presets:
- Build services directly from remote git contexts.
- Support source pinning via `NDLSS_GIT_REF` (`main`, tag, or commit SHA).

## Image Presets (Recommended)

- `deploy/compose-images/generic.yml`: best default for mixed/polyglot repos.
- `deploy/compose-images/python.yml`: Python and notebooks.
- `deploy/compose-images/typescript.yml`: TypeScript-first repositories.
- `deploy/compose-images/javascript.yml`: JavaScript/TypeScript web repos.
- `deploy/compose-images/java-kotlin.yml`: Java/Kotlin repos.
- `deploy/compose-images/csharp.yml`: .NET/C# repositories.
- `deploy/compose-images/go.yml`: Go repos.

## Source-Build Presets (Fallback)

- `deploy/compose/generic.yml`: best default for mixed/polyglot repos.
- `deploy/compose/python.yml`: Python and notebooks.
- `deploy/compose/typescript.yml`: TypeScript-first repositories.
- `deploy/compose/javascript.yml`: JavaScript/TypeScript web repos.
- `deploy/compose/java-kotlin.yml`: Java/Kotlin repos.
- `deploy/compose/csharp.yml`: .NET/C# repositories.
- `deploy/compose/go.yml`: Go repos.

## One-line start (PowerShell)

```powershell
$preset = "python"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

## One-line start (bash)

```bash
preset=python; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d
```

## Parallel stacks for multiple projects

Use unique `-p` values and unique host ports:

```powershell
$env:MCP_PORT="18080"; $env:QDRANT_PORT="16333"; docker compose -p ndlss-project-a -f ndlss-compose.yml up -d
$env:MCP_PORT="28080"; $env:QDRANT_PORT="26333"; docker compose -p ndlss-project-b -f ndlss-compose.yml up -d
```

## Configuration overrides

You can still override any setting at runtime, for example:

```powershell
$env:INDEX_FILE_TYPES=".md,.txt,.py,.sql"
$env:INDEX_EXCLUDE_PATTERNS=".git,node_modules,.venv"
docker compose -f ndlss-compose.yml up -d
```

Image override example:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.1.3"
docker compose -f ndlss-compose.yml up -d
```

## Stop

```powershell
docker compose -f ndlss-compose.yml down
```
