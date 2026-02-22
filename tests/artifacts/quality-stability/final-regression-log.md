# Quality Stability Run

- startedAt: 2026-02-22T14:11:16.9123558+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 73 items
tests\unit\file_indexer\test_chunk_identity.py ...                       [  4%]
tests\unit\file_indexer\test_chunker.py .....                            [ 10%]
tests\unit\file_indexer\test_embedding_retry.py ..                       [ 13%]
tests\unit\file_indexer\test_file_filters.py .....                       [ 20%]
tests\unit\file_indexer\test_file_fingerprint.py .....                   [ 27%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_config.py . [ 28%]
.                                                                        [ 30%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_resilience.py . [ 31%]
.                                                                        [ 32%]
tests\unit\file_indexer\test_git_diff_reader.py ..                       [ 35%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 38%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 41%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 43%]
tests\unit\mcp_server\test_mcp_tool_adapters_search.py ...               [ 47%]
tests\unit\mcp_server\test_mcp_tool_registry.py ..                       [ 50%]
tests\unit\mcp_server\test_mcp_transport_concurrency.py .                [ 52%]
tests\unit\mcp_server\test_mcp_transport_error_mapper.py ...             [ 56%]
tests\unit\mcp_server\test_mcp_transport_handshake.py ....               [ 61%]
tests\unit\mcp_server\test_mcp_transport_negative_cases.py ...           [ 65%]
tests\unit\mcp_server\test_mcp_transport_protocol_models.py ....         [ 71%]
tests\unit\mcp_server\test_mcp_transport_session_state.py ..             [ 73%]
tests\unit\mcp_server\test_root_commands_endpoint.py ..                  [ 76%]
tests\unit\mcp_server\test_search_repository_missing_collection.py ..... [ 83%]
                                                                         [ 83%]
tests\unit\mcp_server\test_search_result_resolution.py ....              [ 89%]
tests\unit\mcp_server\test_semantic_search_filters.py ..                 [ 91%]
tests\unit\mcp_server\test_semantic_search_service.py ..                 [ 94%]
tests\unit\mcp_server\test_vector_upsert_repository_config.py ..         [ 97%]
tests\unit\mcp_server\test_vector_upsert_repository_resilience.py ..     [100%]
============================= 73 passed in 0.82s ==============================
[quality] stage 'unit' passed in 1251ms
[quality] stage 'us1' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 697B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [auth] library/alpine:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/python:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 ...
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 0.7s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 0.7s
#8 [file-indexer internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [mcp-server internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#12 [file-indexer internal] load build context
#12 transferring context: 5.50kB done
#12 DONE 0.0s
#13 [mcp-server internal] load build context
#13 transferring context: 9.62kB done
#13 DONE 0.0s
#14 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#15 CACHED
#16 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#16 CACHED
#17 [file-indexer  3/11] WORKDIR /app
#17 CACHED
#18 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#19 CACHED
#20 [file-indexer  9/11] COPY src /app/src
#20 CACHED
#21 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#21 CACHED
#22 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#22 CACHED
#23 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server  3/17] WORKDIR /app
#28 CACHED
#29 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#29 CACHED
#30 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#30 CACHED
#31 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#31 CACHED
#32 [mcp-server  4/17] COPY src /app/src
#32 CACHED
#33 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#33 CACHED
#34 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#35 CACHED
#36 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#36 CACHED
#37 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#37 CACHED
#38 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#38 CACHED
#39 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#39 CACHED
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#40 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#40 exporting attestation manifest sha256:9daf8df3dd91294d777e000d6b66228a6ac18d085ec209653a69c5602680acdc 0.1s done
#40 exporting manifest list sha256:025bd3eb3dc467c6fbfa16ffd8c009f2d4452d1bd6d73ddd82e79779e8d3b268
#40 exporting manifest list sha256:025bd3eb3dc467c6fbfa16ffd8c009f2d4452d1bd6d73ddd82e79779e8d3b268 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#41 [mcp-server] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#41 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#41 exporting attestation manifest sha256:9d8d944b9e302349851aa694fa14edc6be5214e13251ba56de3a604f8beeedf9 0.1s done
#41 exporting manifest list sha256:727b446702486a5786075c579d718c4247365cead00e372d8bc43b892d3be779 0.0s done
#41 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#41 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#41 DONE 0.2s
#42 [file-indexer] resolving provenance for metadata file
#42 DONE 0.0s
#43 [mcp-server] resolving provenance for metadata file
#43 DONE 0.0s
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
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 9 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-eed0302e859849818e31dd579f5d08dd container=/workspace/tests/fixtures/idempotency-runtime-eed0302e859849818e31dd579f5d08dd
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=81d0cf40429647f58f382facb30fb9da
[US1] runId=81d0cf40429647f58f382facb30fb9da status=running attempt=1/120
[US1] runId=81d0cf40429647f58f382facb30fb9da status=completed attempt=2/120
[US1] runId=81d0cf40429647f58f382facb30fb9da finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=8b47eb4354a840e091c07825ed18e24f
[US1] runId=8b47eb4354a840e091c07825ed18e24f status=running attempt=1/120
[US1] runId=8b47eb4354a840e091c07825ed18e24f status=completed attempt=2/120
[US1] runId=8b47eb4354a840e091c07825ed18e24f finished status=completed
US1 repeat-run completed. run1=81d0cf40429647f58f382facb30fb9da run2=8b47eb4354a840e091c07825ed18e24f artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-08716978f8a2479aba7ef209dfeac6ca container=/workspace/tests/fixtures/idempotency-runtime-08716978f8a2479aba7ef209dfeac6ca
US2 deterministic update completed. run1=204c1cb8a87d46f7b1a9a9f901d0a3dc run2=131c2b8f49e24b7facf26ec72dfc7f19
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-5ebc9615527541608c5215178c1c592c container=/workspace/tests/fixtures/idempotency-runtime-5ebc9615527541608c5215178c1c592c
US3 stale cleanup completed. run2=cbb379721c6c4b93ba155b2992e60517
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
[quality] stage 'us1' passed in 27527ms
[quality] stage 'us1_persistence' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 697B done
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
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 9.62kB done
#11 DONE 0.0s
#12 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#12 CACHED
#13 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#13 CACHED
#14 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#15 CACHED
#16 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#17 CACHED
#18 [file-indexer  3/11] WORKDIR /app
#18 CACHED
#19 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#19 CACHED
#20 [file-indexer  9/11] COPY src /app/src
#20 CACHED
#21 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#21 CACHED
#22 [mcp-server  4/17] COPY src /app/src
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#27 CACHED
#28 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#28 CACHED
#29 [mcp-server  3/17] WORKDIR /app
#29 CACHED
#30 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#30 CACHED
#31 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#31 CACHED
#32 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#32 CACHED
#33 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#33 CACHED
#34 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#35 CACHED
#36 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#38 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#38 exporting attestation manifest sha256:e43768e5163065307416821c005bbd759f2b6b0b6893c4aa6af9fc7045073ada 0.1s done
#38 exporting manifest list sha256:e6ae03a498b92518d28615f85f860b755b7ff2b7bcf9ab96f262bc0753cdf16f
#38 exporting manifest list sha256:e6ae03a498b92518d28615f85f860b755b7ff2b7bcf9ab96f262bc0753cdf16f 0.0s done
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#39 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#39 exporting attestation manifest sha256:d1168827fa4e83fbe5ca6fb2701ce32207219f4f1170017548e6544e2f3c1e79 0.1s done
#39 exporting manifest list sha256:8087db195c6899775a695a510f4decf9c1ad90c1bab1257d05b3e9919a4d2e43 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
US1 ingestion collection creation passed. runId=83244bd55bd74d359fc40572c2235257 points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
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
[quality] stage 'us1_persistence' passed in 23901ms
[quality] stage 'integration' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 697B done
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
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 9.62kB done
#11 DONE 0.0s
#12 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer  3/11] WORKDIR /app
#13 CACHED
#14 [file-indexer  9/11] COPY src /app/src
#14 CACHED
#15 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#16 CACHED
#17 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#22 CACHED
#23 [mcp-server  3/17] WORKDIR /app
#23 CACHED
#24 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#24 CACHED
#25 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#28 CACHED
#29 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#29 CACHED
#30 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#30 CACHED
#31 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#34 CACHED
#35 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server  4/17] COPY src /app/src
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [mcp-server] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#38 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#38 exporting attestation manifest sha256:30ec77497a4bf2f0d2c0fa757a67138e1e162e60e56aa531dc7ec2553d511b20
#38 exporting attestation manifest sha256:30ec77497a4bf2f0d2c0fa757a67138e1e162e60e56aa531dc7ec2553d511b20 0.1s done
#38 exporting manifest list sha256:ba50e758384ce681d6ef44ebc552215c74ee256e07aa8c5775edd6b252488c80
#38 exporting manifest list sha256:ba50e758384ce681d6ef44ebc552215c74ee256e07aa8c5775edd6b252488c80 0.0s done
#38 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#38 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#38 DONE 0.3s
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#39 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#39 exporting attestation manifest sha256:ff0059e25516cc1ff009bfcc4611312c75e7f94316a396f939e86aeab8c59075 0.1s done
#39 exporting manifest list sha256:db1d1ea8b634a2d17845d8287890ebb2453f04de023728d1ff1eb712a3347d37 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
#3 transferring dockerfile: 697B done
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
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 9.62kB 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#13 CACHED
#14 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  9/11] COPY src /app/src
#16 CACHED
#17 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#17 CACHED
#18 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#18 CACHED
#19 [file-indexer  3/11] WORKDIR /app
#19 CACHED
#20 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server  4/17] COPY src /app/src
#22 CACHED
#23 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#24 CACHED
#25 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#25 CACHED
#26 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#27 CACHED
#28 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#28 CACHED
#29 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#29 CACHED
#30 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#30 CACHED
#31 [mcp-server  3/17] WORKDIR /app
#31 CACHED
#32 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#32 CACHED
#33 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#33 CACHED
#34 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#34 CACHED
#35 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#35 CACHED
#36 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#38 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#38 exporting attestation manifest sha256:be34658f2663524d55c080ce9b998c62cedf27ba728f8ad35c1b3d2b1e4f081e
#38 exporting attestation manifest sha256:be34658f2663524d55c080ce9b998c62cedf27ba728f8ad35c1b3d2b1e4f081e 0.1s done
#38 exporting manifest list sha256:b23ee3e3204c5635a1fd2e8b3f90b56a5e09bd1ebe7ddf6439e7dc9f135a81ba 0.0s done
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#39 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 done
#39 exporting attestation manifest sha256:b406ee8a3a2a5960f765b13851cc531bf4349ef7a7ab2a3645311c5304420453 0.1s done
#39 exporting manifest list sha256:6aa8d827c688516d66323f2535a9a72fd0aba8205b4114c01f5001ac68893c61 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
 ndlss-memory-mcp-server  Built
 ndlss-memory-file-indexer  Built
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
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 697B done
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
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 9.62kB 0.0s done
#11 DONE 0.0s
#12 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#13 CACHED
#14 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  3/11] WORKDIR /app
#16 CACHED
#17 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  9/11] COPY src /app/src
#18 CACHED
#19 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#22 CACHED
#23 [mcp-server  3/17] WORKDIR /app
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#26 CACHED
#27 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#27 CACHED
#28 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#28 CACHED
#29 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server  4/17] COPY src /app/src
#30 CACHED
#31 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#33 CACHED
#34 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#34 CACHED
#35 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [mcp-server] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#38 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#38 exporting attestation manifest sha256:63f5b3bf4d93da11638cb6a5958805840d90c9a659c87b1930d8e23244a0d147
#38 exporting attestation manifest sha256:63f5b3bf4d93da11638cb6a5958805840d90c9a659c87b1930d8e23244a0d147 0.1s done
#38 exporting manifest list sha256:6c5e4672608eca6ee1bfe99cad00df5fe8b17b5c26f59dd21e071e0e25d7dad7 0.0s done
#38 naming to docker.io/library/ndlss-memory-mcp-server:latest
#38 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#38 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#38 DONE 0.2s
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#39 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#39 exporting attestation manifest sha256:880e5743f0520d0a8bc11f55de1a8a3600c488262d707c6d8261e6ca42d29338 0.1s done
#39 exporting manifest list sha256:bc94b039cb381ea135523429d0811b4a54a1047ec60aadeb623b13598f450207 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   14 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         14 seconds ago   Up 14 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-5714994a67cb4b6982ba87666295b274 container=/workspace/tests/fixtures/delta-runtime-5714994a67cb4b6982ba87666295b274
US1 delta changed-only completed. run=ce3343f3fb534d04a03a6ed635c2f622
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-e604bf6bb24d4efca9d162590d9453f8 container=/workspace/tests/fixtures/delta-runtime-e604bf6bb24d4efca9d162590d9453f8
US2 delta delete+rename completed. run=4685c41410ec4ec680236c6c18034cd9
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-eddd21123faa466bbaaaf9442e62418b container=/workspace/tests/fixtures/delta-runtime-eddd21123faa466bbaaaf9442e62418b
US3 delta fallback completed. run=a8989f94e4d840f1ac2f66127e186be0 reason=BASE_REF_NOT_FOUND
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
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 697B 0.0s done
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
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 9.62kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#12 CACHED
#13 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#13 CACHED
#14 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server  3/17] WORKDIR /app
#16 CACHED
#17 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#19 CACHED
#20 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#20 CACHED
#21 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#22 CACHED
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  4/17] COPY src /app/src
#26 CACHED
#27 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#27 CACHED
#28 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  3/11] WORKDIR /app
#31 CACHED
#32 [file-indexer  9/11] COPY src /app/src
#32 CACHED
#33 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#33 CACHED
#34 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#34 CACHED
#35 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#38 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#38 exporting attestation manifest sha256:860540afd00557d708ebc99c9d7ec06e8746e2f4f177f38c67d86d8fd722079d 0.1s done
#38 exporting manifest list sha256:db2a7a517b21f696bc5092bb1a4eb5cc9dc151dddb0b4a44162f790448d41cb6
#38 exporting manifest list sha256:db2a7a517b21f696bc5092bb1a4eb5cc9dc151dddb0b4a44162f790448d41cb6 0.0s done
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#39 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#39 exporting attestation manifest sha256:2e489d9fd97be3080f687014e2bae304058cf2a4b8e4f58e6112d94864a93f57 0.1s done
#39 exporting manifest list sha256:2561b00b532d64ffc9924319e77133db34d36c6ff1a26c7bd8eea3cc4a446fa0 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   14 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US1 deterministic chunking scenario finished for runId=e0cacab92e2b40ae97b79199f8bfdd9c
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US2 retry+upsert scenario finished for runId=fdfa33535d6e44b59d702a18a31ec323 retryCount=0
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=89b6377e9bac43dd9c45cde3973a8be3 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US3 metadata traceability scenario finished for runId=d76639252fb34ab9937b11b2cf5e1420
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
[quality] stage 'integration' passed in 253923ms
[quality] stage 'us2' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 697B done
#3 DONE 0.0s
#4 [auth] library/alpine:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/python:pull token for registry-1.docker.io
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
#10 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#12 [file-indexer internal] load build context
#12 transferring context: 5.50kB done
#12 DONE 0.0s
#13 [mcp-server internal] load build context
#13 transferring context: 9.62kB done
#13 DONE 0.0s
#14 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#14 CACHED
#15 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#17 CACHED
#18 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#18 CACHED
#19 [file-indexer  9/11] COPY src /app/src
#19 CACHED
#20 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#20 CACHED
#21 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#21 CACHED
#22 [file-indexer  3/11] WORKDIR /app
#22 CACHED
#23 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#23 CACHED
#24 [mcp-server  3/17] WORKDIR /app
#24 CACHED
#25 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#26 CACHED
#27 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#28 CACHED
#29 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#29 CACHED
#30 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#30 CACHED
#31 [mcp-server  4/17] COPY src /app/src
#31 CACHED
#32 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#32 CACHED
#33 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#33 CACHED
#34 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#34 CACHED
#35 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#35 CACHED
#36 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#37 CACHED
#38 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#38 CACHED
#39 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#39 CACHED
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#40 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#40 exporting attestation manifest sha256:97a4090816bb433b2ab217d0245681682d235e5339ec83572c7cc4f6d999935b
#40 exporting attestation manifest sha256:97a4090816bb433b2ab217d0245681682d235e5339ec83572c7cc4f6d999935b 0.1s done
#40 exporting manifest list sha256:cea3c08471c1dac7a4e001278c8a4d25a494a99489cdc64d7a84ddaca4f57218
#40 exporting manifest list sha256:cea3c08471c1dac7a4e001278c8a4d25a494a99489cdc64d7a84ddaca4f57218 0.0s done
#40 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#40 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#40 DONE 0.2s
#41 [file-indexer] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#41 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#41 exporting attestation manifest sha256:3b4aafdb318e3bf3e382dc1620e1c29e16cea03300056259648423cc8d3560db 0.1s done
#41 exporting manifest list sha256:3fe33d0211c4b855fac6f362b5ce35f65508b38f5aae89a6443938ae81a96b4c 0.0s done
#41 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#41 DONE 0.2s
#42 [file-indexer] resolving provenance for metadata file
#42 DONE 0.0s
#43 [mcp-server] resolving provenance for metadata file
#43 DONE 0.0s
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
US2 search flow completed. ingestionRunId=960654b0c91c4e9d80d7f4bac697472c results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
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
[quality] stage 'us2' passed in 22910ms
[quality] stage 'us2_custom_port' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB 0.0s done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 697B done
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
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 9.62kB 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#12 CACHED
#13 [file-indexer  9/11] COPY src /app/src
#13 CACHED
#14 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#15 CACHED
#16 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#16 CACHED
#17 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#17 CACHED
#18 [file-indexer  3/11] WORKDIR /app
#18 CACHED
#19 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#22 CACHED
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#24 CACHED
#25 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#25 CACHED
#26 [mcp-server  3/17] WORKDIR /app
#26 CACHED
#27 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#31 CACHED
#32 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#32 CACHED
#33 [mcp-server  4/17] COPY src /app/src
#33 CACHED
#34 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#34 CACHED
#35 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#35 CACHED
#36 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [mcp-server] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#38 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#38 exporting attestation manifest sha256:7e7389e4c6b6bd4b41b8a4339b9158126a1ca6e22003125add6bb07e8449a01a
#38 exporting attestation manifest sha256:7e7389e4c6b6bd4b41b8a4339b9158126a1ca6e22003125add6bb07e8449a01a 0.1s done
#38 exporting manifest list sha256:2b00905aa9dbdbaa92c367f68f276c523901f2d78c848a06aa2de9bcc4e1d082
#38 exporting manifest list sha256:2b00905aa9dbdbaa92c367f68f276c523901f2d78c848a06aa2de9bcc4e1d082 0.0s done
#38 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#38 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#38 DONE 0.3s
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#39 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#39 exporting attestation manifest sha256:3a5269117e3318f252957e397a6ec3c45029976a083f451fa0f81c042144be21 0.1s done
#39 exporting manifest list sha256:d32081fab7d6efe509b5182ef36b4633528ac065811e99d874fe3242e3ba4ddd 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
US2 custom external port scenario passed. runId=87238b594c5c490d84bb9d41c039e78e artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us2_custom_port' passed in 22346ms
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 61ms
[quality] stage 'mcp_transport' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 697B done
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
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 9.62kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#12 CACHED
#13 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#13 CACHED
#14 [mcp-server  4/17] COPY src /app/src
#14 CACHED
#15 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#15 CACHED
#16 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#16 CACHED
#17 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#17 CACHED
#18 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#20 CACHED
#21 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#21 CACHED
#22 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#22 CACHED
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#25 CACHED
#26 [mcp-server  3/17] WORKDIR /app
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#28 CACHED
#29 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#29 CACHED
#30 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#30 CACHED
#31 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#32 CACHED
#33 [file-indexer  3/11] WORKDIR /app
#33 CACHED
#34 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [file-indexer  9/11] COPY src /app/src
#35 CACHED
#36 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#36 CACHED
#37 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [file-indexer] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#38 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#38 exporting attestation manifest sha256:6a6addc7dfe5d6f477d7d561641bef6692028880e78eb78abb6b2070d9dad0bf 0.1s done
#38 exporting manifest list sha256:310b9ba1adfdf87020698ca93acf4d7a496a745d3cf7009327ac2d13bbd505b6
#38 exporting manifest list sha256:310b9ba1adfdf87020698ca93acf4d7a496a745d3cf7009327ac2d13bbd505b6 0.0s done
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#39 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 0.0s done
#39 exporting attestation manifest sha256:f72dc493b255009ac5d78c8b6ced3f8bb5c48d8f99b4da9a3ab528a53953ba80 0.1s done
#39 exporting manifest list sha256:263cc806c4468ac4ae212dc667ddd82adbf86785d89a80eeb4ae7ae190c6a7b5 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.3s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
[quality] stage 'mcp_transport' passed in 27988ms
[quality] stage 'us3' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 697B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.3s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.4s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#8 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#8 DONE 0.0s
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 9.62kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#12 CACHED
#13 [mcp-server  3/17] WORKDIR /app
#13 CACHED
#14 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#15 CACHED
#16 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#16 CACHED
#17 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#18 CACHED
#19 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#19 CACHED
#20 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#20 CACHED
#21 [mcp-server  4/17] COPY src /app/src
#21 CACHED
#22 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#24 CACHED
#25 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#29 CACHED
#30 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  9/11] COPY src /app/src
#31 CACHED
#32 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#32 CACHED
#33 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#33 CACHED
#34 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#34 CACHED
#35 [file-indexer  3/11] WORKDIR /app
#35 CACHED
#36 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#36 CACHED
#37 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [file-indexer] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#38 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#38 exporting attestation manifest sha256:e15de9d212e881b917f92a2b48d851d3f21dcdbb8702d56d32911a5de73e03d3
#38 exporting attestation manifest sha256:e15de9d212e881b917f92a2b48d851d3f21dcdbb8702d56d32911a5de73e03d3 0.1s done
#38 exporting manifest list sha256:e5171bb381a15841a0140c119cf21405e12585a24f78e74232a14a1f9e15027a
#38 exporting manifest list sha256:e5171bb381a15841a0140c119cf21405e12585a24f78e74232a14a1f9e15027a 0.0s done
#38 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#38 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#38 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#39 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 done
#39 exporting attestation manifest sha256:86445a700ef591adb8de1357b9a5f7e7568c68b674d4e0cd73ab69869b1f6223 0.1s done
#39 exporting manifest list sha256:e08525797be4a72f5045aa0791984f74321caa71fd24d94ea9535d6bd3d64766 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-1dcfc5cd4ef54c3aa0aaccaea5533e56 container=/workspace/tests/fixtures/delta-runtime-1dcfc5cd4ef54c3aa0aaccaea5533e56
US1 delta changed-only completed. run=3c8d50bca4ed4f75937dd98d4d907f0a
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=45b4d45a1dd24617a19bf995a5f496e4 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US1 ingestion collection creation passed. runId=fea1bc4ab3794cbc80f5dc8bf556c20a points=7 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-6dfb206b83f94724beb28055e2a97358 container=/workspace/tests/fixtures/idempotency-runtime-6dfb206b83f94724beb28055e2a97358
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=f9eee8ba42d342829f33f1c82c6a6a54
[US1] runId=f9eee8ba42d342829f33f1c82c6a6a54 status=running attempt=1/120
[US1] runId=f9eee8ba42d342829f33f1c82c6a6a54 status=completed attempt=2/120
[US1] runId=f9eee8ba42d342829f33f1c82c6a6a54 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=5951adca3fa54b4eba7e37da998978b1
[US1] runId=5951adca3fa54b4eba7e37da998978b1 status=running attempt=1/120
[US1] runId=5951adca3fa54b4eba7e37da998978b1 status=completed attempt=2/120
[US1] runId=5951adca3fa54b4eba7e37da998978b1 finished status=completed
US1 repeat-run completed. run1=f9eee8ba42d342829f33f1c82c6a6a54 run2=5951adca3fa54b4eba7e37da998978b1 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-2f3ef4a9af9f424fb99fd6dcd2213741 container=/workspace/tests/fixtures/idempotency-runtime-2f3ef4a9af9f424fb99fd6dcd2213741
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=809e6da538564fcab2ffcc82ccbce15e
[US1] runId=809e6da538564fcab2ffcc82ccbce15e status=running attempt=1/120
[US1] runId=809e6da538564fcab2ffcc82ccbce15e status=completed attempt=2/120
[US1] runId=809e6da538564fcab2ffcc82ccbce15e finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=b685a019e27646a0badbf2f14d660244
[US1] runId=b685a019e27646a0badbf2f14d660244 status=running attempt=1/120
[US1] runId=b685a019e27646a0badbf2f14d660244 status=completed attempt=2/120
[US1] runId=b685a019e27646a0badbf2f14d660244 finished status=completed
US1 repeat-run completed. run1=809e6da538564fcab2ffcc82ccbce15e run2=b685a019e27646a0badbf2f14d660244 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
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
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 1.27kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 697B done
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
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 9.62kB done
#11 DONE 0.0s
#12 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#13 CACHED
#14 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#16 CACHED
#17 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#17 CACHED
#18 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#19 CACHED
#20 [mcp-server  4/17] COPY src /app/src
#20 CACHED
#21 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server  3/17] WORKDIR /app
#22 CACHED
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#24 CACHED
#25 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  9/11] COPY src /app/src
#28 CACHED
#29 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#29 CACHED
#30 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#31 CACHED
#32 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#32 CACHED
#33 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#33 CACHED
#34 [file-indexer  3/11] WORKDIR /app
#34 CACHED
#35 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#37 CACHED
#38 [mcp-server] exporting to image
#38 exporting layers done
#38 exporting manifest sha256:f7184e455899dc9c6e1fd292ac8fa03c86c0cb5bd0ab639fbea834143dcd957f done
#38 exporting config sha256:46326d116ac966a418665267edac527b7297dce2b1efae60e98d7cb1a29ad855 done
#38 exporting attestation manifest sha256:8f5efc39d7021ff08d79c46945f88c9cf10b7a5be3285112d75faf3309edc65e 0.1s done
#38 exporting manifest list sha256:a54e07c3c032fa18055c014d58790fb88e40cff36425dba751ef52f85afae6d5
#38 exporting manifest list sha256:a54e07c3c032fa18055c014d58790fb88e40cff36425dba751ef52f85afae6d5 0.0s done
#38 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#38 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#38 DONE 0.2s
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:08e799439c5f7181920c51843b4be3fbbaf628afea7763382961001c75c24b8b done
#39 exporting config sha256:b00c0394e33076ef1a3cb3815c04739672fbd1929b345bfe8e68afbc351cfcaf done
#39 exporting attestation manifest sha256:8182171e814525b331213972f319674b5ee7a2e96c0b014f75f30fad48e859c0 0.1s done
#39 exporting manifest list sha256:9229d04afa701b598f870eb8dba93b892f8f45a2d8d5c5beb1d024f55492b66f 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] resolving provenance for metadata file
#40 DONE 0.0s
#41 [mcp-server] resolving provenance for metadata file
#41 DONE 0.0s
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
US2 custom external port scenario passed. runId=1675f7c0e9064c2482709b77f14c56d1 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us3' passed in 53478ms
Quality run passed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-22T14:18:30.4891802+03:00
- exitCode: 0
