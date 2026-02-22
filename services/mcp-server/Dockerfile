FROM python:3.12-alpine

RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml

WORKDIR /app

COPY src /app/src
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY config/security-policy.yaml /app/config/security-policy.yaml
COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml

RUN sed -i 's/\r$//' /app/scripts/*.sh
RUN chmod +x /app/scripts/entrypoint.sh
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
