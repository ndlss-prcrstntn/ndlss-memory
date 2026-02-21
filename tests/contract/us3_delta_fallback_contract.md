# Contract: US3 Delta Fallback

## Scope

Fallback-related fields for delta-after-commit run.

## Assertions

- On git diff failure, status/summary include:
  - `effectiveMode=full-scan-fallback`
  - `fallbackReasonCode`
- Summary remains machine-readable and includes `reasonBreakdown`.
