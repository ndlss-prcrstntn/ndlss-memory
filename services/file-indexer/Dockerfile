FROM alpine:3.20

RUN apk add --no-cache bash coreutils

WORKDIR /app

COPY scripts/validate-config.sh /app/scripts/validate-config.sh
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
COPY src /app/src

RUN sed -i 's/\r$//' /app/scripts/*.sh
RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
