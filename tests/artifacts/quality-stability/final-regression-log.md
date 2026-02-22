# Quality Stability Run

- startedAt: 2026-02-23T00:43:54.3609522+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 99 items
tests\unit\file_indexer\test_chunk_identity.py ...                       [  3%]
tests\unit\file_indexer\test_chunker.py .....                            [  8%]
tests\unit\file_indexer\test_embedding_retry.py ..                       [ 10%]
tests\unit\file_indexer\test_file_filters.py .....                       [ 15%]
tests\unit\file_indexer\test_file_fingerprint.py .....                   [ 20%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_config.py . [ 21%]
.                                                                        [ 22%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_resilience.py . [ 23%]
.                                                                        [ 24%]
tests\unit\file_indexer\test_git_diff_reader.py ..                       [ 26%]
tests\unit\file_indexer\test_run_limits_selection.py ..                  [ 28%]
tests\unit\mcp_server\test_bootstrap_collection_service.py ..            [ 30%]
tests\unit\mcp_server\test_bootstrap_orchestrator.py ...                 [ 33%]
tests\unit\mcp_server\test_bootstrap_state.py ...                        [ 36%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 38%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 40%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 42%]
tests\unit\mcp_server\test_mcp_tool_adapters_search.py ...               [ 45%]
tests\unit\mcp_server\test_mcp_tool_registry.py ..                       [ 47%]
tests\unit\mcp_server\test_mcp_transport_concurrency.py .                [ 48%]
tests\unit\mcp_server\test_mcp_transport_error_mapper.py ...             [ 51%]
tests\unit\mcp_server\test_mcp_transport_handshake.py ....               [ 55%]
tests\unit\mcp_server\test_mcp_transport_negative_cases.py ...           [ 58%]
tests\unit\mcp_server\test_mcp_transport_protocol_models.py ....         [ 62%]
tests\unit\mcp_server\test_mcp_transport_session_state.py ..             [ 64%]
tests\unit\mcp_server\test_root_commands_endpoint.py ..                  [ 66%]
tests\unit\mcp_server\test_search_repository_missing_collection.py ..... [ 71%]
                                                                         [ 71%]
tests\unit\mcp_server\test_search_result_resolution.py ....              [ 75%]
tests\unit\mcp_server\test_semantic_search_filters.py ..                 [ 77%]
tests\unit\mcp_server\test_semantic_search_service.py ..                 [ 79%]
tests\unit\mcp_server\test_startup_preflight_checks.py ....              [ 83%]
tests\unit\mcp_server\test_startup_preflight_models.py ...               [ 86%]
tests\unit\mcp_server\test_startup_readiness_endpoint.py ..              [ 88%]
tests\unit\mcp_server\test_startup_readiness_summary.py .                [ 89%]
tests\unit\mcp_server\test_vector_upsert_repository_config.py ..         [ 91%]
tests\unit\mcp_server\test_vector_upsert_repository_resilience.py ..     [ 93%]
tests\unit\mcp_server\test_watch_mode_retry_policy.py ...                [ 96%]
tests\unit\mcp_server\test_watch_mode_state.py ...                       [100%]
============================= 99 passed in 0.99s ==============================
[quality] stage 'unit' passed in 1646ms
[quality] stage 'us1' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B 0.0s done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 ...
#5 [auth] library/python:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [auth] library/alpine:pull token for registry-1.docker.io
#6 DONE 0.0s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 1.7s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 1.7s
#8 [file-indexer internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [mcp-server internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#12 [file-indexer internal] load build context
#12 transferring context: 72.94kB 0.0s done
#12 DONE 0.1s
#13 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#13 CACHED
#14 [mcp-server internal] load build context
#14 transferring context: 265.22kB 0.0s done
#14 DONE 0.1s
#15 [file-indexer  3/12] WORKDIR /app
#15 CACHED
#16 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#16 CACHED
#17 [mcp-server  3/17] WORKDIR /app
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 DONE 0.1s
#19 [mcp-server  4/17] COPY src /app/src
#19 DONE 0.2s
#20 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 DONE 0.1s
#21 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#21 DONE 0.1s
#22 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#22 DONE 0.1s
#23 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#23 DONE 0.1s
#24 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#24 DONE 0.1s
#25 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#25 DONE 0.1s
#26 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#26 DONE 0.1s
#27 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#27 DONE 0.1s
#28 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#28 DONE 0.1s
#29 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#29 DONE 0.1s
#30 [file-indexer 10/12] COPY src /app/src
#30 DONE 0.2s
#31 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#31 DONE 0.1s
#32 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 ...
#33 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#33 DONE 0.1s
#34 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#34 DONE 0.1s
#35 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#35 DONE 0.1s
#32 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 DONE 0.5s
#36 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#36 DONE 0.1s
#37 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#37 DONE 2.0s
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 ...
#39 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#39 DONE 1.7s
#40 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#40 ...
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 DONE 3.9s
#40 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#40 DONE 1.7s
#41 [file-indexer] exporting to image
#41 exporting layers
#41 exporting layers 1.5s done
#41 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f
#41 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f 0.3s done
#41 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a
#41 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a 0.2s done
#41 exporting attestation manifest sha256:fb9118760a95fe2e04a787f4b1dd355b8930c857a5011f7dea6c880eb8ebb7e5
#41 exporting attestation manifest sha256:fb9118760a95fe2e04a787f4b1dd355b8930c857a5011f7dea6c880eb8ebb7e5 0.2s done
#41 exporting manifest list sha256:ca5a4705c2fe45a447d759d7eb20b52f81c454dc0caf2efe38a9da2c99cbecf7
#41 exporting manifest list sha256:ca5a4705c2fe45a447d759d7eb20b52f81c454dc0caf2efe38a9da2c99cbecf7 0.0s done
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.4s done
#41 DONE 2.9s
#42 [mcp-server] exporting to image
#42 exporting layers 1.3s done
#42 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd 0.0s done
#42 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d 0.0s done
#42 exporting attestation manifest sha256:93e6abd70d7351cfc522b3392896cf3f8bbeb5ff87a01eebe32d8f981da12a5c 0.1s done
#42 exporting manifest list sha256:002b9748a18338e7076044c7d5bf980075318959f8030ae583c806eae948579c 0.0s done
#42 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#42 unpacking to docker.io/library/ndlss-memory-mcp-server:latest
#42 ...
#43 [file-indexer] resolving provenance for metadata file
#43 DONE 0.0s
#42 [mcp-server] exporting to image
#42 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.7s done
#42 DONE 2.2s
#44 [mcp-server] resolving provenance for metadata file
#44 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   16 seconds ago   Up 9 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     16 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         16 seconds ago   Up 15 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-925bdd2666f64a00a28830d0ff57e8f9 container=/workspace/tests/fixtures/idempotency-runtime-925bdd2666f64a00a28830d0ff57e8f9
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=cad26834fbed4366b013393ca6d714c2
[US1] runId=cad26834fbed4366b013393ca6d714c2 status=running attempt=1/120
[US1] runId=cad26834fbed4366b013393ca6d714c2 status=completed attempt=3/120
[US1] runId=cad26834fbed4366b013393ca6d714c2 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=7508adecbfbe4747b643f463a25ec893
[US1] runId=7508adecbfbe4747b643f463a25ec893 status=running attempt=1/120
[US1] runId=7508adecbfbe4747b643f463a25ec893 status=completed attempt=2/120
[US1] runId=7508adecbfbe4747b643f463a25ec893 finished status=completed
US1 repeat-run completed. run1=cad26834fbed4366b013393ca6d714c2 run2=7508adecbfbe4747b643f463a25ec893 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-a73c58b66add4ade82fb0471849e0dee container=/workspace/tests/fixtures/idempotency-runtime-a73c58b66add4ade82fb0471849e0dee
US2 deterministic update completed. run1=bf793db1792747cf9e95b2c95cfe5069 run2=8c64235b692d4dacbdd1239ad743b5bc
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-598b5dabab2343e78586c739923ba3cf container=/workspace/tests/fixtures/idempotency-runtime-598b5dabab2343e78586c739923ba3cf
US3 stale cleanup completed. run2=fb3fb16b407f49b88048181061927557
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
Idempotency compose regression completed
[quality] stage 'us1' passed in 39542ms
[quality] stage 'us1_persistence' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.6s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.6s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server  4/17] COPY src /app/src
#12 CACHED
#13 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#13 CACHED
#14 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#15 CACHED
#16 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server  3/17] WORKDIR /app
#17 CACHED
#18 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#18 CACHED
#19 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#20 CACHED
#21 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#21 CACHED
#22 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#22 CACHED
#23 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#28 CACHED
#29 [file-indexer  3/12] WORKDIR /app
#29 CACHED
#30 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 CACHED
#33 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#33 CACHED
#34 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#34 CACHED
#35 [file-indexer 10/12] COPY src /app/src
#35 CACHED
#36 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#39 exporting attestation manifest sha256:e91de031d7fcafb44e3ca5b5e10c191bedfde7a5ad56c5223e85d4c46d49c933
#39 exporting attestation manifest sha256:e91de031d7fcafb44e3ca5b5e10c191bedfde7a5ad56c5223e85d4c46d49c933 0.1s done
#39 exporting manifest list sha256:ac8aa57a24fbbaf22ded3eade12f4b2b9a02cdc9e9ebe8ed48fed3a7e144461d 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:9679e68de76a7493192ded97b850189b09e631ac2ed4a4e645be2ca1b76f9549 0.1s done
#40 exporting manifest list sha256:514ff19f4900e698ce2327cf44c1132df39c1a45179ceba31915a39a9ef65054 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US1 ingestion collection creation passed. runId=463241b5a201462a9a0bf47bf3a3d7ac points=15 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'us1_persistence' passed in 25633ms
[quality] stage 'integration' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.3s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server  3/17] WORKDIR /app
#14 CACHED
#15 [mcp-server  4/17] COPY src /app/src
#15 CACHED
#16 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#17 CACHED
#18 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#18 CACHED
#19 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#20 CACHED
#21 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#21 CACHED
#22 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#22 CACHED
#23 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#23 CACHED
#24 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#28 CACHED
#29 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#29 CACHED
#30 [file-indexer 10/12] COPY src /app/src
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#32 CACHED
#33 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer  3/12] WORKDIR /app
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f 0.0s done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#39 exporting attestation manifest sha256:fed1a8c865c6f5df352e6726beaf2d25e14e2dfb7434fe6ab41684a777887e9e 0.1s done
#39 exporting manifest list sha256:aa487570e0cfc56c7cfe6a066ffee94e19aabddc52386360b660198fe41364bf
#39 exporting manifest list sha256:aa487570e0cfc56c7cfe6a066ffee94e19aabddc52386360b660198fe41364bf 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd 0.0s done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:77dc43dead90e47d7823921b8cfaab23aab160f91cc9004c6e74844fced7c571 0.1s done
#40 exporting manifest list sha256:b805e56cefd0a713491e4678151d39bcc4f8390e6beaa6eeacf2211fe4f09438 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Full-scan fixture environment prepared at tests/fixtures/full-scan
US2 full scan filtering check passed
Full-scan fixture environment prepared at tests/fixtures/full-scan
US3 full scan resilience check passed
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.6s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.6s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB 0.0s done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.46kB 0.0s done
#11 DONE 0.0s
#12 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#12 CACHED
#13 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#13 CACHED
#14 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#15 CACHED
#16 [mcp-server  4/17] COPY src /app/src
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#19 CACHED
#20 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#20 CACHED
#21 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#21 CACHED
#22 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#22 CACHED
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  3/17] WORKDIR /app
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#27 CACHED
#28 [file-indexer  3/12] WORKDIR /app
#28 CACHED
#29 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [file-indexer 10/12] COPY src /app/src
#30 CACHED
#31 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#31 CACHED
#32 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#32 CACHED
#33 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#33 CACHED
#34 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#34 CACHED
#35 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#35 CACHED
#36 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#39 exporting attestation manifest sha256:c91c7443b640ab3d630c64609d966df7285b3c9af7c2f488c3be3aaf31e49bc5
#39 exporting attestation manifest sha256:c91c7443b640ab3d630c64609d966df7285b3c9af7c2f488c3be3aaf31e49bc5 0.1s done
#39 exporting manifest list sha256:7a80dcd290319d8f6835b94013db9b639273f8930867e58280e686c4cc81b41b 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.3s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:5112da0606d57961d73d4658b0e6d297277913557a5f887ce9845ea36590b75d 0.1s done
#40 exporting manifest list sha256:78acef11feed953158773031b6207e9fef7a91230d0a05c448f427275b8ec858 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.3s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Container ndlss-memory-qdrant  Running
 Container ndlss-memory-file-indexer  Recreate
 Container ndlss-memory-file-indexer  Recreated
 Container ndlss-memory-mcp-server  Recreate
 Container ndlss-memory-mcp-server  Recreated
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
Full scan compose regression check passed
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB 0.0s done
#2 DONE 0.6s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.8s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 ...
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 1.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 1.1s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.3s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.3s
#8 [file-indexer internal] load build context
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.6s done
#9 DONE 0.8s
#10 [mcp-server internal] load build context
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.5s done
#11 DONE 0.7s
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB done
#8 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#12 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#12 CACHED
#13 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#13 CACHED
#14 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#14 CACHED
#15 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#15 CACHED
#16 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#16 CACHED
#17 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer 10/12] COPY src /app/src
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#26 CACHED
#27 [mcp-server  3/17] WORKDIR /app
#27 CACHED
#28 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#28 CACHED
#29 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server  4/17] COPY src /app/src
#31 CACHED
#32 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#32 CACHED
#33 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#34 CACHED
#35 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#35 CACHED
#36 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#39 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#39 exporting attestation manifest sha256:198d4de93a8bd7ec5bcf47a616f66f5d3e814b31fb08ee5a27ae728f9fa87230
#39 exporting attestation manifest sha256:198d4de93a8bd7ec5bcf47a616f66f5d3e814b31fb08ee5a27ae728f9fa87230 0.1s done
#39 exporting manifest list sha256:146eff24596295e31832dd8afac9e5835c2109631b50eced0a7c0394c7ae229b
#39 exporting manifest list sha256:146eff24596295e31832dd8afac9e5835c2109631b50eced0a7c0394c7ae229b 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#40 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#40 exporting attestation manifest sha256:59a7e27243ff44bd6a2ae21ab5f9f9f14c74cbeef55fc9d07d3c1ea3e056f964 0.1s done
#40 exporting manifest list sha256:7c8bd190f56af69b1078238ad53da46df266582c3823a28762a93c106306e084 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-ee6e8c97e74041a096b6517b521e8599 container=/workspace/tests/fixtures/delta-runtime-ee6e8c97e74041a096b6517b521e8599
US1 delta changed-only completed. run=235d233b67174c32aeb4a164487a496e
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-b29b01dbd16d44c68eb7970a1e8d59eb container=/workspace/tests/fixtures/delta-runtime-b29b01dbd16d44c68eb7970a1e8d59eb
US2 delta delete+rename completed. run=9bb8053dbd574c67b82aba4d29615a73
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-f7175c5ed82d42c9998110d84d147c9f container=/workspace/tests/fixtures/delta-runtime-f7175c5ed82d42c9998110d84d147c9f
US3 delta fallback completed. run=742256ed5b0143f6a082f81048e34af4 reason=BASE_REF_NOT_FOUND
Delta-after-commit compose regression completed
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.3s
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.3s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.46kB done
#11 DONE 0.0s
#12 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#12 CACHED
#13 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#13 CACHED
#14 [file-indexer 10/12] COPY src /app/src
#14 CACHED
#15 [file-indexer  3/12] WORKDIR /app
#15 CACHED
#16 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#16 CACHED
#17 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#19 CACHED
#20 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#25 CACHED
#26 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#26 CACHED
#27 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#27 CACHED
#28 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#28 CACHED
#29 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#29 CACHED
#30 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#30 CACHED
#31 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#32 CACHED
#33 [mcp-server  3/17] WORKDIR /app
#33 CACHED
#34 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#34 CACHED
#35 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#35 CACHED
#36 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [mcp-server  4/17] COPY src /app/src
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#39 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d 0.0s done
#39 exporting attestation manifest sha256:38bf96e76f95601cbbc216ec3779e126bcd492f0a96bf4138169e86bfd71aec2
#39 exporting attestation manifest sha256:38bf96e76f95601cbbc216ec3779e126bcd492f0a96bf4138169e86bfd71aec2 0.1s done
#39 exporting manifest list sha256:dc22d84ada8563a4b00d961444472c6e1e55d2253a42d7a70e344089a1afe3fa 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#40 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#40 exporting attestation manifest sha256:b9c9f8e7a120bef7d514834599885d0678a3b7655ca89e5da23416e6d1a7c723 0.1s done
#40 exporting manifest list sha256:c3247cdefa5ace754d4f26ced6eace7fcba7d5614a185907d7fce474c09315bc 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US1 deterministic chunking scenario finished for runId=593886008c05481aae5efda7349765b3
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US2 retry+upsert scenario finished for runId=615cdadcbd914f55b0ffefdbf01cd233 retryCount=1
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=8fdc7e28c1964d02949ad0d42a778347 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US3 metadata traceability scenario finished for runId=3fe8bb1e696143ec8012537dfb09a810
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
Ingestion compose regression completed
[quality] stage 'integration' passed in 311758ms
[quality] stage 'us2' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [auth] library/python:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/alpine:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 1.0s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 1.1s
#8 [mcp-server internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.1s
#10 [file-indexer internal] load .dockerignore
#10 transferring context: 2B done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.46kB done
#11 DONE 0.0s
#12 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#12 CACHED
#13 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#13 CACHED
#14 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#14 CACHED
#15 [mcp-server  4/17] COPY src /app/src
#15 CACHED
#16 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#17 CACHED
#18 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#18 CACHED
#19 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#19 CACHED
#20 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#20 CACHED
#21 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#21 CACHED
#22 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server  3/17] WORKDIR /app
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#25 CACHED
#26 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#28 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#28 DONE 0.0s
#29 [file-indexer internal] load build context
#29 transferring context: 5.55kB done
#29 DONE 0.0s
#30 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#30 CACHED
#31 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#31 CACHED
#32 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 CACHED
#33 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#33 CACHED
#34 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [file-indexer  3/12] WORKDIR /app
#35 CACHED
#36 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#36 CACHED
#37 [file-indexer 10/12] COPY src /app/src
#37 CACHED
#38 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#38 CACHED
#39 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#39 CACHED
#40 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#40 CACHED
#41 [file-indexer] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#41 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a 0.0s done
#41 exporting attestation manifest sha256:bbc62e166936cc3e79a9e98fdcda145105d3e81f25bed7a0a77cf8e306183b7d
#41 exporting attestation manifest sha256:bbc62e166936cc3e79a9e98fdcda145105d3e81f25bed7a0a77cf8e306183b7d 0.1s done
#41 exporting manifest list sha256:8396fea8f78814cac7348f73eb06dd599bedc90e73c4248e8e76eeaa3d8c79c0 0.0s done
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 DONE 0.2s
#42 [mcp-server] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#42 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#42 exporting attestation manifest sha256:2324d281fa3afce446860a534d442d74c55652ad50b0defa01033047830993f7 0.1s done
#42 exporting manifest list sha256:7d055b4fdd6bece5b9cef7a2a06811efe56470c48be0d05b13e8e0bdc663ee3d 0.0s done
#42 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#42 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#42 DONE 0.2s
#43 [mcp-server] resolving provenance for metadata file
#43 DONE 0.0s
#44 [file-indexer] resolving provenance for metadata file
#44 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 search flow completed. ingestionRunId=f77f19f374a04121950d08497c967e56 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'us2' passed in 23707ms
[quality] stage 'us2_custom_port' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#12 CACHED
#13 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#13 CACHED
#14 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#15 CACHED
#16 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#19 CACHED
#20 [mcp-server  3/17] WORKDIR /app
#20 CACHED
#21 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#21 CACHED
#22 [mcp-server  4/17] COPY src /app/src
#22 CACHED
#23 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#23 CACHED
#24 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#24 CACHED
#25 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/12] COPY src /app/src
#28 CACHED
#29 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  3/12] WORKDIR /app
#31 CACHED
#32 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#32 CACHED
#33 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#34 CACHED
#35 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#36 CACHED
#37 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#39 exporting attestation manifest sha256:2861196a4d6032dbf0967318cf8d740916b587e65e3f197c2ebab6899ac93c38 0.1s done
#39 exporting manifest list sha256:940e690cb2e76e88d50547492c565c79c5d76b72ecb46a540353db7dedd234cb
#39 exporting manifest list sha256:940e690cb2e76e88d50547492c565c79c5d76b72ecb46a540353db7dedd234cb 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d 0.0s done
#40 exporting attestation manifest sha256:1105a571021fba0f3c2e48d10ffdd32617ec19c99662dae857b06f3632d7e1ba 0.1s done
#40 exporting manifest list sha256:21f950873eab1ca611b8b486b14ad6b0b3857481529c619c76a152f067afba43 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.3s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=6e820fa299854ca9af756b5294e42429 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'us2_custom_port' passed in 23366ms
[quality] stage 'startup_preflight' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#12 CACHED
#13 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#13 CACHED
#14 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#18 CACHED
#19 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#19 CACHED
#20 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#20 CACHED
#21 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#21 CACHED
#22 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#22 CACHED
#23 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#23 CACHED
#24 [mcp-server  3/17] WORKDIR /app
#24 CACHED
#25 [mcp-server  4/17] COPY src /app/src
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/12] COPY src /app/src
#28 CACHED
#29 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#29 CACHED
#30 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#30 CACHED
#31 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#31 CACHED
#32 [file-indexer  3/12] WORKDIR /app
#32 CACHED
#33 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#35 CACHED
#36 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#36 CACHED
#37 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a 0.0s done
#39 exporting attestation manifest sha256:ce939ac3fce6f0d1ec97a2a6f29dcc7ba48179f26f32ae43b71f0ee30b874091
#39 exporting attestation manifest sha256:ce939ac3fce6f0d1ec97a2a6f29dcc7ba48179f26f32ae43b71f0ee30b874091 0.1s done
#39 exporting manifest list sha256:5b160d0883284e97958805b2a6e95efd8ead827c502f854177f3cf874c8f35c7 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:a92fa2366690dee731b608f6ccc1c2884a5aa80e78b5ce8a8e141dc331aeea5f 0.1s done
#40 exporting manifest list sha256:6a1885531dbc200de45e9b85a5ab6d551b56fad6ab2d4d84f5b95d1ea3f7d861 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
[startup-preflight-smoke] ready scenario passed
{
    "bootstrap":  {
                      "checkedAt":  "2026-02-22T21:51:14.389498+00:00",
                      "collectionName":  "workspace_chunks",
                      "decision":  "skip-already-completed",
                      "reason":  "bootstrap already completed for workspace",
                      "runId":  "f0fb2b4848f04bd4a41d48cdee75194b",
                      "status":  "ready",
                      "trigger":  "auto-startup",
                      "workspaceKey":  "/workspace|c52ddf65534b7b46"
                  },
    "checkedAt":  "2026-02-22T21:51:14.391291+00:00",
    "collection":  {
                       "checkedAt":  "2026-02-22T21:51:14.389569+00:00",
                       "collectionName":  "workspace_chunks",
                       "exists":  true,
                       "pointCount":  9942
                   },
    "collectionName":  "workspace_chunks",
    "indexMode":  "full-scan",
    "mcpEndpoint":  "/mcp",
    "preflightChecks":  [
                            {
                                "checkId":  "qdrant_reachability",
                                "checkedAt":  "2026-02-22T21:51:14.383584+00:00",
                                "details":  {
                                                "status":  200,
                                                "url":  "http://qdrant:6333/collections"
                                            },
                                "message":  "Qdrant доступен",
                                "severity":  "critical",
                                "status":  "passed"
                            },
                            {
                                "checkId":  "workspace_readable",
                                "checkedAt":  "2026-02-22T21:51:14.386742+00:00",
                                "details":  {
                                                "workspacePath":  "/workspace"
                                            },
                                "message":  "Рабочая директория доступна для чтения",
                                "severity":  "critical",
                                "status":  "passed"
                            },
                            {
                                "checkId":  "git_available",
                                "checkedAt":  "2026-02-22T21:51:14.386759+00:00",
                                "details":  {
                                                "indexMode":  "full-scan"
                                            },
                                "message":  "Проверка git пропущена для текущего index mode",
                                "severity":  "info",
                                "status":  "skipped"
                            }
                        ],
    "serviceReadiness":  {
                             "fileIndexer":  "healthy",
                             "mcpServer":  "healthy",
                             "qdrant":  "healthy"
                         },
    "status":  "ready",
    "workspacePath":  "/workspace"
}
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'startup_preflight' passed in 21772ms
[quality] stage 'startup_bootstrap' started
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-2803be92072241c2a64d1cb22edb90da container=/workspace/tests/fixtures/idempotency-runtime-2803be92072241c2a64d1cb22edb90da
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.3s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.1s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#8 [mcp-server internal] load build context
#8 transferring context: 11.46kB done
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 transferring context: 5.55kB done
#9 DONE 0.0s
#12 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server  3/17] WORKDIR /app
#14 CACHED
#15 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#15 CACHED
#16 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#18 CACHED
#19 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server  4/17] COPY src /app/src
#20 CACHED
#21 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#22 CACHED
#23 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#23 CACHED
#24 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#28 CACHED
#29 [file-indexer  3/12] WORKDIR /app
#29 CACHED
#30 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#30 CACHED
#31 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#31 CACHED
#32 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#32 CACHED
#33 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer 10/12] COPY src /app/src
#36 CACHED
#37 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#39 exporting attestation manifest sha256:f9cd075c6765bfa3cab43cd28a008cc8bfcbd6d8ec6596a59eb207c035d5bd1f
#39 exporting attestation manifest sha256:f9cd075c6765bfa3cab43cd28a008cc8bfcbd6d8ec6596a59eb207c035d5bd1f 0.1s done
#39 exporting manifest list sha256:19d1edd8da5f2783278f72244de353179ff8187cb0c498df33f002f4071c4804 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:e6d5d013132d7078829c9565642b9180c5a26f5b02d15aea52eb05eea1d60793 0.1s done
#40 exporting manifest list sha256:feb571496492b0cdf18a495a8671dc05385468d968d1e42c016599090004d2c7 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
startup bootstrap smoke passed: collection=workspace_chunks points=9942 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\startup-bootstrap-smoke.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'startup_bootstrap' passed in 22539ms
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 93ms
[quality] stage 'mcp_transport' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer internal] load build context
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#12 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#15 CACHED
#16 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#18 CACHED
#19 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#19 CACHED
#20 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#21 CACHED
#22 [mcp-server  3/17] WORKDIR /app
#22 CACHED
#23 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#23 CACHED
#24 [mcp-server  4/17] COPY src /app/src
#24 CACHED
#25 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB done
#8 DONE 0.0s
#28 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#28 CACHED
#29 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#30 CACHED
#31 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#31 CACHED
#32 [file-indexer 10/12] COPY src /app/src
#32 CACHED
#33 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#34 CACHED
#35 [file-indexer  3/12] WORKDIR /app
#35 CACHED
#36 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#36 CACHED
#37 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#39 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a 0.0s done
#39 exporting attestation manifest sha256:617cfd14155f2f87532a8a9db34ea36035996447187c43d57eb76dfa4e7c0ee5
#39 exporting attestation manifest sha256:617cfd14155f2f87532a8a9db34ea36035996447187c43d57eb76dfa4e7c0ee5 0.1s done
#39 exporting manifest list sha256:d8d9aa06b93c444e5766882804c58e00880893bb981537a11cd1a0b3edf9ad69 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#40 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#40 exporting attestation manifest sha256:c39a6b5a511fced41d2dba7d537516a9459f7fc6c44b5accf7495af6d821efbb 0.1s done
#40 exporting manifest list sha256:6546b8a32a399aa773444bffa8ef39a01075d9998ab56416db37fda5a23dcb06 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-mcp-server  Built
 ndlss-memory-file-indexer  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
