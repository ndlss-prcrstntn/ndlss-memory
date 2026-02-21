# Integration: US2 Delta Delete+Rename

## Goal

Validate stale-record cleanup for deleted and renamed files.

## Execution

Run:

```powershell
pwsh scripts/tests/us2_delta_delete_rename.ps1
```

## Expected

- `deletedFiles >= 1`
- `renamedFiles >= 1`
- `removedRecords >= 1`
