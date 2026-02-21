# US3: system status contract

## Goal
Validate `/v1/system/status` and `/v1/system/services/{serviceName}` behavior.

## Checks
- Aggregated status includes all required services.
- `overallStatus` is one of `healthy|degraded|down`.
- Unknown service returns `404` with `SERVICE_NOT_FOUND` error code.
