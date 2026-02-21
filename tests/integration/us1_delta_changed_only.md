# Integration: US1 Delta Changed-Only

## Goal

Validate that delta-after-commit indexes only changed files (`A`, `M`).

## Execution

Run:

```powershell
pwsh scripts/tests/us1_delta_changed_only.ps1
```

## Expected

- `effectiveMode=delta-after-commit`
- `addedFiles >= 1`
- `modifiedFiles >= 1`
- `indexedFiles >= 1`
