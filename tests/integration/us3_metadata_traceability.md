# US3 Integration: Metadata Traceability

## Goal

Ensure every stored chunk includes required metadata fields and summary reports
metadata coverage.

## Required Metadata

- `path`
- `fileName`
- `fileType`
- `contentHash`
- `timestamp`

## Steps

1. Run ingestion job against fixture workspace.
2. Wait for terminal status.
3. Retrieve summary endpoint output.

## Expected Results

- `metadataCoverage` object contains all required fields.
- Coverage for each required field is between `0` and `1`.
- Successful runs target full coverage (`1.0`) for all fields.
