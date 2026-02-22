# Quality Stability Run

- startedAt: 2026-02-22T16:43:39.4279798+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 83 items
tests\unit\file_indexer\test_chunk_identity.py ...                       [  3%]
tests\unit\file_indexer\test_chunker.py .....                            [  9%]
tests\unit\file_indexer\test_embedding_retry.py ..                       [ 12%]
tests\unit\file_indexer\test_file_filters.py .....                       [ 18%]
tests\unit\file_indexer\test_file_fingerprint.py .....                   [ 24%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_config.py . [ 25%]
.                                                                        [ 26%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_resilience.py . [ 27%]
.                                                                        [ 28%]
tests\unit\file_indexer\test_git_diff_reader.py ..                       [ 31%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 33%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 36%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 38%]
tests\unit\mcp_server\test_mcp_tool_adapters_search.py ...               [ 42%]
tests\unit\mcp_server\test_mcp_tool_registry.py ..                       [ 44%]
tests\unit\mcp_server\test_mcp_transport_concurrency.py .                [ 45%]
tests\unit\mcp_server\test_mcp_transport_error_mapper.py ...             [ 49%]
tests\unit\mcp_server\test_mcp_transport_handshake.py ....               [ 54%]
tests\unit\mcp_server\test_mcp_transport_negative_cases.py ...           [ 57%]
tests\unit\mcp_server\test_mcp_transport_protocol_models.py ....         [ 62%]
tests\unit\mcp_server\test_mcp_transport_session_state.py ..             [ 65%]
tests\unit\mcp_server\test_root_commands_endpoint.py ..                  [ 67%]
tests\unit\mcp_server\test_search_repository_missing_collection.py ..... [ 73%]
                                                                         [ 73%]
tests\unit\mcp_server\test_search_result_resolution.py ....              [ 78%]
tests\unit\mcp_server\test_semantic_search_filters.py ..                 [ 80%]
tests\unit\mcp_server\test_semantic_search_service.py ..                 [ 83%]
tests\unit\mcp_server\test_startup_preflight_checks.py ....              [ 87%]
tests\unit\mcp_server\test_startup_preflight_models.py ...               [ 91%]
tests\unit\mcp_server\test_startup_readiness_endpoint.py ..              [ 93%]
tests\unit\mcp_server\test_startup_readiness_summary.py .                [ 95%]
tests\unit\mcp_server\test_vector_upsert_repository_config.py ..         [ 97%]
tests\unit\mcp_server\test_vector_upsert_repository_resilience.py ..     [100%]
============================= 83 passed in 0.83s ==============================
[quality] stage 'unit' passed in 1339ms
[quality] stage 'us1' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.6s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.6s
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
#10 transferring context: 10.26kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#12 CACHED
#13 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#13 CACHED
#14 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#14 CACHED
#15 [mcp-server  4/17] COPY src /app/src
#15 CACHED
#16 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#16 CACHED
#17 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#17 CACHED
#18 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#18 CACHED
#19 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#21 CACHED
#22 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  3/17] WORKDIR /app
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  3/12] WORKDIR /app
#28 CACHED
#29 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [file-indexer 10/12] COPY src /app/src
#30 CACHED
#31 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#31 CACHED
#32 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#32 CACHED
#33 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#33 CACHED
#34 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#34 CACHED
#35 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#35 CACHED
#36 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#39 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#39 exporting attestation manifest sha256:d0e0de0a89a5bea4b746a525545be780383dc3e026cc82768c6199da63081f31 0.1s done
#39 exporting manifest list sha256:784cd13bb8a88955354757ae26932a6ca90a16e367cd01b1efc31ba78a4a8969
#39 exporting manifest list sha256:784cd13bb8a88955354757ae26932a6ca90a16e367cd01b1efc31ba78a4a8969 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#40 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d 0.0s done
#40 exporting attestation manifest sha256:7159c50360cafc920f615b4093ae869256bc7fd0d5a588fe7ee65d353b6758ed 0.1s done
#40 exporting manifest list sha256:658d5b5674ecee752a36c9b2b56c39464d767ced81e0f3fe01e373c425fa63be 0.0s done
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 13 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-a1ef6d96f8f6434bad3f4f1789763c29 container=/workspace/tests/fixtures/idempotency-runtime-a1ef6d96f8f6434bad3f4f1789763c29
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=0674eaad2cdc423fb4738382b3a15dbc
[US1] runId=0674eaad2cdc423fb4738382b3a15dbc status=running attempt=1/120
[US1] runId=0674eaad2cdc423fb4738382b3a15dbc status=completed attempt=2/120
[US1] runId=0674eaad2cdc423fb4738382b3a15dbc finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=ee762405b7fd4389b9f9764f782775e1
[US1] runId=ee762405b7fd4389b9f9764f782775e1 status=running attempt=1/120
[US1] runId=ee762405b7fd4389b9f9764f782775e1 status=completed attempt=2/120
[US1] runId=ee762405b7fd4389b9f9764f782775e1 finished status=completed
US1 repeat-run completed. run1=0674eaad2cdc423fb4738382b3a15dbc run2=ee762405b7fd4389b9f9764f782775e1 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-bd6786d159984478b737f213701c1362 container=/workspace/tests/fixtures/idempotency-runtime-bd6786d159984478b737f213701c1362
US2 deterministic update completed. run1=170f3804ba8144a2ae204ba243a1c9e7 run2=8b1da110bca0498f969ecafe05790b74
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-50cebb3441554fa387bfbee0460c2446 container=/workspace/tests/fixtures/idempotency-runtime-50cebb3441554fa387bfbee0460c2446
US3 stale cleanup completed. run2=f68c9200c6d44d83b33d47f5c83396c7
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
[quality] stage 'us1' passed in 25879ms
[quality] stage 'us1_persistence' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 791B done
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
#10 transferring context: 10.26kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#12 CACHED
#13 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#13 CACHED
#14 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#15 CACHED
#16 [mcp-server  3/17] WORKDIR /app
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server  4/17] COPY src /app/src
#18 CACHED
#19 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#20 CACHED
#21 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#22 CACHED
#23 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#23 CACHED
#24 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#26 CACHED
#27 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#27 CACHED
#28 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#28 CACHED
#29 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#29 CACHED
#30 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#30 CACHED
#31 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#31 CACHED
#32 [file-indexer  3/12] WORKDIR /app
#32 CACHED
#33 [file-indexer 10/12] COPY src /app/src
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#39 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#39 exporting attestation manifest sha256:ed52e3d7a066ed2943405c4f7278abb4a66cadf66a391d59f14727d96414fadd
#39 exporting attestation manifest sha256:ed52e3d7a066ed2943405c4f7278abb4a66cadf66a391d59f14727d96414fadd 0.1s done
#39 exporting manifest list sha256:fd431ba580b9253c79bb1e23f0d996dc8fc3b35648a31e997eda71f67ac55eee
#39 exporting manifest list sha256:fd431ba580b9253c79bb1e23f0d996dc8fc3b35648a31e997eda71f67ac55eee 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#40 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#40 exporting attestation manifest sha256:504851d2a83f4630ec2ccf5ca7b93bbc8007a64f9a5609bafa76ba82ec9b4c83 0.1s done
#40 exporting manifest list sha256:75d6e54fac53574d31890fd6fbe56b9a626c1102300f53cbb9e6f8a01ece4404 0.0s done
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
US1 ingestion collection creation passed. runId=308d2ad9579d47ccbfc975675d4578a6 points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
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
[quality] stage 'us1_persistence' passed in 23422ms
[quality] stage 'integration' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
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
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 10.26kB done
#11 DONE 0.0s
#12 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#12 CACHED
#13 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#13 CACHED
#14 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server  4/17] COPY src /app/src
#16 CACHED
#17 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#17 CACHED
#18 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#18 CACHED
#19 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#19 CACHED
#20 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#22 CACHED
#23 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#23 CACHED
#24 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#24 CACHED
#25 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#25 CACHED
#26 [mcp-server  3/17] WORKDIR /app
#26 CACHED
#27 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#27 CACHED
#28 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#28 CACHED
#29 [file-indexer 10/12] COPY src /app/src
#29 CACHED
#30 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#30 CACHED
#31 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#31 CACHED
#32 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#32 CACHED
#33 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  3/12] WORKDIR /app
#35 CACHED
#36 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#39 exporting attestation manifest sha256:ccd598500952873e9f4e4c0b89bb7fc9a8645a2083aba247c7416308ae22845a 0.1s done
#39 exporting manifest list sha256:aeb619735c208710fd0a34dfde08e803342c0ded41abd3e49cba542f0e680294
#39 exporting manifest list sha256:aeb619735c208710fd0a34dfde08e803342c0ded41abd3e49cba542f0e680294 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#40 exporting attestation manifest sha256:c1fd1082e3af20f6e061c021eb84c5373d2ef0bcdd29e59fc2ada29f0f8d181e 0.1s done
#40 exporting manifest list sha256:c6b5cfe21eda6dd4b1f764fcf5bfab7ba7d37ceb6523ea4e19dc1dc5d8f508a0 0.0s done
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
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
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
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB 0.0s done
#11 DONE 0.0s
#8 [mcp-server internal] load build context
#8 transferring context: 10.26kB 0.0s done
#8 DONE 0.0s
#12 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#12 CACHED
#13 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#13 CACHED
#14 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#15 CACHED
#16 [file-indexer  3/12] WORKDIR /app
#16 CACHED
#17 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#19 CACHED
#20 [file-indexer 10/12] COPY src /app/src
#20 CACHED
#21 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  4/17] COPY src /app/src
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server  3/17] WORKDIR /app
#27 CACHED
#28 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#28 CACHED
#29 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#30 CACHED
#31 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#33 CACHED
#34 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#34 CACHED
#35 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#35 CACHED
#36 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d 0.0s done
#39 exporting attestation manifest sha256:bf3ffc370cc37255336800940393ceebd73e222d221b29b59f6e67536ecb92a1
#39 exporting attestation manifest sha256:bf3ffc370cc37255336800940393ceebd73e222d221b29b59f6e67536ecb92a1 0.1s done
#39 exporting manifest list sha256:ac2b66c886d0c22eb8f1d7520bd52e52c8cdf2f4322ebf29420ad735fc3a7a44
#39 exporting manifest list sha256:ac2b66c886d0c22eb8f1d7520bd52e52c8cdf2f4322ebf29420ad735fc3a7a44 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#40 exporting attestation manifest sha256:b01451fd7c5497f387a0c3ad8149b6a5328cbb56d72f62fc407ed57508993b14 0.1s done
#40 exporting manifest list sha256:c66788ccf970ddc61a735f28e33b9fb081300860535d526506597595f59d4741 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
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
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
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
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 791B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.8s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.8s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 10.26kB done
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#12 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#12 CACHED
#13 [mcp-server  4/17] COPY src /app/src
#13 CACHED
#14 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#14 CACHED
#15 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#15 CACHED
#16 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#17 CACHED
#18 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#18 CACHED
#19 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#20 CACHED
#21 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server  3/17] WORKDIR /app
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#9 [file-indexer internal] load build context
#9 transferring context: 5.55kB done
#9 DONE 0.0s
#28 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#29 CACHED
#30 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#32 CACHED
#33 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#33 CACHED
#34 [file-indexer 10/12] COPY src /app/src
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer  3/12] WORKDIR /app
#36 CACHED
#37 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#39 exporting attestation manifest sha256:f986abc7469de1ef0b3b02dd2d4cbe5d6d94b98083033a3c25c89963560615cf 0.1s done
#39 exporting manifest list sha256:c95f639428e14606f88b5c84bd27638055bf76f24f8ba8c624c0037616cb0b50
#39 exporting manifest list sha256:c95f639428e14606f88b5c84bd27638055bf76f24f8ba8c624c0037616cb0b50 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#40 exporting attestation manifest sha256:36edb9d4e426aca2cf62f7d2854b041d5376772a74bf756d5d0a2347c9de99dc 0.1s done
#40 exporting manifest list sha256:3a9e8687e7840ef936413812183b48ec5d7e848132cb63dc6987c5c6ecdbe981 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
#42 [file-indexer] resolving provenance for metadata file
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-68410e1c34fb41e1ab5c8d5cc2cf99b3 container=/workspace/tests/fixtures/delta-runtime-68410e1c34fb41e1ab5c8d5cc2cf99b3
US1 delta changed-only completed. run=7c161ff987a74ce9a49ac327c0f85130
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-6be129bcb1c5466d9856afebcdbbc1ec container=/workspace/tests/fixtures/delta-runtime-6be129bcb1c5466d9856afebcdbbc1ec
US2 delta delete+rename completed. run=33dfab6f776f451e8d522c77cbac00e7
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-cfc53fc1ed2d4ce2af8b6ce7ed3890cb container=/workspace/tests/fixtures/delta-runtime-cfc53fc1ed2d4ce2af8b6ce7ed3890cb
US3 delta fallback completed. run=239fe66838b74e18805438bef2f02b67 reason=BASE_REF_NOT_FOUND
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
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
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
#10 transferring context: 10.26kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#13 CACHED
#14 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#15 CACHED
#16 [mcp-server  3/17] WORKDIR /app
#16 CACHED
#17 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  4/17] COPY src /app/src
#18 CACHED
#19 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#19 CACHED
#20 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#20 CACHED
#21 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#21 CACHED
#22 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#25 CACHED
#26 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#26 CACHED
#27 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#27 CACHED
#28 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#28 CACHED
#29 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#29 CACHED
#30 [file-indexer 10/12] COPY src /app/src
#30 CACHED
#31 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#31 CACHED
#32 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#32 CACHED
#33 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#35 CACHED
#36 [file-indexer  3/12] WORKDIR /app
#36 CACHED
#37 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers 0.0s done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#39 exporting attestation manifest sha256:110e65722108db96b4d2ab53dd1293c42b8781111ae375ba7fcd67a6921533c8 0.1s done
#39 exporting manifest list sha256:94cf9e4b474176472cc89e73aee682f9a3f074df917f34f7b4dceb294c509f97
#39 exporting manifest list sha256:94cf9e4b474176472cc89e73aee682f9a3f074df917f34f7b4dceb294c509f97 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#40 exporting attestation manifest sha256:7b1e45a5675c8958f2b90bf1c39a7d6a836948e274908cd85f30ee33ecf80c64 0.1s done
#40 exporting manifest list sha256:1d7511065d1109842bc1fb60966b99d70f9a523f781b16cbd159e7f94f30324c 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Error
dependency failed to start: container ndlss-memory-file-indexer is unhealthy
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
[quality] stage 'integration' failed code=INTEGRATION_FAILED message=docker compose failed with exit code 1 (args: -f Z:\WORK\ndlss-memory\infra\\docker\\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build)
[quality] stage 'us2' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
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
#10 transferring context: 10.26kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [file-indexer  3/12] WORKDIR /app
#12 CACHED
#13 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#14 CACHED
#15 [file-indexer 10/12] COPY src /app/src
#15 CACHED
#16 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#16 CACHED
#17 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#23 CACHED
#24 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#28 CACHED
#29 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#29 CACHED
#30 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#30 CACHED
#31 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#31 CACHED
#32 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#32 CACHED
#33 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#33 CACHED
#34 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#34 CACHED
#35 [mcp-server  3/17] WORKDIR /app
#35 CACHED
#36 [mcp-server  4/17] COPY src /app/src
#36 CACHED
#37 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d 0.0s done
#39 exporting attestation manifest sha256:b5d0831facfdd543317072e61729f6d61018051c1056719d544219b93e2a6c60
#39 exporting attestation manifest sha256:b5d0831facfdd543317072e61729f6d61018051c1056719d544219b93e2a6c60 0.1s done
#39 exporting manifest list sha256:f22c1ce9176f442a4edea7824df39628bd68f9e1b00c3321db9457d0a7b401f4
#39 exporting manifest list sha256:f22c1ce9176f442a4edea7824df39628bd68f9e1b00c3321db9457d0a7b401f4 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#40 exporting attestation manifest sha256:6832432c0e786c6230b955d107aba49894eccb5cb2d64692bf525841ce69c28d 0.1s done
#40 exporting manifest list sha256:6790b807ee73f2fb54c66f8af5d06886629cb00c85475d049aedba1daaf36d86 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 search flow completed. ingestionRunId=651f9f5b4f2648c6bc96f165eadadd61 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
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
[quality] stage 'us2' passed in 22128ms
[quality] stage 'us2_custom_port' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
#3 DONE 0.0s
#4 [auth] library/python:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/alpine:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#6 ...
#7 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#7 DONE 0.7s
#6 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#6 DONE 0.7s
#8 [mcp-server internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [file-indexer internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#12 [mcp-server internal] load build context
#12 transferring context: 10.26kB done
#12 DONE 0.0s
#13 [file-indexer internal] load build context
#13 transferring context: 5.55kB done
#13 DONE 0.0s
#14 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#19 CACHED
#20 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#20 CACHED
#21 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#21 CACHED
#22 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#22 CACHED
#23 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server  4/17] COPY src /app/src
#25 CACHED
#26 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#27 CACHED
#28 [mcp-server  3/17] WORKDIR /app
#28 CACHED
#29 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#32 CACHED
#33 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#33 CACHED
#34 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#34 CACHED
#35 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [file-indexer  3/12] WORKDIR /app
#36 CACHED
#37 [file-indexer 10/12] COPY src /app/src
#37 CACHED
#38 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#39 CACHED
#40 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#40 CACHED
#41 [file-indexer] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#41 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 0.0s done
#41 exporting attestation manifest sha256:7e5d8f5d1496d6c823aac558e948f1f9254bc99530bca5f484b111156423ce79
#41 exporting attestation manifest sha256:7e5d8f5d1496d6c823aac558e948f1f9254bc99530bca5f484b111156423ce79 0.1s done
#41 exporting manifest list sha256:fe744f879cbc377934035df8ff7c9e7a2bbe33039bedcebb184ce9a04a52c38b 0.0s done
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 DONE 0.2s
#42 [mcp-server] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#42 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#42 exporting attestation manifest sha256:35926c61fd8de14c87d379622f8b120ba2d05ae7000fabda965f6452c6a884d2 0.1s done
#42 exporting manifest list sha256:82d660f5aaae873455b3b213dcfd8cace47a3f16a77ff3455b0cf67f784e899b 0.0s done
#42 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=dcd87949e19f4cffa4c1a7b3d072f89c artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us2_custom_port' passed in 22323ms
[quality] stage 'startup_preflight' started
[quality] stage 'startup_preflight' failed code=STARTUP_PREFLIGHT_SMOKE_FAILED message= ndlss-memory-mcp-server  Built
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 35ms
[quality] stage 'mcp_transport' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 791B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 ...
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.3s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 transferring context: 10.26kB done
#9 DONE 0.0s
#10 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#12 CACHED
#13 [mcp-server  3/17] WORKDIR /app
#13 CACHED
#14 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#14 CACHED
#15 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#15 CACHED
#16 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  4/17] COPY src /app/src
#18 CACHED
#19 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#20 CACHED
#21 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#21 CACHED
#22 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/12] COPY src /app/src
#28 CACHED
#29 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#29 CACHED
#30 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#30 CACHED
#31 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#31 CACHED
#32 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 CACHED
#33 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#33 CACHED
#34 [file-indexer  3/12] WORKDIR /app
#34 CACHED
#35 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#35 CACHED
#36 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#36 CACHED
#37 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#39 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#39 exporting attestation manifest sha256:f12e925157fc4cc44e02770717aef7b13c5ed557a65de7f14c85b2b8cce6e213 0.1s done
#39 exporting manifest list sha256:e62e99dd27d9d66a86e3c598eaa64d12196a4f6bfe8c9edc057642f0905cbdf5
#39 exporting manifest list sha256:e62e99dd27d9d66a86e3c598eaa64d12196a4f6bfe8c9edc057642f0905cbdf5 0.1s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#40 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 0.0s done
#40 exporting attestation manifest sha256:07aa8f6b60592e21ade4f347719d14be4d567292fabbb7627971d85aea2350f8 0.1s done
#40 exporting manifest list sha256:f2f225146b0a10e704350dd59cfe1a7e5adfd50b264b840c5eb20ec12eeee68a 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
#42 [file-indexer] resolving provenance for metadata file
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
[quality] stage 'mcp_transport' passed in 19991ms
[quality] stage 'us3' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 791B 0.0s done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B 0.0s done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B 0.0s done
#7 DONE 0.0s
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#8 [mcp-server internal] load build context
#8 transferring context: 10.26kB done
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 transferring context: 5.55kB done
#9 DONE 0.0s
#12 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server  3/17] WORKDIR /app
#14 CACHED
#15 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#15 CACHED
#16 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#19 CACHED
#20 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#20 CACHED
#21 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#21 CACHED
#22 [mcp-server  4/17] COPY src /app/src
#22 CACHED
#23 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#23 CACHED
#24 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#24 CACHED
#25 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#26 CACHED
#27 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#27 CACHED
#28 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#28 CACHED
#29 [file-indexer 10/12] COPY src /app/src
#29 CACHED
#30 [file-indexer  3/12] WORKDIR /app
#30 CACHED
#31 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#31 CACHED
#32 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#32 CACHED
#33 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#35 CACHED
#36 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#36 CACHED
#37 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 0.0s done
#39 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#39 exporting attestation manifest sha256:693f86ed44fad082696d8508b8dd46d808d2b149b86173427d902237d7ec4864
#39 exporting attestation manifest sha256:693f86ed44fad082696d8508b8dd46d808d2b149b86173427d902237d7ec4864 0.1s done
#39 exporting manifest list sha256:f39d1f7b1c158f836ed4c042041caa7ce7cf0c9007bad7392864f907b92537a1 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 0.0s done
#40 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d done
#40 exporting attestation manifest sha256:50e15522b92a1c4cd37f2494344c26d1055a36bc364a4bc628aeb67d526e34da 0.1s done
#40 exporting manifest list sha256:7e4633fbe21c004b726bdfebe8826c8aafc8b4720acdc8b242aeaf5f150524e3 0.0s done
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
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-0cf6c5b39f8149438cb6a1304276d847 container=/workspace/tests/fixtures/delta-runtime-0cf6c5b39f8149438cb6a1304276d847
US1 delta changed-only completed. run=d4603a4bb8ea430a9a6d771551c31acf
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=516ff09fa6fe4d53b88e54d4fdf93a02 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US1 ingestion collection creation passed. runId=f988fa1f117e46a38cc43d18b70ed161 points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-a7f45f6ad5c14935acb927a376510d06 container=/workspace/tests/fixtures/idempotency-runtime-a7f45f6ad5c14935acb927a376510d06
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=9c42099e6d9840068b39df8c27f8b0bb
[US1] runId=9c42099e6d9840068b39df8c27f8b0bb status=running attempt=1/120
[US1] runId=9c42099e6d9840068b39df8c27f8b0bb status=completed attempt=2/120
[US1] runId=9c42099e6d9840068b39df8c27f8b0bb finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=f67ba972b3a84d22a7534afe44c06f67
[US1] runId=f67ba972b3a84d22a7534afe44c06f67 status=running attempt=1/120
[US1] runId=f67ba972b3a84d22a7534afe44c06f67 status=completed attempt=2/120
[US1] runId=f67ba972b3a84d22a7534afe44c06f67 finished status=completed
US1 repeat-run completed. run1=9c42099e6d9840068b39df8c27f8b0bb run2=f67ba972b3a84d22a7534afe44c06f67 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-0a18bbc5fc73486e8dea266c8409c3ee container=/workspace/tests/fixtures/idempotency-runtime-0a18bbc5fc73486e8dea266c8409c3ee
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=0fb1fad5ca004dda8a0ea11b94cefa75
[US1] runId=0fb1fad5ca004dda8a0ea11b94cefa75 status=running attempt=1/120
[US1] runId=0fb1fad5ca004dda8a0ea11b94cefa75 status=completed attempt=2/120
[US1] runId=0fb1fad5ca004dda8a0ea11b94cefa75 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=ab29fa56c72446368cd3d4793d54672e
[US1] runId=ab29fa56c72446368cd3d4793d54672e status=running attempt=1/120
[US1] runId=ab29fa56c72446368cd3d4793d54672e status=completed attempt=2/120
[US1] runId=ab29fa56c72446368cd3d4793d54672e finished status=completed
US1 repeat-run completed. run1=0fb1fad5ca004dda8a0ea11b94cefa75 run2=ab29fa56c72446368cd3d4793d54672e artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
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
#2 transferring dockerfile: 791B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 ...
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.6s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.6s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#11 CACHED
#12 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer 10/12] COPY src /app/src
#13 CACHED
#14 [file-indexer  3/12] WORKDIR /app
#14 CACHED
#15 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#15 CACHED
#16 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#19 CACHED
#20 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#20 CACHED
#21 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#21 CACHED
#22 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#22 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#22 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#22 DONE 0.0s
#8 [mcp-server internal] load build context
#8 transferring context: 10.26kB done
#8 DONE 0.0s
#23 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#23 CACHED
#24 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#25 CACHED
#26 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#26 CACHED
#27 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server  4/17] COPY src /app/src
#28 CACHED
#29 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#30 CACHED
#31 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#32 CACHED
#33 [mcp-server  3/17] WORKDIR /app
#33 CACHED
#34 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#34 CACHED
#35 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#36 CACHED
#37 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:7dae8a7a89ecb38623fc2052dca1fbbec47c0a708a7b65396ed33af5dd560f61 done
#39 exporting config sha256:1b38872ef6710f583f0eb0f80900e7d95a63e6e1dff549bb44092e84b4177910 done
#39 exporting attestation manifest sha256:59196cca2c9fb87e4209a87d0bf35681e7b798752bf6e2915e0bfb0fd792a6ba 0.0s done
#39 exporting manifest list sha256:0cba124b2439156a07fb994856087ce76e3a78e6e1e9bc583147e556e92d7e1e
#39 exporting manifest list sha256:0cba124b2439156a07fb994856087ce76e3a78e6e1e9bc583147e556e92d7e1e 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:6a7b4a361f9f24397dd6fbc914a67e576145b2bda40f3ea107529ca86a4d7ef1 done
#40 exporting config sha256:70343fdb8a0ae160d74a8b44a806e977cd44daa8649a599a776e1eb0f850733d 0.0s done
#40 exporting attestation manifest sha256:e7580b3d4362dae80207ff1db37c8af5d6265fb394e7c00959993f9469c614e6 0.1s done
#40 exporting manifest list sha256:de286b5ff7b795bec06a876d9a0ac18356f2cab97a54b1d0e5e8571f79beb333 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
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
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 custom external port scenario passed. runId=51361c8b2b89492fa011160c01a35414 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us3' passed in 55102ms
Quality run failed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-22T16:48:52.9485337+03:00
- exitCode: 1