MCP transport smoke completed. artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\mcp-transport-smoke.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
[quality] stage 'mcp_transport' passed in 21773ms
[quality] stage 'us3' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B 0.0s done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#13 CACHED
#14 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#14 CACHED
#15 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#15 CACHED
#16 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#16 CACHED
#17 [mcp-server  4/17] COPY src /app/src
#17 CACHED
#18 [mcp-server  3/17] WORKDIR /app
#18 CACHED
#19 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#21 CACHED
#22 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#22 CACHED
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#25 CACHED
#26 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#26 CACHED
#27 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#27 CACHED
#28 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#32 CACHED
#33 [file-indexer 10/12] COPY src /app/src
#33 CACHED
#34 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer  3/12] WORKDIR /app
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#39 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d 0.0s done
#39 exporting attestation manifest sha256:258f61b4b256efe58ef6166fefe5294a7a0c771ea2dadbb4c83cc7d879565aad
#39 exporting attestation manifest sha256:258f61b4b256efe58ef6166fefe5294a7a0c771ea2dadbb4c83cc7d879565aad 0.1s done
#39 exporting manifest list sha256:35b721187b80da6a077ff4c835fb48226c629aa5deab0bc66043ad7442f486ef
#39 exporting manifest list sha256:35b721187b80da6a077ff4c835fb48226c629aa5deab0bc66043ad7442f486ef 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#40 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#40 exporting attestation manifest sha256:74725b664a33b7d9af9b69cacf88a1d746324fd9d0ccb0f59022642fdae7f814 0.1s done
#40 exporting manifest list sha256:b325bfa213ed1ced388f61c5b47ff0d4cf5aef15bc5e9d77a725aef5e7dc5004 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-9d724e94898449678e14f5d0db268389 container=/workspace/tests/fixtures/delta-runtime-9d724e94898449678e14f5d0db268389
US1 delta changed-only completed. run=7661fb46944b430280775c23cb61c400
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=c061f6f97e7d4a42a1be6f6da48b770f results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US1 ingestion collection creation passed. runId=bb353f6ade6448c7b5b841003053c5db points=15 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-f769a8e1bde643618756fab78e62b68c container=/workspace/tests/fixtures/idempotency-runtime-f769a8e1bde643618756fab78e62b68c
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=5096f714f0d944649c34507f070dc699
[US1] runId=5096f714f0d944649c34507f070dc699 status=running attempt=1/120
[US1] runId=5096f714f0d944649c34507f070dc699 status=completed attempt=2/120
[US1] runId=5096f714f0d944649c34507f070dc699 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=fa7e22c5c53e448f87a8ea37811f657b
[US1] runId=fa7e22c5c53e448f87a8ea37811f657b status=running attempt=1/120
[US1] runId=fa7e22c5c53e448f87a8ea37811f657b status=completed attempt=2/120
[US1] runId=fa7e22c5c53e448f87a8ea37811f657b finished status=completed
US1 repeat-run completed. run1=5096f714f0d944649c34507f070dc699 run2=fa7e22c5c53e448f87a8ea37811f657b artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-ac94fecfb8ca45fea696acc3853183bd container=/workspace/tests/fixtures/idempotency-runtime-ac94fecfb8ca45fea696acc3853183bd
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=47e385a42a8d497daed0a699f511202b
[US1] runId=47e385a42a8d497daed0a699f511202b status=running attempt=1/120
[US1] runId=47e385a42a8d497daed0a699f511202b status=completed attempt=2/120
[US1] runId=47e385a42a8d497daed0a699f511202b finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=be0eb32fa0b3496d9e2359572bdc1c76
[US1] runId=be0eb32fa0b3496d9e2359572bdc1c76 status=running attempt=1/120
[US1] runId=be0eb32fa0b3496d9e2359572bdc1c76 status=completed attempt=2/120
[US1] runId=be0eb32fa0b3496d9e2359572bdc1c76 finished status=completed
US1 repeat-run completed. run1=47e385a42a8d497daed0a699f511202b run2=be0eb32fa0b3496d9e2359572bdc1c76 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer internal] load build context
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.1s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.1s done
#11 DONE 0.1s
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB done
#8 DONE 0.0s
#12 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#12 CACHED
#13 [mcp-server  4/17] COPY src /app/src
#13 CACHED
#14 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#14 CACHED
#15 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#15 CACHED
#16 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#18 CACHED
#19 [mcp-server  3/17] WORKDIR /app
#19 CACHED
#20 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#20 CACHED
#21 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#22 CACHED
#23 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#23 CACHED
#24 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#26 CACHED
#27 [file-indexer  3/12] WORKDIR /app
#27 CACHED
#28 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#28 CACHED
#29 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#29 CACHED
#30 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#30 CACHED
#31 [file-indexer 10/12] COPY src /app/src
#31 CACHED
#32 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#32 CACHED
#33 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#34 CACHED
#35 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#35 CACHED
#36 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:a0c870bc75f535f1cf395151be4fa416b71832450a7b40cc5e1ea2962844b7bd done
#39 exporting config sha256:8d8ba60fa8b78aee7f1179cff38faea29df4918aa09c360969cdc8023cce5d1d done
#39 exporting attestation manifest sha256:fe4010c007b72a49fa842153dfb85cafbc5fef76dcadd68eacc8eed88fdf412f
#39 exporting attestation manifest sha256:fe4010c007b72a49fa842153dfb85cafbc5fef76dcadd68eacc8eed88fdf412f 0.1s done
#39 exporting manifest list sha256:da8b02f67cc0bc26fee018afa224453b0f0bd2b42266557056c8d948d05e1187
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:8b0d8fd9b46dc394c733f874325d6cfe6eb4e0a12b00b64ca6287ea227622c0f done
#40 exporting config sha256:333fea04de89262fc5dc51dda1145f4b713d8760523de02dd106d5139f031d6a done
#40 exporting attestation manifest sha256:649e8919aa541082f19b5e954fd303d4666ad83b45bda662baecb1e8757bea17 0.1s done
#40 exporting manifest list sha256:f4b631bde6febd8d88696c7817d1e885ea4ceb5a10cda23cd8d5c00c16278142 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.3s
#39 [mcp-server] exporting to image
#39 exporting manifest list sha256:da8b02f67cc0bc26fee018afa224453b0f0bd2b42266557056c8d948d05e1187 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#41 [file-indexer] resolving provenance for metadata file
#41 DONE 0.0s
#42 [mcp-server] resolving provenance for metadata file
#42 DONE 0.0s
 ndlss-memory-file-indexer  Built
 ndlss-memory-mcp-server  Built
 Network ndlss_net  Creating
 Network ndlss_net  Created
 Container ndlss-memory-qdrant  Creating
 Container ndlss-memory-qdrant  Created
 Container ndlss-memory-file-indexer  Creating
 Container ndlss-memory-file-indexer  Created
 Container ndlss-memory-mcp-server  Creating
 Container ndlss-memory-mcp-server  Created
 Container ndlss-memory-qdrant  Starting
 Container ndlss-memory-qdrant  Started
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Starting
 Container ndlss-memory-file-indexer  Started
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=8f0822f715284aea8866d9e297844997 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
 Container ndlss-memory-mcp-server  Stopping
 Container ndlss-memory-mcp-server  Stopped
 Container ndlss-memory-mcp-server  Removing
 Container ndlss-memory-mcp-server  Removed
 Container ndlss-memory-file-indexer  Stopping
 Container ndlss-memory-file-indexer  Stopped
 Container ndlss-memory-file-indexer  Removing
 Container ndlss-memory-file-indexer  Removed
 Container ndlss-memory-qdrant  Stopping
 Container ndlss-memory-qdrant  Stopped
 Container ndlss-memory-qdrant  Removing
 Container ndlss-memory-qdrant  Removed
 Network ndlss_net  Removing
 Network ndlss_net  Removed
US3 E2E quality scenario passed. artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us3-e2e-summary.json
[quality] stage 'us3' passed in 54248ms
Quality run passed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-23T00:53:00.7256390+03:00
- exitCode: 0
