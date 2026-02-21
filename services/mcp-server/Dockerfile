FROM python:3.12-alpine

RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml

WORKDIR /app

COPY src/system_status_handler.py /app/src/system_status_handler.py
COPY src/full_scan_state.py /app/src/full_scan_state.py
COPY src/full_scan_errors.py /app/src/full_scan_errors.py
COPY src/ingestion_state.py /app/src/ingestion_state.py
COPY src/ingestion_errors.py /app/src/ingestion_errors.py
COPY src/idempotency_state.py /app/src/idempotency_state.py
COPY src/idempotency_errors.py /app/src/idempotency_errors.py
COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY config/security-policy.yaml /app/config/security-policy.yaml
COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml

RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
