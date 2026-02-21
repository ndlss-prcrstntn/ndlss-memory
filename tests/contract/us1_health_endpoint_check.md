# US1 health endpoint contract check

## Endpoint
`GET /health`

## Assertions
- HTTP 200
- JSON body contains `status`
- JSON body contains `timestamp`
- `status` equals `ok`
