# Contract: US1 Delta Jobs

## Scope

`POST /v1/indexing/delta-after-commit/jobs` and `GET /v1/indexing/delta-after-commit/jobs/{runId}`.

## Assertions

- Start endpoint returns `202` and `requestedMode=delta-after-commit`.
- Status endpoint returns counters:
  - `addedFiles`
  - `modifiedFiles`
  - `indexedFiles`
  - `skippedFiles`
- Unknown run returns `404 RUN_NOT_FOUND`.
