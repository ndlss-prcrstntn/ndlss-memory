# Implementation Report: 004-indexing-idempotency

## Scope Delivered

- SHA256 file fingerprinting and change detection
- Deterministic chunk identity generation
- Skip unchanged flow before upsert
- Stale chunk deletion for changed and removed files
- Idempotency run API (`start`, `status`, `summary`) in MCP server

## Validation Artifacts

- Unit tests:
  - `tests/unit/file_indexer/test_file_fingerprint.py`
  - `tests/unit/file_indexer/test_chunk_identity.py`
- Integration scenarios:
  - `tests/integration/us1_idempotent_repeat_run.md`
  - `tests/integration/us2_deterministic_chunk_updates.md`
  - `tests/integration/us3_stale_chunk_cleanup.md`
- Contract scenarios:
  - `tests/contract/idempotency_pipeline_contract_smoke.md`
  - `tests/contract/us3_idempotency_summary_contract.md`

## E2E / Regression Notes

- Compose regression script prepared: `scripts/tests/idempotency_compose_regression.ps1`
- Compose regression executed locally (2026-02-21): PASS
  - US1 repeat-run: PASS (`run1=cdedafda80af4c45a91633c3227e3af9`, `run2=672b29719cb44b9582a31c03b7c54dfa`)
  - US2 deterministic update: PASS (`run1=e8cfa4cfd2bb467dad33af9086a42c35`, `run2=29452656ac804401bcfd7271958183a8`)
  - US3 stale cleanup: PASS (`run2=a62f395410824e90980d756d6d8664a5`)
- Full-scan regression scenario documented: `tests/integration/regression_full_scan_after_idempotency.md`
- Delta-after-commit regression scenario documented: `tests/integration/regression_delta_after_commit_after_idempotency.md`

## Open Items

- Execute compose regression in CI and attach logs.
- Update release metadata (tag/changelog) before publish.
