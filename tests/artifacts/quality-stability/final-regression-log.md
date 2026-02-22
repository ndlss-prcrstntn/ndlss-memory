# Quality Stability Run

- startedAt: 2026-02-22T22:31:50.1550397+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 97 items
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
tests\unit\mcp_server\test_bootstrap_collection_service.py ..            [ 28%]
tests\unit\mcp_server\test_bootstrap_orchestrator.py ...                 [ 31%]
tests\unit\mcp_server\test_bootstrap_state.py ...                        [ 35%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 37%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 39%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 41%]
tests\unit\mcp_server\test_mcp_tool_adapters_search.py ...               [ 44%]
tests\unit\mcp_server\test_mcp_tool_registry.py ..                       [ 46%]
tests\unit\mcp_server\test_mcp_transport_concurrency.py .                [ 47%]
tests\unit\mcp_server\test_mcp_transport_error_mapper.py ...             [ 50%]
tests\unit\mcp_server\test_mcp_transport_handshake.py ....               [ 54%]
tests\unit\mcp_server\test_mcp_transport_negative_cases.py ...           [ 57%]
tests\unit\mcp_server\test_mcp_transport_protocol_models.py ....         [ 61%]
tests\unit\mcp_server\test_mcp_transport_session_state.py ..             [ 63%]
tests\unit\mcp_server\test_root_commands_endpoint.py ..                  [ 65%]
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
============================= 97 passed in 1.19s ==============================
[quality] stage 'unit' passed in 2173ms
[quality] stage 'us1' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [auth] library/python:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/alpine:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#6 DONE 1.0s
#7 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#7 DONE 1.0s
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
#12 transferring context: 5.55kB done
#12 DONE 0.0s
#13 [mcp-server internal] load build context
#13 transferring context: 11.34kB done
#13 DONE 0.0s
#14 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#14 CACHED
#15 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#15 CACHED
#16 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#16 CACHED
#17 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#17 CACHED
#18 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#18 CACHED
#19 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#19 CACHED
#20 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#21 CACHED
#22 [file-indexer  3/12] WORKDIR /app
#22 CACHED
#23 [file-indexer 10/12] COPY src /app/src
#23 CACHED
#24 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server  4/17] COPY src /app/src
#28 CACHED
#29 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#29 CACHED
#30 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#30 CACHED
#31 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#31 CACHED
#32 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#32 CACHED
#33 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#34 CACHED
#35 [mcp-server  3/17] WORKDIR /app
#35 CACHED
#36 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#37 CACHED
#38 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#38 CACHED
#39 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#39 CACHED
#40 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#40 CACHED
#41 [file-indexer] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#41 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#41 exporting attestation manifest sha256:24dbf33a8b9a7b0418fe9593256a825955ae37069794590768533f1542c2b58b 0.1s done
#41 exporting manifest list sha256:41c7c5cc0d5f5e180366c04cc51ec6865da3d590f162b1b95c536756a8437fe0
#41 exporting manifest list sha256:41c7c5cc0d5f5e180366c04cc51ec6865da3d590f162b1b95c536756a8437fe0 0.0s done
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 DONE 0.2s
#42 [mcp-server] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#42 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#42 exporting attestation manifest sha256:4998b7c287c58f2b77e8c78eb8801a4606c4dacbc316da57f6304ec66a876410 0.1s done
#42 exporting manifest list sha256:ebf48f7e6bd73a54e3c0a80940e45129b59616bbfb66f8e232a8d2e34cd63f7e 0.0s done
#42 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#42 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#42 DONE 0.2s
#43 [file-indexer] resolving provenance for metadata file
#43 DONE 0.0s
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
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-b03db4345ff04b5185179be1fc4aa45c container=/workspace/tests/fixtures/idempotency-runtime-b03db4345ff04b5185179be1fc4aa45c
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=c637ea796d5b41799b8ada877ebf58c9
[US1] runId=c637ea796d5b41799b8ada877ebf58c9 status=running attempt=1/120
[US1] runId=c637ea796d5b41799b8ada877ebf58c9 status=completed attempt=2/120
[US1] runId=c637ea796d5b41799b8ada877ebf58c9 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=b0cdfc60f0464030b1b30da0b6ae1792
[US1] runId=b0cdfc60f0464030b1b30da0b6ae1792 status=running attempt=1/120
[US1] runId=b0cdfc60f0464030b1b30da0b6ae1792 status=completed attempt=2/120
[US1] runId=b0cdfc60f0464030b1b30da0b6ae1792 finished status=completed
US1 repeat-run completed. run1=c637ea796d5b41799b8ada877ebf58c9 run2=b0cdfc60f0464030b1b30da0b6ae1792 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-208f6d1983a74382a4430727aaaba8b0 container=/workspace/tests/fixtures/idempotency-runtime-208f6d1983a74382a4430727aaaba8b0
US2 deterministic update completed. run1=087a98d6e6ec476595d9f1d32689b530 run2=6800dd775de74060b4feca481931be6f
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-012bf2a287f9462c92827ca9f404c903 container=/workspace/tests/fixtures/idempotency-runtime-012bf2a287f9462c92827ca9f404c903
US3 stale cleanup completed. run2=3cd869ae19e64fa1a9d3d0aff09b4f0f
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
[quality] stage 'us1' passed in 27013ms
[quality] stage 'us1_persistence' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB done
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
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#12 CACHED
#13 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#13 CACHED
#14 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#14 CACHED
#15 [file-indexer  3/12] WORKDIR /app
#15 CACHED
#16 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#16 CACHED
#17 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [file-indexer 10/12] COPY src /app/src
#20 CACHED
#21 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#8 [mcp-server internal] load build context
#8 transferring context: 11.34kB done
#8 DONE 0.0s
#23 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#25 CACHED
#26 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#26 CACHED
#27 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#28 CACHED
#29 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#30 CACHED
#31 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#31 CACHED
#32 [mcp-server  3/17] WORKDIR /app
#32 CACHED
#33 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#33 CACHED
#34 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#34 CACHED
#35 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server  4/17] COPY src /app/src
#36 CACHED
#37 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#39 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#39 exporting attestation manifest sha256:93b82614b6c0c8e4a2c6257cfeddb9bcf937103f7ffe4d59454cfac3f4ef71e8 0.1s done
#39 exporting manifest list sha256:e2e1185562b084106c44251f888723a1db1945aac171f1ec76f69da2de5da604
#39 exporting manifest list sha256:e2e1185562b084106c44251f888723a1db1945aac171f1ec76f69da2de5da604 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#40 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea done
#40 exporting attestation manifest sha256:f5970601de30241dccc21a72884c2ff3b8f09e906d058c50623898536c15a48f 0.1s done
#40 exporting manifest list sha256:a9b9e4597951724ee74b2150ba1750f9cc96d99c7c5fbb3d5ff84a08ed858d11
#40 exporting manifest list sha256:a9b9e4597951724ee74b2150ba1750f9cc96d99c7c5fbb3d5ff84a08ed858d11 0.0s done
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
US1 ingestion collection creation passed. runId=f86a2cef01e44989868111adedd07143 points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
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
[quality] stage 'us1_persistence' passed in 23506ms
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
#11 transferring context: 11.34kB done
#11 DONE 0.0s
#12 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#12 CACHED
#13 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#13 CACHED
#14 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  3/12] WORKDIR /app
#16 CACHED
#17 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#19 CACHED
#20 [file-indexer 10/12] COPY src /app/src
#20 CACHED
#21 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#23 CACHED
#24 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#24 CACHED
#25 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#26 CACHED
#27 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#28 CACHED
#29 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#32 CACHED
#33 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [mcp-server  4/17] COPY src /app/src
#34 CACHED
#35 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#35 CACHED
#36 [mcp-server  3/17] WORKDIR /app
#36 CACHED
#37 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea done
#39 exporting attestation manifest sha256:a64916caf610cdf12e900d9b8a1c882e0628ffdda9dd79bfc92312d54a34b8be 0.1s done
#39 exporting manifest list sha256:edf2dae1e0c49167c3158b72759b95b55aee2df55a0d1272d8a85a5d5bc8c72f
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:4ef5001e4f5b0ba493d3e803d7104423384172b3e2d45f84f09eccbd6b07de36 0.1s done
#40 exporting manifest list sha256:7fc491d3afaf7107823a2ba3f0f33c5257db01df37156c5b6efc8f6a71eaa12c 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting manifest list sha256:edf2dae1e0c49167c3158b72759b95b55aee2df55a0d1272d8a85a5d5bc8c72f 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
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
#4 DONE 0.6s
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.7s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.1s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#12 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#12 CACHED
#13 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#13 CACHED
#14 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#14 CACHED
#15 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#15 CACHED
#16 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#16 CACHED
#17 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#18 CACHED
#19 [file-indexer 10/12] COPY src /app/src
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#8 [mcp-server internal] load build context
#8 transferring context: 11.34kB done
#8 DONE 0.0s
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#25 CACHED
#26 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#26 CACHED
#27 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server  4/17] COPY src /app/src
#28 CACHED
#29 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#29 CACHED
#30 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#30 CACHED
#31 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server  3/17] WORKDIR /app
#33 CACHED
#34 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#35 CACHED
#36 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:2e7781d2a0f2f6241a4d8f4a76d52f7e93da80dd3c0b4155c85176614fa7eb87 0.0s done
#40 exporting manifest list sha256:e3d9dbaa85c118c73344f60bf872e5f15759e664d1323ae4b328c72e8ccf420c 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting attestation manifest sha256:277d4da79c7e43653a3a46a9bb299d8706ef0f5bbc78c3abb18922008d5d41c5 0.1s done
#39 exporting manifest list sha256:63a5bfc9b9636146a03b4dedec526a0afe9c91cf6b64d8ebfd0193ed22af1ccb
#39 exporting manifest list sha256:63a5bfc9b9636146a03b4dedec526a0afe9c91cf6b64d8ebfd0193ed22af1ccb 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
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
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 800B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.6s
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.6s
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
#11 transferring context: 11.34kB done
#11 DONE 0.0s
#12 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#12 CACHED
#13 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#13 CACHED
#14 [file-indexer  3/12] WORKDIR /app
#14 CACHED
#15 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#15 CACHED
#16 [file-indexer 10/12] COPY src /app/src
#16 CACHED
#17 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#18 CACHED
#19 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#19 CACHED
#20 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#20 CACHED
#21 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#24 CACHED
#25 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server  4/17] COPY src /app/src
#26 CACHED
#27 [mcp-server  3/17] WORKDIR /app
#27 CACHED
#28 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#28 CACHED
#29 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#30 CACHED
#31 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#32 CACHED
#33 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#33 CACHED
#34 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#34 CACHED
#35 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#35 CACHED
#36 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#39 exporting attestation manifest sha256:e402e6826957771df0d2ba6c0eca4b4fa3b77b6a0716eedc6d9d05323e3ea68f
#39 exporting attestation manifest sha256:e402e6826957771df0d2ba6c0eca4b4fa3b77b6a0716eedc6d9d05323e3ea68f 0.1s done
#39 exporting manifest list sha256:831fd628a867f5352db1f8b626b01a6b08f2a74a3dc79d43a53985293e519d62
#39 exporting manifest list sha256:831fd628a867f5352db1f8b626b01a6b08f2a74a3dc79d43a53985293e519d62 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:e1fc59bd5eb74d9eb1ecad0c74deafa7b5a1386e073b5e6079f01399bcf40cfc 0.1s done
#40 exporting manifest list sha256:3696631683d74369639551c61e5aaf72ba444314d2192b4e78522798da3986f3 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
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
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 9 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 15 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-fd9e31283c62451ba7682eead0d12a50 container=/workspace/tests/fixtures/delta-runtime-fd9e31283c62451ba7682eead0d12a50
US1 delta changed-only completed. run=88b673b1f4394de2b1f62f9b98779a8f
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-3934b214bfcf40a69e64c7b6a543bceb container=/workspace/tests/fixtures/delta-runtime-3934b214bfcf40a69e64c7b6a543bceb
US2 delta delete+rename completed. run=e867786bd7384736b4b386057798b637
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-4d8a7f4c06d94373bc2a190723e62854 container=/workspace/tests/fixtures/delta-runtime-4d8a7f4c06d94373bc2a190723e62854
US3 delta fallback completed. run=71f4376c622b49b6995b6a710fecd54a reason=BASE_REF_NOT_FOUND
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
#10 transferring context: 11.34kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#13 CACHED
#14 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#15 CACHED
#16 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#16 CACHED
#17 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#17 CACHED
#18 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#22 CACHED
#23 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#23 CACHED
#24 [mcp-server  3/17] WORKDIR /app
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server  4/17] COPY src /app/src
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
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
#34 [file-indexer 10/12] COPY src /app/src
#34 CACHED
#35 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#36 CACHED
#37 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#39 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#39 exporting attestation manifest sha256:be6da5eb24a7be1c51dc6664996fe481b97995e6a79e5de15c9be72c5a171567
#39 exporting attestation manifest sha256:be6da5eb24a7be1c51dc6664996fe481b97995e6a79e5de15c9be72c5a171567 0.1s done
#39 exporting manifest list sha256:5b214803eb4168f80d177babc1c40e9e88b399ad35d779298a59570fcd83e03a
#39 exporting manifest list sha256:5b214803eb4168f80d177babc1c40e9e88b399ad35d779298a59570fcd83e03a 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#40 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea done
#40 exporting attestation manifest sha256:a0f22bc939eb45c735ca55dbf7f1cc8419721bdf0e1f14798a969429d6c8489b 0.1s done
#40 exporting manifest list sha256:eadfefdd9d645155573e80c95428cd215eeb9709c69dfab2458fc87157b26d3e 0.0s done
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   14 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         14 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US1 deterministic chunking scenario finished for runId=5b2a45e5254540789447c8409b68621c
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US2 retry+upsert scenario finished for runId=fcf10114aaed4cec9c30a14425b1dbed retryCount=1
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=25681a6f34ff41d5afb0854dc2eb3b97 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US3 metadata traceability scenario finished for runId=4dbc4da93d01496e94008b8682eeaf7d
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
[quality] stage 'integration' passed in 303993ms
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
#6 ...
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 1.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 1.0s
#8 [file-indexer internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [mcp-server internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#12 [file-indexer internal] load build context
#12 transferring context: 5.55kB done
#12 DONE 0.0s
#13 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#13 CACHED
#14 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#14 CACHED
#15 [file-indexer 10/12] COPY src /app/src
#15 CACHED
#16 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#16 CACHED
#17 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#17 CACHED
#18 [file-indexer  3/12] WORKDIR /app
#18 CACHED
#19 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#19 CACHED
#20 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#21 CACHED
#22 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#22 CACHED
#23 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#23 CACHED
#24 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#24 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#24 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#24 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.34kB 0.0s done
#10 DONE 0.0s
#25 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#26 CACHED
#27 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#27 CACHED
#28 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#28 CACHED
#29 [mcp-server  4/17] COPY src /app/src
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#31 CACHED
#32 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#32 CACHED
#33 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#33 CACHED
#34 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#34 CACHED
#35 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#35 CACHED
#36 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#37 CACHED
#38 [mcp-server  3/17] WORKDIR /app
#38 CACHED
#39 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#39 CACHED
#40 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#40 CACHED
#41 [mcp-server] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#41 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#41 ...
#42 [file-indexer] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#42 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#42 exporting attestation manifest sha256:81b678cf428f544bcd495a440f676be0a8b9ead728f78e02f3d289b8b5c240ca 0.1s done
#42 exporting manifest list sha256:ea21fcaa9935d8e91ac89c249d7ea7c833c699cf04856e2ea3cc45ba81cad753 0.0s done
#42 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#42 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#42 DONE 0.2s
#41 [mcp-server] exporting to image
#41 exporting attestation manifest sha256:63d6568e95a145696c182394e6db3c3b60a8a451adbdedd1e15d4bf8111aa645
#41 exporting attestation manifest sha256:63d6568e95a145696c182394e6db3c3b60a8a451adbdedd1e15d4bf8111aa645 0.1s done
#41 exporting manifest list sha256:42179cc3d0e4decc44835169095eed1198e3c7aaff0204c97512005564311f7a 0.0s done
#41 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#41 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#41 DONE 0.2s
#43 [file-indexer] resolving provenance for metadata file
#43 DONE 0.0s
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 search flow completed. ingestionRunId=7d2ec595c5d24e41afa0e1e267e0fef4 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
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
[quality] stage 'us2' passed in 23256ms
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
#10 transferring context: 11.34kB 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#13 CACHED
#14 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#14 CACHED
#15 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#15 CACHED
#16 [mcp-server  3/17] WORKDIR /app
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [mcp-server  4/17] COPY src /app/src
#19 CACHED
#20 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#20 CACHED
#21 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#21 CACHED
#22 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#22 CACHED
#23 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/12] COPY src /app/src
#28 CACHED
#29 [file-indexer  3/12] WORKDIR /app
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#31 CACHED
#32 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#32 CACHED
#33 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#33 CACHED
#34 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#34 CACHED
#35 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#39 exporting attestation manifest sha256:db8c90b823815ed2b5408063c365746c899bfe58a97a1c3cd8bdbc6ed66ab1d6
#39 exporting attestation manifest sha256:db8c90b823815ed2b5408063c365746c899bfe58a97a1c3cd8bdbc6ed66ab1d6 0.1s done
#39 exporting manifest list sha256:22f319592ad2c538efede0f4fc32e6642badf8224c96556d7f5d1688f1abd435
#39 exporting manifest list sha256:22f319592ad2c538efede0f4fc32e6642badf8224c96556d7f5d1688f1abd435 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:18366bba9c84d2a9731f135beba5eafb86b358fdd397a967e512cf89edd5e0c6 0.1s done
#40 exporting manifest list sha256:538e1bebee50ca59f117bc5f7548d1ce8d3e8a64f632bcf98aebb996b9ff56ae 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=229091d73c064de2b311aeadf7eec67b artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us2_custom_port' passed in 22421ms
[quality] stage 'startup_preflight' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 ...
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
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
#11 transferring context: 11.34kB done
#11 DONE 0.0s
#12 [file-indexer  3/12] WORKDIR /app
#12 CACHED
#13 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer 10/12] COPY src /app/src
#14 CACHED
#15 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#15 CACHED
#16 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#17 CACHED
#18 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#19 CACHED
#20 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#20 CACHED
#21 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  3/17] WORKDIR /app
#23 CACHED
#24 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#24 CACHED
#25 [mcp-server  4/17] COPY src /app/src
#25 CACHED
#26 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#26 CACHED
#27 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#28 CACHED
#29 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#32 CACHED
#33 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#34 CACHED
#35 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#35 CACHED
#36 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#36 CACHED
#37 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#39 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#39 exporting attestation manifest sha256:2f350dfd869a99460de08fd767898e4507a9486d3ba972505b6c37794e0f167b 0.1s done
#39 exporting manifest list sha256:87a1277be587753aff68f3b6af5b10323623a5ebd555c896d46e4aa10c1d3c5b
#39 exporting manifest list sha256:87a1277be587753aff68f3b6af5b10323623a5ebd555c896d46e4aa10c1d3c5b 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#40 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#40 exporting attestation manifest sha256:7290da79a77ffc23417a911f8e913a7b55a7b45416b60e3a805e72c5ae09bcfd 0.1s done
#40 exporting manifest list sha256:3cb645cbbc546bb328c390a33eddac12ff0c1c7ab650dbeb82c3de64b23def1b 0.0s done
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
[startup-preflight-smoke] ready scenario passed
{
    "bootstrap":  {
                      "checkedAt":  "2026-02-22T19:38:46.825291+00:00",
                      "collectionName":  "workspace_chunks",
                      "decision":  "skip-already-completed",
                      "reason":  "bootstrap already completed for workspace",
                      "runId":  "f0fb2b4848f04bd4a41d48cdee75194b",
                      "status":  "ready",
                      "trigger":  "auto-startup",
                      "workspaceKey":  "/workspace|c52ddf65534b7b46"
                  },
    "checkedAt":  "2026-02-22T19:38:46.827781+00:00",
    "collection":  {
                       "checkedAt":  "2026-02-22T19:38:46.825477+00:00",
                       "collectionName":  "workspace_chunks",
                       "exists":  true,
                       "pointCount":  9408
                   },
    "collectionName":  "workspace_chunks",
    "indexMode":  "full-scan",
    "mcpEndpoint":  "/mcp",
    "preflightChecks":  [
                            {
                                "checkId":  "qdrant_reachability",
                                "checkedAt":  "2026-02-22T19:38:46.818287+00:00",
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
                                "checkedAt":  "2026-02-22T19:38:46.820286+00:00",
                                "details":  {
                                                "workspacePath":  "/workspace"
                                            },
                                "message":  "Рабочая директория доступна для чтения",
                                "severity":  "critical",
                                "status":  "passed"
                            },
                            {
                                "checkId":  "git_available",
                                "checkedAt":  "2026-02-22T19:38:46.820312+00:00",
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
[quality] stage 'startup_preflight' passed in 21554ms
[quality] stage 'startup_bootstrap' started
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-a7de7d067cff4ec19b9fadc5f0d4b4d0 container=/workspace/tests/fixtures/idempotency-runtime-a7de7d067cff4ec19b9fadc5f0d4b4d0
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
#4 ...
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 transferring context: 5.55kB done
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#11 CACHED
#12 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#12 CACHED
#13 [file-indexer 10/12] COPY src /app/src
#13 CACHED
#14 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#14 CACHED
#15 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#15 CACHED
#16 [file-indexer  3/12] WORKDIR /app
#16 CACHED
#17 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#17 CACHED
#18 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#18 CACHED
#19 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#19 CACHED
#20 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#20 CACHED
#21 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#21 CACHED
#22 [mcp-server internal] load build context
#22 transferring context: 11.34kB done
#22 DONE 0.0s
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server  4/17] COPY src /app/src
#26 CACHED
#27 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#27 CACHED
#28 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#28 CACHED
#29 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#29 CACHED
#30 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#30 CACHED
#31 [mcp-server  3/17] WORKDIR /app
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#33 CACHED
#34 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#39 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#39 exporting attestation manifest sha256:e5442a9b833a5d4318cee9828a88a77e41a4d42cd76e5eefc7a79f5e0b9eab07 0.1s done
#39 exporting manifest list sha256:bf251cfd0bb1a579f161e86e69cb1d84f9e269fe4c1cdfcf6c98514a70c47ec2
#39 exporting manifest list sha256:bf251cfd0bb1a579f161e86e69cb1d84f9e269fe4c1cdfcf6c98514a70c47ec2 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#40 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea done
#40 exporting attestation manifest sha256:6b97b4a560ba492022a0cc6c97b3569402c2cf3c4e4c9dc8d882b95ae2dd373d 0.1s done
#40 exporting manifest list sha256:90c664425f3d505e7d8497f6a1408d2cfc9d9240cd09efaf92a390790af30276 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest
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
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
startup bootstrap smoke passed: collection=workspace_chunks points=9408 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\startup-bootstrap-smoke.json
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
[quality] stage 'startup_bootstrap' passed in 21409ms
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 66ms
[quality] stage 'mcp_transport' started
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
#11 transferring context: 11.34kB done
#11 DONE 0.0s
#12 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#12 CACHED
#13 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer  3/12] WORKDIR /app
#14 CACHED
#15 [file-indexer 10/12] COPY src /app/src
#15 CACHED
#16 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#20 CACHED
#21 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#27 CACHED
#28 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#28 CACHED
#29 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#29 CACHED
#30 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#30 CACHED
#31 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#31 CACHED
#32 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#32 CACHED
#33 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [mcp-server  3/17] WORKDIR /app
#35 CACHED
#36 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server  4/17] COPY src /app/src
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#39 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#39 exporting attestation manifest sha256:b8cdddac846eab53373f8b6cfc2fdce4906f0ce5722f5042a383b9d9f7920027 0.1s done
#39 exporting manifest list sha256:8af7d224d69a9a36e1269b110818bc34ea5e4be779357bc522f9f38bfd947202
#39 exporting manifest list sha256:8af7d224d69a9a36e1269b110818bc34ea5e4be779357bc522f9f38bfd947202 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#40 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea done
#40 exporting attestation manifest sha256:816c6eabe951c6a8ce5b7f6ba307d739830f1049bc1b5e1fc4869b1f55fdade0 0.1s done
#40 exporting manifest list sha256:bdf2e8b13b674a9f4778b99f1557e7f8a9363af574aea34edb2d09b6218a3033 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest
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
[quality] stage 'mcp_transport' passed in 21451ms
[quality] stage 'us3' started
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
#10 transferring context: 11.34kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server  4/17] COPY src /app/src
#12 CACHED
#13 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#13 CACHED
#14 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#14 CACHED
#15 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#15 CACHED
#16 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#16 CACHED
#17 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#18 CACHED
#19 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server  3/17] WORKDIR /app
#20 CACHED
#21 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#21 CACHED
#22 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#22 CACHED
#23 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#23 CACHED
#24 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [file-indexer 10/12] COPY src /app/src
#27 CACHED
#28 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#28 CACHED
#29 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#29 CACHED
#30 [file-indexer  3/12] WORKDIR /app
#30 CACHED
#31 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#31 CACHED
#32 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#32 CACHED
#33 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#35 CACHED
#36 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#39 exporting attestation manifest sha256:bbfe8bdd3130dc72d20a3a381d03140e2bc918a97e7501ecef49c8c3bc8431eb
#39 exporting attestation manifest sha256:bbfe8bdd3130dc72d20a3a381d03140e2bc918a97e7501ecef49c8c3bc8431eb 0.1s done
#39 exporting manifest list sha256:274907d1ef7569b123fca69e1ce5d39d8266ca820d467b681ec82520f0dd69be 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:c3f08f7fc094540e985c1c24dc0fd720f466354a5ca482a25c9aa75ce931cb26 0.1s done
#40 exporting manifest list sha256:ed093cd7115cdb645451e7eb55920d39144478221923f729ac36b36d91d31227 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-913219e6bdf64c619548dd5d7e780441 container=/workspace/tests/fixtures/delta-runtime-913219e6bdf64c619548dd5d7e780441
US1 delta changed-only completed. run=b29cd8c69195449f89dbcc1d1f22f6d4
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=ad9f220de5eb44d9b3dfdac1fbf5a28c results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US1 ingestion collection creation passed. runId=0c4e34bb3979464db83a3a69f6afd310 points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-9cd98ff6e9e84005b39ee5cc3358f0d3 container=/workspace/tests/fixtures/idempotency-runtime-9cd98ff6e9e84005b39ee5cc3358f0d3
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=0b032e2be894458ba1b5561709997328
[US1] runId=0b032e2be894458ba1b5561709997328 status=running attempt=1/120
[US1] runId=0b032e2be894458ba1b5561709997328 status=completed attempt=2/120
[US1] runId=0b032e2be894458ba1b5561709997328 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=a893dbd57e49477b96bfcd8cb246dafa
[US1] runId=a893dbd57e49477b96bfcd8cb246dafa status=running attempt=1/120
[US1] runId=a893dbd57e49477b96bfcd8cb246dafa status=completed attempt=2/120
[US1] runId=a893dbd57e49477b96bfcd8cb246dafa finished status=completed
US1 repeat-run completed. run1=0b032e2be894458ba1b5561709997328 run2=a893dbd57e49477b96bfcd8cb246dafa artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-0fea28f8fdf94b4e991177a44af10fa7 container=/workspace/tests/fixtures/idempotency-runtime-0fea28f8fdf94b4e991177a44af10fa7
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=59db3e2b4cfb46ab9329df7791d1c563
[US1] runId=59db3e2b4cfb46ab9329df7791d1c563 status=running attempt=1/120
[US1] runId=59db3e2b4cfb46ab9329df7791d1c563 status=completed attempt=2/120
[US1] runId=59db3e2b4cfb46ab9329df7791d1c563 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=f5d895c296e545c4ad29ac3dea0386eb
[US1] runId=f5d895c296e545c4ad29ac3dea0386eb status=running attempt=1/120
[US1] runId=f5d895c296e545c4ad29ac3dea0386eb status=completed attempt=2/120
[US1] runId=f5d895c296e545c4ad29ac3dea0386eb finished status=completed
US1 repeat-run completed. run1=59db3e2b4cfb46ab9329df7791d1c563 run2=f5d895c296e545c4ad29ac3dea0386eb artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
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
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.34kB done
#11 DONE 0.0s
#12 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#14 CACHED
#15 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#15 CACHED
#16 [mcp-server  4/17] COPY src /app/src
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server  3/17] WORKDIR /app
#18 CACHED
#19 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#19 CACHED
#20 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#21 CACHED
#22 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/12] COPY src /app/src
#28 CACHED
#29 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#32 CACHED
#33 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [file-indexer  3/12] WORKDIR /app
#34 CACHED
#35 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#35 CACHED
#36 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:34bd3060aa7a11d05f28e68368e2d6b47b8f9d5f80b1f342d36c0a79d2c5060d done
#39 exporting config sha256:18dfe22d740431fca57073f753bacd7f75e0b30fcad125dc38570a9813a2dbea 0.0s done
#39 exporting attestation manifest sha256:b5933994ce2132b8d7924c8461a03b4af47a187eaedfc37035fff488391e4b11
#39 exporting attestation manifest sha256:b5933994ce2132b8d7924c8461a03b4af47a187eaedfc37035fff488391e4b11 0.1s done
#39 exporting manifest list sha256:bf6987e84b57fdf306ac34900c04b107cd49dc5b9d2d3411897a97538926910f
#39 exporting manifest list sha256:bf6987e84b57fdf306ac34900c04b107cd49dc5b9d2d3411897a97538926910f 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:d11f80454f84d8f19c8d6eaa7722677f51219d20e8de5311e8a89a5d8b7bb1ee done
#40 exporting config sha256:7de3cf1acba966a8bfb16da0bae23046ec7049dbf6f0c5b55960b9b6382c04b9 done
#40 exporting attestation manifest sha256:308d533215ce9c6574ea2cef2d85ecedb719ac5547278c08d66ca98c7856dee2 0.1s done
#40 exporting manifest list sha256:8f3777d1b965ff9f47974d05118503ffcecacb15234045386d167d1c98a5612b 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=3013edd2bf044b0a9c33ace3a54c7836 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us3' passed in 53271ms
Quality run passed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-22T22:40:30.5045766+03:00
- exitCode: 0
