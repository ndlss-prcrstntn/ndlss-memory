# Implementation Report: 005-delta-after-commit

## Scope Delivered

- Git-based delta change detection using `git diff --name-status --find-renames`.
- Processing only changed inputs (`added`, `modified`) in delta runs.
- Deletion and rename synchronization (`remove old` + `index new`).
- Automatic fallback to `full-scan-fallback` mode when git diff fails.
- MCP API for delta runs (`start`, `status`, `summary`).

## Validation Artifacts

- Unit tests:
  - `tests/unit/file_indexer/test_git_diff_reader.py`
- Contract scenarios:
  - `tests/contract/delta_after_commit_contract_smoke.md`
  - `tests/contract/us1_delta_jobs_contract.md`
  - `tests/contract/us2_delta_summary_contract.md`
  - `tests/contract/us3_delta_fallback_contract.md`
- Integration scenarios:
  - `tests/integration/us1_delta_changed_only.md`
  - `tests/integration/us2_delta_delete_rename.md`
  - `tests/integration/us3_delta_fallback_full_scan.md`
  - `tests/integration/regression_full_scan_after_delta_after_commit.md`
  - `tests/integration/regression_idempotency_after_delta_after_commit.md`

## E2E / Regression Notes

- Compose regression script: `scripts/tests/delta_after_commit_compose_regression.ps1`
- Compose regression executed locally (2026-02-21): PASS
  - US1 changed-only: PASS (`run=4740dd6074854474a418d392b1548127`)
  - US2 delete+rename: PASS (`run=0e10640eed1f40d7bde6dc5ae07196a4`)
  - US3 fallback: PASS (`run=47904224230a4d1fb84072cf605f8d25`, `fallbackReasonCode=BASE_REF_NOT_FOUND`)
- Runtime API contract synced to `services/mcp-server/openapi/delta-after-commit-indexing.openapi.yaml`
- Feature contract maintained in `specs/005-delta-after-commit/contracts/delta-after-commit-indexing.openapi.yaml`

## Open Items

- Execute compose regression in CI and attach logs to release artifacts.
- Add semantic-search regression once search tools are implemented.
