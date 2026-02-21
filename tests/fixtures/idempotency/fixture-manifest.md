# Idempotency Fixture Manifest

## Purpose

Fixture set for validating hash-based deduplication, deterministic chunk IDs,
and stale chunk cleanup behavior.

## Structure

- `baseline/docs/readme.md`: baseline markdown for repeat-run checks.
- `baseline/docs/notes.txt`: text file for deterministic chunk ID checks.
- `changes/edited.txt`: file intended to be modified between runs.
- `changes/deleted.txt`: file intended to be removed between runs.

## Expected Scenarios

- Two identical runs must produce no duplicate records.
- Editing `changes/edited.txt` must update only affected chunks.
- Deleting `changes/deleted.txt` must remove stale chunk records.
