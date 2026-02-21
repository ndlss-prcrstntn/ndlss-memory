# Contract: US2 Delta Summary

## Scope

`GET /v1/indexing/delta-after-commit/jobs/{runId}/summary`

## Assertions

- Summary includes `deletedFiles`, `renamedFiles`, `removedRecords`.
- Summary in running state returns `409 RUN_NOT_FINISHED`.
- `reasonBreakdown` includes machine-readable reason codes.
