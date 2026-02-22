# Release Checklist

## Versioning and metadata

- [ ] Update `VERSION`
- [ ] Update `CHANGELOG.md`
- [ ] Create release tag (`0.1.1` and/or `v0.1.1`)

## Validation

- [ ] Validate compose files (`docker compose config`)
- [ ] Run quality/stability suite
- [ ] Verify examples in `README.md` and `docs/quickstart.md`

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

## Artifacts and docs

- [ ] `README.md` is up to date
- [ ] `CONTRIBUTING.md` is up to date
- [ ] `docs/compose-presets.md` lists all presets
- [ ] `docs/quickstart.md` matches current startup flow
