# Regression: Full Scan after Delta-after-commit

## Goal

Ensure full-scan mode keeps behavior after delta implementation.

## Checks

1. Set `INDEX_MODE=full-scan`.
2. Run existing full-scan integration scenarios.
3. Verify counters and error model unchanged.
