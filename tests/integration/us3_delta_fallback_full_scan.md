# Integration: US3 Delta Fallback to Full Scan

## Goal

Validate automatic fallback when git diff cannot be computed.

## Execution

Run:

```powershell
pwsh scripts/tests/us3_delta_fallback_full_scan.ps1
```

## Expected

- `effectiveMode=full-scan-fallback`
- `fallbackReasonCode` is present.
