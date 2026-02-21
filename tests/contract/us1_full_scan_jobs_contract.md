# US1 Contract: Full Scan Job Start and Progress

## Endpoints

- `POST /v1/indexing/full-scan/jobs`
- `GET /v1/indexing/full-scan/jobs/{jobId}`

## Contract Assertions

1. `POST` returns `202` and payload:
   - `jobId` (string)
   - `status` (`queued|running`)
   - `acceptedAt` (date-time)
2. `GET` returns `200` and payload:
   - `jobId`
   - `status`
   - `processedCount`
   - `indexedCount`
   - `skipCount`
   - `errorCount`
   - `lastEventAt`
3. Unknown job returns `404` with:
   - `errorCode`
   - `message`

