# Compose observability contract test

## Goal
Validate runtime contract alignment with `compose-observability.openapi.yaml`.

## Contract checks
- `GET /health` returns status and timestamp.
- `GET /v1/system/status` returns overall status and per-service states.
- `GET /v1/system/config` returns effective runtime config.
- `GET /v1/system/services/{serviceName}` returns 404 for unknown service.
