# Regression: Full Scan After Ingestion

## Goal

Verify full-scan endpoints and counters remain functional after ingestion
pipeline integration.

## Steps

1. Start an ingestion run and wait for completion.
2. Start a full-scan run via `POST /v1/indexing/full-scan/jobs`.
3. Poll full-scan progress and request summary.

## Expected Results

- Full-scan run is accepted and completes without API errors.
- Full-scan counters are present and non-negative.
- Ingestion routes remain reachable after full-scan execution.
