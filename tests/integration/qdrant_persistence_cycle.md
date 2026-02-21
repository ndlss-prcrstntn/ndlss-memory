# Qdrant persistence cycle test

## Goal
Confirm Qdrant data volume survives restart cycle.

## Steps
1. Start stack.
2. Insert a test marker record in Qdrant.
3. Stop stack with `docker compose down`.
4. Start stack again.
5. Verify marker record still exists.

## Expected
Data is preserved in named volume `ndlss_memory_qdrant_data`.

