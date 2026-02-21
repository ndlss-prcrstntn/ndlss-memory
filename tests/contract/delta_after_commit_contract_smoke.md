# Contract Smoke: Delta-after-commit API

## Goal

Validate basic availability and payload shape for delta-after-commit endpoints.

## Steps

1. `POST /v1/indexing/delta-after-commit/jobs` with valid `workspacePath`.
2. Verify `202` with `runId`, `status`, `acceptedAt`, `requestedMode`.
3. `GET /v1/indexing/delta-after-commit/jobs/{runId}` until terminal status.
4. `GET /v1/indexing/delta-after-commit/jobs/{runId}/summary`.

## Expected

- Error model follows `{errorCode,message,details?}`.
- Status contains counters and `effectiveMode`.
- Summary contains `reasonBreakdown` and fallback fields when applicable.
