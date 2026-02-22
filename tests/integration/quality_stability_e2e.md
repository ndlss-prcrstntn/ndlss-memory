# Integration: Quality Stability E2E

## Goal

Validate end-to-end flow in a single run:

1. `docker compose up`
2. `full-scan` run
3. `delta-after-commit` run
4. `semantic search` query and result resolution
5. repeat-run consistency check

## Steps

1. Execute `scripts/tests/quality_stability_e2e.ps1`.
2. Verify script exits with code 0.
3. Verify artifact file `tests/artifacts/quality-stability/us3-e2e-summary.json` exists.
4. Verify all flags under `checks` are `true`.

## Expected

- No stage returns fatal error.
- The suite writes machine-readable artifact for the run.
- Repeat-run consistency check does not regress (`failedChunks` does not increase).
