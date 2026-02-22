# Contract: Quality Stability E2E Stage

## Endpoint/Script Surface

- Script: `scripts/tests/quality_stability_e2e.ps1`
- Artifact: `tests/artifacts/quality-stability/us3-e2e-summary.json`

## Required Output Fields

- [ ] `runId` is present and non-empty
- [ ] `stageName` equals `us3-e2e-quality`
- [ ] `status` equals `passed` on success
- [ ] `generatedAt` is ISO-8601 timestamp
- [ ] `checks.composeUp` is boolean
- [ ] `checks.fullScan` is boolean
- [ ] `checks.deltaAfterCommit` is boolean
- [ ] `checks.semanticSearch` is boolean
- [ ] `checks.repeatRunConsistency` is boolean

## Failure Semantics

- [ ] Script exits non-zero on any failed stage
- [ ] Script always attempts compose teardown in `finally`
