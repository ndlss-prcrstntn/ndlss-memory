# US3 Contract: Full Scan Summary Endpoint

## Endpoint

- `GET /v1/indexing/full-scan/jobs/{jobId}/summary`

## Contract Assertions

1. Для завершенной задачи endpoint возвращает `200` и поля:
   - `jobId`
   - `result`
   - `durationSeconds`
   - `totals`
   - `skipBreakdown`
2. Для `running/queued` задачи endpoint возвращает `409`.
3. Для несуществующей задачи endpoint возвращает `404`.
4. Ошибки возвращаются в машиночитаемом формате:
   - `errorCode`
   - `message`
   - `details` (optional)

