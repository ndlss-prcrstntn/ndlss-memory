# Regression: Delta-after-commit After Ingestion

## Goal

Ensure delta-after-commit mode still starts and keeps runtime contract intact
after ingestion changes.

## Steps

1. Run stack with `INDEX_MODE=delta-after-commit`.
2. Trigger ingestion job.
3. Query `/v1/system/config` and `/v1/system/status`.

## Expected Results

- Runtime reports `indexMode=delta-after-commit`.
- Ingestion endpoints return valid responses.
- No regression in service health endpoints.
