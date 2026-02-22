# Contract: Quality Stage Result

## Scope

Contract validates the shape of stage-level and run-level outputs produced by the quality suite.

## Stage Schema

- [ ] Stage has `stageName` and one of: `unit`, `integration`, `contract`, `e2e`
- [ ] Stage has terminal `status` in: `passed`, `failed`, `skipped`
- [ ] Stage has `startedAt`, `finishedAt`, `durationMs`
- [ ] Failed stage has `failureCode` and `failureMessage`
- [ ] Stage may provide `artifactPaths` list of repository-relative files

## Run Schema

- [ ] Run has `runId`, `startedAt`, `finishedAt`, `status`
- [ ] Run has `stages` array with at least one stage
- [ ] Run `status=failed` when any stage has `status=failed`
- [ ] Run has machine-readable `failures` with `stage`, `code`, `message`

## Traceability

- [ ] `runId` in report matches `runId` logged in stage summaries
- [ ] Artifact files referenced by stage outputs exist on disk
