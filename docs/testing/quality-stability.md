# Quality Stability Suite

## Purpose

This document defines the quality-gate run for feature `008-quality-stability-tests`.

## Stages

1. `unit`: run `pytest` suites for `file_indexer` and `mcp_server`.
2. `integration`: run compose regression scripts for ingestion/indexing flows.
3. `contract`: validate contract markdown and OpenAPI presence/shape.
4. `e2e`: run full end-to-end smoke including repeat-run consistency.

## Entry Points

- Main runner: `scripts/tests/quality_gate_runner.ps1`
- Wrapper: `scripts/tests/run_quality_stability_suite.ps1`
- Contract checker: `scripts/tests/contract_quality_stability.ps1`
- E2E runner: `scripts/tests/quality_stability_e2e.ps1`

## Artifacts

Artifacts are written under `tests/artifacts/quality-stability/`:

- `quality-run-report.json`
- `us1-idempotency-summary.json`
- `us2-integration-summary.json`
- `final-regression-log.md`
- `contract-check-summary.md`

## Exit Criteria

The run is `PASS` only when all enabled stages pass and the report file status is `passed`.
