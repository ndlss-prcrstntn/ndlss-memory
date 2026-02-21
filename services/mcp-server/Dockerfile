FROM python:3.12-alpine

RUN apk add --no-cache curl && pip install --no-cache-dir flask pyyaml

WORKDIR /app

COPY src/system_status_handler.py /app/src/system_status_handler.py
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY config/security-policy.yaml /app/config/security-policy.yaml
COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml

RUN chmod +x /app/scripts/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
