FROM alpine:3.20

RUN apk add --no-cache bash coreutils

WORKDIR /app

COPY scripts/validate-config.sh /app/scripts/validate-config.sh
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json

RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
