# Release Checklist

## Versioning and metadata

- [ ] Update `VERSION`
- [ ] Update `CHANGELOG.md`
- [ ] Create release tag (`0.2.0` and/or `v0.2.0`)
- [ ] Ensure changelog has a matching section (`## <version> - <date>`)

## Validation

- [ ] Validate compose files (`docker compose config`)
- [ ] Run quality/stability suite
- [ ] Verify examples in [README](../README.md) and [Quickstart](quickstart.md)
- [ ] Validate MCP ingestion creates `workspace_chunks` and `points/count > 0`
- [ ] Validate non-default external `QDRANT_PORT` works with internal `QDRANT_API_PORT=6333`

## Docker Hub publishing

Repository prerequisites:

- [ ] Docker Hub repositories exist:
  - `ndlss-memory-file-indexer`
  - `ndlss-memory-mcp-server`
- [ ] GitHub secrets are configured:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

Release flow:

- [ ] Push release tag
- [ ] Verify workflow `.github/workflows/docker-release.yml` passed
- [ ] Verify images were pushed:
  - `<namespace>/ndlss-memory-file-indexer:<tag>`
  - `<namespace>/ndlss-memory-mcp-server:<tag>`
  - optional `latest`
- [ ] Verify published images include `QDRANT_API_PORT` and `INGESTION_ENABLE_QDRANT_HTTP=1` runtime defaults in compose presets

## Artifacts and docs

- [ ] [README](../README.md) is up to date
- [ ] [CONTRIBUTING](../CONTRIBUTING.md) is up to date
- [ ] [Compose presets](compose-presets.md) lists all presets
- [ ] [Quickstart](quickstart.md) matches current startup flow

## GitHub Release publishing

- [ ] Verify workflow `.github/workflows/github-release.yml` passed
- [ ] Verify Release page contains notes from `CHANGELOG.md`
