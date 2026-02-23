# Quality Stability Run

- startedAt: 2026-02-23T03:16:03.8304269+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 107 items
tests\unit\file_indexer\test_chunk_identity.py ...                       [  2%]
tests\unit\file_indexer\test_chunker.py .....                            [  7%]
tests\unit\file_indexer\test_docs_index_selection.py .                   [  8%]
tests\unit\file_indexer\test_embedding_retry.py ..                       [ 10%]
tests\unit\file_indexer\test_file_filters.py .....                       [ 14%]
tests\unit\file_indexer\test_file_fingerprint.py .....                   [ 19%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_config.py . [ 20%]
..                                                                       [ 22%]
tests\unit\file_indexer\test_file_indexer_vector_upsert_repository_resilience.py . [ 23%]
.                                                                        [ 24%]
tests\unit\file_indexer\test_git_diff_reader.py ..                       [ 26%]
tests\unit\file_indexer\test_run_limits_selection.py ..                  [ 28%]
tests\unit\mcp_server\test_bootstrap_collection_service.py ...           [ 30%]
tests\unit\mcp_server\test_bootstrap_orchestrator.py ...                 [ 33%]
tests\unit\mcp_server\test_bootstrap_state.py ...                        [ 36%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 38%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 40%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 42%]
tests\unit\mcp_server\test_mcp_docs_search_tool.py ...                   [ 44%]
tests\unit\mcp_server\test_mcp_tool_adapters_search.py ...               [ 47%]
tests\unit\mcp_server\test_mcp_tool_registry.py ..                       [ 49%]
tests\unit\mcp_server\test_mcp_transport_concurrency.py .                [ 50%]
tests\unit\mcp_server\test_mcp_transport_error_mapper.py ...             [ 53%]
tests\unit\mcp_server\test_mcp_transport_handshake.py ....               [ 57%]
tests\unit\mcp_server\test_mcp_transport_negative_cases.py ...           [ 59%]
tests\unit\mcp_server\test_mcp_transport_protocol_models.py ....         [ 63%]
tests\unit\mcp_server\test_mcp_transport_session_state.py ..             [ 65%]
tests\unit\mcp_server\test_root_commands_endpoint.py ..                  [ 67%]
tests\unit\mcp_server\test_search_repository_docs.py .                   [ 68%]
tests\unit\mcp_server\test_search_repository_missing_collection.py ..... [ 72%]
                                                                         [ 72%]
tests\unit\mcp_server\test_search_result_resolution.py ....              [ 76%]
tests\unit\mcp_server\test_semantic_search_filters.py ..                 [ 78%]
tests\unit\mcp_server\test_semantic_search_service.py ..                 [ 80%]
tests\unit\mcp_server\test_startup_preflight_checks.py ....              [ 84%]
tests\unit\mcp_server\test_startup_preflight_models.py ...               [ 86%]
tests\unit\mcp_server\test_startup_readiness_endpoint.py ..              [ 88%]
tests\unit\mcp_server\test_startup_readiness_summary.py .                [ 89%]
tests\unit\mcp_server\test_vector_upsert_repository_config.py ...        [ 92%]
tests\unit\mcp_server\test_vector_upsert_repository_resilience.py ..     [ 94%]
tests\unit\mcp_server\test_watch_mode_retry_policy.py ...                [ 97%]
tests\unit\mcp_server\test_watch_mode_state.py ...                       [100%]
============================= 107 passed in 1.18s =============================
[quality] stage 'unit' passed in 2175ms
[quality] stage 'us1' started
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
#5 DONE 0.6s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.7s
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
#10 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#10 CACHED
#11 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#11 CACHED
#12 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#12 CACHED
#13 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#13 CACHED
#14 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#14 CACHED
#15 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#15 CACHED
#16 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#16 CACHED
#17 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  3/12] WORKDIR /app
#18 CACHED
#19 [file-indexer 10/12] COPY src /app/src
#19 CACHED
#20 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#20 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#20 DONE 0.0s
#21 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#21 CACHED
#22 [mcp-server internal] load build context
#22 transferring context: 11.46kB done
#22 DONE 0.0s
#23 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server  4/17] COPY src /app/src
#26 CACHED
#27 [mcp-server  3/17] WORKDIR /app
#27 CACHED
#28 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#28 CACHED
#29 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#30 CACHED
#31 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#32 CACHED
#33 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#33 CACHED
#34 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#34 CACHED
#35 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#36 CACHED
#37 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:c4fcba6f7c4551a053e16ba15a54cdfb170c41ba7f267cabcd29517f307b1291 0.1s done
#40 exporting manifest list sha256:21449e498fed7e128cdf10cef55c154d6edc126748b75fd017b80b3c61164aba 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting attestation manifest sha256:1febefabb274ccc63a84bda73c8fa478fbc849f385bf91cb3a8526be8a8e82a1 0.1s done
#39 exporting manifest list sha256:06b1f61f925f03515cf47b7abd707ec05fc09d40349a3f21857060222d281faf
#39 exporting manifest list sha256:06b1f61f925f03515cf47b7abd707ec05fc09d40349a3f21857060222d281faf 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   15 seconds ago   Up 9 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 15 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-be1423eb7ba442ad93eb813bb8d8c85f container=/workspace/tests/fixtures/idempotency-runtime-be1423eb7ba442ad93eb813bb8d8c85f
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=179c5918c0cc49a0a8180027e65c8276
[US1] runId=179c5918c0cc49a0a8180027e65c8276 status=running attempt=1/120
[US1] runId=179c5918c0cc49a0a8180027e65c8276 status=completed attempt=3/120
[US1] runId=179c5918c0cc49a0a8180027e65c8276 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=467fcad5fc4a4297be748b50f9765038
[US1] runId=467fcad5fc4a4297be748b50f9765038 status=running attempt=1/120
[US1] runId=467fcad5fc4a4297be748b50f9765038 status=completed attempt=2/120
[US1] runId=467fcad5fc4a4297be748b50f9765038 finished status=completed
US1 repeat-run completed. run1=179c5918c0cc49a0a8180027e65c8276 run2=467fcad5fc4a4297be748b50f9765038 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-a7626ba8455847a49d2d576790082eb5 container=/workspace/tests/fixtures/idempotency-runtime-a7626ba8455847a49d2d576790082eb5
US2 deterministic update completed. run1=f5e0330e54ef4e3195d18bbf83b632d5 run2=22412833c955452cb395a21da1caa1bd
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-5306a72e6f36487cb09a883758dda77e container=/workspace/tests/fixtures/idempotency-runtime-5306a72e6f36487cb09a883758dda77e
US3 stale cleanup completed. run2=df5bcffa3b9d48fc8f3fcb44a282732e
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
[quality] stage 'us1' passed in 28212ms
[quality] stage 'us1_persistence' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [auth] library/alpine:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/python:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 0.7s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 0.7s
#8 [mcp-server internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [file-indexer internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 DONE 0.0s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#12 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#12 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#12 DONE 0.0s
#13 [mcp-server internal] load build context
#13 transferring context: 11.46kB 0.0s done
#13 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#14 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#14 CACHED
#15 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#15 CACHED
#16 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#16 CACHED
#17 [mcp-server  3/17] WORKDIR /app
#17 CACHED
#18 [mcp-server  4/17] COPY src /app/src
#18 CACHED
#19 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#19 CACHED
#20 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#20 CACHED
#21 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#21 CACHED
#22 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#22 CACHED
#23 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#27 CACHED
#28 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#28 CACHED
#29 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#29 CACHED
#30 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#30 CACHED
#31 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#31 CACHED
#32 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#32 CACHED
#33 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#33 CACHED
#34 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#34 CACHED
#35 [file-indexer  3/12] WORKDIR /app
#35 CACHED
#36 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#36 CACHED
#37 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#37 CACHED
#38 [file-indexer 10/12] COPY src /app/src
#38 CACHED
#39 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#39 CACHED
#40 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#40 CACHED
#41 [mcp-server] exporting to image
#41 exporting layers done
#41 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#41 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#41 exporting attestation manifest sha256:071d2fd486df368a6af750147763c0e770284ef46aa43dcc38517c9716f11e8f
#41 exporting attestation manifest sha256:071d2fd486df368a6af750147763c0e770284ef46aa43dcc38517c9716f11e8f 0.1s done
#41 exporting manifest list sha256:4fa179620356a93297a62df225be8ae947d222783fc57c155529d957d86ee5f2
#41 exporting manifest list sha256:4fa179620356a93297a62df225be8ae947d222783fc57c155529d957d86ee5f2 0.0s done
#41 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#41 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#41 DONE 0.3s
#42 [file-indexer] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#42 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#42 exporting attestation manifest sha256:50d09e40e56e9d1e778d5601da500b45073275c9d51732c1fce8105cf27c0738 0.1s done
#42 exporting manifest list sha256:e9598971d2119ca4bc1af6a98d487f9abf78793f1938c9bd9f70db3a1192ca52 0.0s done
#42 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#42 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
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
US1 ingestion collection creation passed. runId=dd33ea24678e449bac02b1fefc97ca9a points=15 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
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
[quality] stage 'us1_persistence' passed in 30144ms
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
#11 transferring context: 11.46kB done
#11 DONE 0.0s
#12 [file-indexer  3/12] WORKDIR /app
#12 CACHED
#13 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#13 CACHED
#14 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#15 CACHED
#16 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#16 CACHED
#17 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#18 CACHED
#19 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#19 CACHED
#20 [file-indexer 10/12] COPY src /app/src
#20 CACHED
#21 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  4/17] COPY src /app/src
#23 CACHED
#24 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#25 CACHED
#26 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#27 CACHED
#28 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#28 CACHED
#29 [mcp-server  3/17] WORKDIR /app
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#31 CACHED
#32 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#32 CACHED
#33 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#33 CACHED
#34 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#34 CACHED
#35 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#35 CACHED
#36 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 done
#39 exporting attestation manifest sha256:2f12e6338bfcd69c89451ce34794b9df20a4be7aa121ac4f85ac5e0bb31fdd88 0.1s done
#39 exporting manifest list sha256:a9ab3c13e2b1dca23a88a99687307120b77a7b0df7b27d31a504332c60d2885d
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:7cd46006dd18f110740df69c0f1d3a817a8f73f2c2dd1e254b441e3aa126a0ca 0.1s done
#40 exporting manifest list sha256:4550cbdf9c73030830809fdd05c025aea15b44ed2b350945ce8693d129c4bd7f 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 0.2s
#39 [mcp-server] exporting to image
#39 exporting manifest list sha256:a9ab3c13e2b1dca23a88a99687307120b77a7b0df7b27d31a504332c60d2885d 0.0s done
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
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.6s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.6s
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
#10 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.46kB done
#11 DONE 0.0s
#12 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#12 CACHED
#13 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#13 CACHED
#14 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#14 CACHED
#15 [mcp-server  3/17] WORKDIR /app
#15 CACHED
#16 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#16 CACHED
#17 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#17 CACHED
#18 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#20 CACHED
#21 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#21 CACHED
#22 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#22 CACHED
#23 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#24 CACHED
#25 [mcp-server  4/17] COPY src /app/src
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB done
#8 DONE 0.0s
#28 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#28 CACHED
#29 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#29 CACHED
#30 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#30 CACHED
#31 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#31 CACHED
#32 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#32 CACHED
#33 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#33 CACHED
#34 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#35 CACHED
#36 [file-indexer 10/12] COPY src /app/src
#36 CACHED
#37 [file-indexer  3/12] WORKDIR /app
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 done
#39 exporting attestation manifest sha256:5dc9de403141de1b43bc0c1d81ac03d4269079b008b27ec0df695c2c7cfc4766 0.1s done
#39 exporting manifest list sha256:f372d64195a3cca197f310d9443021238efae532528532d492d0f067e7798ed8
#39 exporting manifest list sha256:f372d64195a3cca197f310d9443021238efae532528532d492d0f067e7798ed8 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:76a206e736c4431fad5308b425ae13507d046f509620b39c7c1d6c542608475b 0.1s done
#40 exporting manifest list sha256:24c6f7083c3ee25b1dbf39270f83d11bb5c8b82c23b8ed321a198f1814262ea3 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest
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
#2 transferring dockerfile: 800B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 1.27kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.6s
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.6s
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
#10 transferring context: 11.46kB 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [file-indexer 10/12] COPY src /app/src
#12 CACHED
#13 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#14 CACHED
#15 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#15 CACHED
#16 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#17 CACHED
#18 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#18 CACHED
#19 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#22 CACHED
#23 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#24 CACHED
#25 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#27 CACHED
#28 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#28 CACHED
#29 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#30 CACHED
#31 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#31 CACHED
#32 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#32 CACHED
#33 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#33 CACHED
#34 [mcp-server  3/17] WORKDIR /app
#34 CACHED
#35 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#35 CACHED
#36 [mcp-server  4/17] COPY src /app/src
#36 CACHED
#37 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#39 exporting attestation manifest sha256:1883e80d4007c064255ed2c422f81ae719f77c3527a9b1eae66c4cf3da574080
#39 exporting attestation manifest sha256:1883e80d4007c064255ed2c422f81ae719f77c3527a9b1eae66c4cf3da574080 0.1s done
#39 exporting manifest list sha256:fb1690ae616b4c7b008ea26b5f93142d4111537928012d9736e9ededff748203 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:928c4a1e855d18063fae29e2edb29f2a3c9da780bee0bf8d39e544e3f1a84897 0.1s done
#40 exporting manifest list sha256:6dcb4e6578fc520e4c428905ecab12b7dd5986d2f1b6659886ed2b62496d4d8c 0.0s done
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   14 seconds ago   Up 8 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     14 seconds ago   Up 2 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         14 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-23392b0ef89a4fefa1b295bdcc16aba1 container=/workspace/tests/fixtures/delta-runtime-23392b0ef89a4fefa1b295bdcc16aba1
US1 delta changed-only completed. run=024b143960014560905632a1cf343d68
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-eb0bd4bc2ecd4d2fb3f697990df35bfc container=/workspace/tests/fixtures/delta-runtime-eb0bd4bc2ecd4d2fb3f697990df35bfc
US2 delta delete+rename completed. run=8ef0322c57fa497589cfe9e49574184f
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-08be6fe4e2e349a494c3a0c78674b185 container=/workspace/tests/fixtures/delta-runtime-08be6fe4e2e349a494c3a0c78674b185
US3 delta fallback completed. run=359c9a94a45443fe8c1659c12f5a03d5 reason=BASE_REF_NOT_FOUND
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
#8 [file-indexer internal] load build context
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 DONE 0.0s
#10 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.1s done
#10 DONE 0.1s
#11 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.1s done
#11 DONE 0.1s
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB done
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 transferring context: 11.46kB done
#9 DONE 0.0s
#12 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#12 CACHED
#13 [file-indexer 10/12] COPY src /app/src
#13 CACHED
#14 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#14 CACHED
#15 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#15 CACHED
#16 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#16 CACHED
#17 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#18 CACHED
#19 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#23 CACHED
#24 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#24 CACHED
#25 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#28 CACHED
#29 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#29 CACHED
#30 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#30 CACHED
#31 [mcp-server  3/17] WORKDIR /app
#31 CACHED
#32 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#32 CACHED
#33 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#33 CACHED
#34 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#34 CACHED
#35 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#35 CACHED
#36 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server  4/17] COPY src /app/src
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 done
#39 exporting attestation manifest sha256:24a945c1408183aa1e9cdfa44afbec47b0c17219c753e154062aec746f20c3f4
#39 exporting attestation manifest sha256:24a945c1408183aa1e9cdfa44afbec47b0c17219c753e154062aec746f20c3f4 0.1s done
#39 exporting manifest list sha256:d689f75c60fe551c7178feb10d246163a395e2093b694636c01e7621950e8d19 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:0033b7ea46df66641163361c6b5b8d76597214309bec5ad5ccd61d584c08bfe8 0.1s done
#40 exporting manifest list sha256:28b65e97434d5fc737f86524100dfd4f0da647021f71e2713f7c3acf6dad8753 0.0s done
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
NAME                        IMAGE                       COMMAND                  SERVICE        CREATED          STATUS                            PORTS
ndlss-memory-file-indexer   ndlss-memory-file-indexer   "/app/scripts/entrypвЂ¦"   file-indexer   16 seconds ago   Up 9 seconds (healthy)            
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:18080->18080/tcp, [::]:18080->18080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         18 seconds ago   Up 14 seconds (healthy)           0.0.0.0:16333->6333/tcp, [::]:16333->6333/tcp
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US1 deterministic chunking scenario finished for runId=ac3a826cbd534f06a780113deed6000d
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US2 retry+upsert scenario finished for runId=5e834b0104e04dd4812eab7accb5068f retryCount=1
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=180e538a6c0e490c8ad7989569751ffa results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US3 metadata traceability scenario finished for runId=c6c3377a57cd401bbccc69c225916e00
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
[quality] stage 'integration' passed in 313273ms
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
#4 [auth] library/alpine:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/python:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 1.0s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 ...
#8 [mcp-server internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [mcp-server  4/17] COPY src /app/src
#11 CACHED
#12 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#12 CACHED
#13 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#13 CACHED
#14 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#16 CACHED
#17 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#17 CACHED
#18 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#19 CACHED
#20 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#20 CACHED
#21 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#21 CACHED
#22 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#22 CACHED
#23 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#23 CACHED
#24 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server  3/17] WORKDIR /app
#25 CACHED
#26 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#26 CACHED
#27 [mcp-server] exporting to image
#27 exporting layers done
#27 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#27 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 done
#27 exporting attestation manifest sha256:600f8c22a17efd5bb58a502d59a4b50fb9132ed5270652f17e52d6f0cf804873 0.0s done
#27 exporting manifest list sha256:85ae28b6d8d1726fb3912fd677f50d9c1a36e2853afaf5f118d12c5182ae23f0 0.0s done
#27 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#27 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#27 DONE 0.1s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 1.3s
#28 [file-indexer internal] load .dockerignore
#28 transferring context: 2B done
#28 DONE 0.0s
#29 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#29 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#29 DONE 0.0s
#30 [file-indexer internal] load build context
#30 transferring context: 5.55kB done
#30 DONE 0.0s
#31 [file-indexer  3/12] WORKDIR /app
#31 CACHED
#32 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#32 CACHED
#33 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#33 CACHED
#34 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#34 CACHED
#35 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#35 CACHED
#36 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [file-indexer 10/12] COPY src /app/src
#37 CACHED
#38 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#38 CACHED
#39 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#39 CACHED
#40 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#40 CACHED
#41 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#41 CACHED
#42 [file-indexer] exporting to image
#42 exporting layers done
#42 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#42 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#42 exporting attestation manifest sha256:817d4c0d7bd3764fc94e286c598c2ddd81bb8b660de5e71cd7b442b067da4bd2 0.0s done
#42 exporting manifest list sha256:fd5cb02c4886d49cdf99a775ceb47b2a5df9572441375f01d2ec4521d8c104f4 0.0s done
#42 naming to docker.io/library/ndlss-memory-file-indexer:latest
#42 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#42 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#42 DONE 0.1s
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
 Container ndlss-memory-qdrant  Waiting
 Container ndlss-memory-file-indexer  Waiting
 Container ndlss-memory-qdrant  Healthy
 Container ndlss-memory-file-indexer  Healthy
 Container ndlss-memory-mcp-server  Starting
 Container ndlss-memory-mcp-server  Started
US2 search flow completed. ingestionRunId=a6d647f2c44a4fe7a5192abf01c1f9bc results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
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
[quality] stage 'us2' passed in 23415ms
[quality] stage 'us2_custom_port' started
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
#5 DONE 0.3s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.3s
#6 [mcp-server internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [file-indexer internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer internal] load build context
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 DONE 0.0s
#10 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 2.4s done
#10 DONE 2.4s
#11 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 1.9s done
#11 DONE 2.5s
#9 [mcp-server internal] load build context
#9 transferring context: 11.46kB done
#9 DONE 1.2s
#8 [file-indexer internal] load build context
#8 transferring context: 5.55kB 0.0s done
#8 DONE 1.1s
#12 [file-indexer 10/12] COPY src /app/src
#12 CACHED
#13 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#13 CACHED
#14 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#15 CACHED
#16 [file-indexer  3/12] WORKDIR /app
#16 CACHED
#17 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#19 CACHED
#20 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#20 CACHED
#21 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 ...
#23 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#23 CACHED
#24 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#24 CACHED
#25 [mcp-server  4/17] COPY src /app/src
#25 CACHED
#26 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#27 CACHED
#28 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#28 CACHED
#29 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#29 CACHED
#30 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#30 CACHED
#31 [mcp-server  3/17] WORKDIR /app
#31 CACHED
#32 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#32 CACHED
#33 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#33 CACHED
#34 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#34 CACHED
#35 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#35 CACHED
#36 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#36 CACHED
#37 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#37 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers 0.0s done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 1.0s done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 1.0s done
#39 exporting attestation manifest sha256:d09081897067f18a298216bd3cb12a1f34b612e65e04ee1ae216a8295a0ef920 0.1s done
#39 exporting manifest list sha256:80ae1604509839f7e3a2838361059f74a92aabf1a7cb6334af5e8cab6aa7cb59
#39 ...
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 1.3s done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 0.1s done
#40 exporting attestation manifest sha256:ce89ef0e5b8f66ed153d177618b3896c0d59668112f6eb5e3cbe440e477e8221 0.1s done
#40 exporting manifest list sha256:2eb0394b77dfbc55b2addd302899203762bdbebdd522a857932c5d26f91b9129 0.0s done
#40 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#40 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#40 DONE 1.6s
#39 [mcp-server] exporting to image
#39 exporting manifest list sha256:80ae1604509839f7e3a2838361059f74a92aabf1a7cb6334af5e8cab6aa7cb59 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 2.3s
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
US2 custom external port scenario passed. runId=84230768480d4e63bd84af6f4f04fb13 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us2_custom_port' passed in 29275ms
[quality] stage 'startup_preflight' started
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
#8 [file-indexer  1/12] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.1s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 11.46kB done
#11 DONE 0.0s
#12 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#13 CACHED
#14 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#14 CACHED
#15 [file-indexer 10/12] COPY src /app/src
#15 CACHED
#16 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#17 CACHED
#18 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#18 CACHED
#19 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#23 CACHED
#24 [mcp-server  3/17] WORKDIR /app
#24 CACHED
#25 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#25 CACHED
#26 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#26 CACHED
#27 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#27 CACHED
#28 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#28 CACHED
#29 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#29 CACHED
#30 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#30 CACHED
#31 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#31 CACHED
#32 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#32 CACHED
#33 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#33 CACHED
#34 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#34 CACHED
#35 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#35 CACHED
#36 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#36 CACHED
#37 [mcp-server  4/17] COPY src /app/src
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#39 exporting attestation manifest sha256:6443e09427dbf94975ee4487af8e435c98f10c2b88dc133d2441333179cc89b7
#39 exporting attestation manifest sha256:6443e09427dbf94975ee4487af8e435c98f10c2b88dc133d2441333179cc89b7 0.1s done
#39 exporting manifest list sha256:e9965144177e5b3c4b85c45f66beb1dac43647d0aea6be90c9e0e38574b8cea6
#39 exporting manifest list sha256:e9965144177e5b3c4b85c45f66beb1dac43647d0aea6be90c9e0e38574b8cea6 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:ede601f9d4c1ce4cc8b0651436d5ec9a2e040c9878af65bb89e3e174eeef5bf2 0.1s done
#40 exporting manifest list sha256:d0ec03097a57662a2c9321a0459777223941679f0d5717fa71f4ab44c1635be7 0.0s done
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
[startup-preflight-smoke] ready scenario passed
{
    "bootstrap":  {
                      "checkedAt":  "2026-02-23T00:23:24.480094+00:00",
                      "collectionName":  "workspace_chunks",
                      "decision":  "skip-already-completed",
                      "reason":  "bootstrap already completed for workspace",
                      "runId":  "f0fb2b4848f04bd4a41d48cdee75194b",
                      "status":  "ready",
                      "trigger":  "auto-startup",
                      "workspaceKey":  "/workspace|c52ddf65534b7b46"
                  },
    "checkedAt":  "2026-02-23T00:23:24.483634+00:00",
    "collection":  {
                       "checkedAt":  "2026-02-23T00:23:24.480186+00:00",
                       "collectionName":  "workspace_chunks",
                       "docsCollection":  {
                                              "checkedAt":  "2026-02-23T00:23:24.480186+00:00",
                                              "collectionName":  "workspace_docs_chunks",
                                              "exists":  false,
                                              "pointCount":  0
                                          },
                       "exists":  true,
                       "pointCount":  10529
                   },
    "collectionName":  "workspace_chunks",
    "indexMode":  "full-scan",
    "mcpEndpoint":  "/mcp",
    "preflightChecks":  [
                            {
                                "checkId":  "qdrant_reachability",
                                "checkedAt":  "2026-02-23T00:23:24.476092+00:00",
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
                                "checkedAt":  "2026-02-23T00:23:24.477035+00:00",
                                "details":  {
                                                "workspacePath":  "/workspace"
                                            },
                                "message":  "Рабочая директория доступна для чтения",
                                "severity":  "critical",
                                "status":  "passed"
                            },
                            {
                                "checkId":  "git_available",
                                "checkedAt":  "2026-02-23T00:23:24.477049+00:00",
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
[quality] stage 'startup_preflight' passed in 21470ms
[quality] stage 'startup_bootstrap' started
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-cca493febfee4298b0d8cc328dc616c2 container=/workspace/tests/fixtures/idempotency-runtime-cca493febfee4298b0d8cc328dc616c2
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
#12 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#12 CACHED
#13 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#13 CACHED
#14 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#14 CACHED
#15 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#15 CACHED
#16 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#16 CACHED
#17 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#18 CACHED
#19 [file-indexer 10/12] COPY src /app/src
#19 CACHED
#20 [file-indexer  3/12] WORKDIR /app
#20 CACHED
#21 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#22 CACHED
#23 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#26 CACHED
#27 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#27 CACHED
#28 [mcp-server  3/17] WORKDIR /app
#28 CACHED
#29 [mcp-server  4/17] COPY src /app/src
#29 CACHED
#30 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#30 CACHED
#31 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#32 CACHED
#33 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#33 CACHED
#34 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#34 CACHED
#35 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#35 CACHED
#36 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#36 CACHED
#37 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#39 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#39 exporting attestation manifest sha256:3c32d11e7e99ee90e643269e7ce63beb7133d61a72d0d2069ce2b75e2695dd66 0.1s done
#39 exporting manifest list sha256:fdf0fd5212e31159993b01266d500a1de16a593007e964acae865b5bf93fdc9c
#39 exporting manifest list sha256:fdf0fd5212e31159993b01266d500a1de16a593007e964acae865b5bf93fdc9c 0.1s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#40 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#40 exporting attestation manifest sha256:8976e8b3d330749316c0ffa9c3222a5dfd55f76b7510b0bec2b6892991d31d5d 0.1s done
#40 exporting manifest list sha256:506c85eb6c8bc7a04e8b13e3a5c4c29abbc075ce22cc397597ae1cd90ce6b8c6 0.0s done
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
startup bootstrap smoke passed: collection=workspace_chunks points=10529 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\startup-bootstrap-smoke.json
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
[quality] stage 'startup_bootstrap' passed in 21523ms
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 49ms
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
#9 [mcp-server internal] load build context
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.55kB done
#10 DONE 0.0s
#11 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#11 CACHED
#12 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#12 CACHED
#13 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#13 CACHED
#14 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#15 CACHED
#16 [file-indexer  3/12] WORKDIR /app
#16 CACHED
#17 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#17 CACHED
#18 [file-indexer 10/12] COPY src /app/src
#18 CACHED
#19 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#20 CACHED
#21 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#21 CACHED
#22 [mcp-server  1/17] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#22 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#22 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#22 DONE 0.0s
#9 [mcp-server internal] load build context
#9 transferring context: 11.46kB done
#9 DONE 0.0s
#23 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#23 CACHED
#24 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#24 CACHED
#25 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#25 CACHED
#26 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#27 CACHED
#28 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#28 CACHED
#29 [mcp-server  3/17] WORKDIR /app
#29 CACHED
#30 [mcp-server  4/17] COPY src /app/src
#30 CACHED
#31 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#31 CACHED
#32 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#32 CACHED
#33 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#33 CACHED
#34 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#34 CACHED
#35 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#35 CACHED
#36 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#36 CACHED
#37 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#39 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#39 exporting attestation manifest sha256:629530b2f4ed6584df285dfdc034d42b7dc0e5ff32d7b929d2d1cc22da45d57a
#39 exporting attestation manifest sha256:629530b2f4ed6584df285dfdc034d42b7dc0e5ff32d7b929d2d1cc22da45d57a 0.1s done
#39 exporting manifest list sha256:85d9fb32f18fd512f903bbb8e040a57dd3ce42d3cd4292f1e6d2c647935b3f8f 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#40 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#40 exporting attestation manifest sha256:064b5799037c52b40b9fc6996975c1e3addff9011df2119ba45a4e31c06c597a 0.1s done
#40 exporting manifest list sha256:0ed94f0c16cf35195daff0e04e30333702e6ba373984760a5f940e8ac66bf52a 0.0s done
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
[quality] stage 'mcp_transport' passed in 21865ms
[quality] stage 'us3' started
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
#10 [mcp-server internal] load build context
#10 transferring context: 11.46kB done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.55kB done
#11 DONE 0.0s
#12 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#12 CACHED
#13 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#13 CACHED
#14 [file-indexer  3/12] WORKDIR /app
#14 CACHED
#15 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#15 CACHED
#16 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#16 CACHED
#17 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#18 CACHED
#19 [file-indexer 10/12] COPY src /app/src
#19 CACHED
#20 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#20 CACHED
#21 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#21 CACHED
#22 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#22 CACHED
#23 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#24 CACHED
#25 [mcp-server  3/17] WORKDIR /app
#25 CACHED
#26 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#27 CACHED
#28 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#28 CACHED
#29 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#29 CACHED
#30 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#30 CACHED
#31 [mcp-server  4/17] COPY src /app/src
#31 CACHED
#32 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#32 CACHED
#33 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#33 CACHED
#34 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#34 CACHED
#35 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#36 CACHED
#37 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#37 CACHED
#38 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#38 CACHED
#39 [file-indexer] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#39 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#39 exporting attestation manifest sha256:c1386ca943e001d281e6a567b9bd14f0d876e4ff9ef74f16a2635b0d73014578
#39 exporting attestation manifest sha256:c1386ca943e001d281e6a567b9bd14f0d876e4ff9ef74f16a2635b0d73014578 0.1s done
#39 exporting manifest list sha256:5e8d116ffceeae7dd2861f0af4bd68d69311eb8741456baf53b3ae67531a5c01
#39 exporting manifest list sha256:5e8d116ffceeae7dd2861f0af4bd68d69311eb8741456baf53b3ae67531a5c01 0.0s done
#39 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#39 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#39 DONE 0.2s
#40 [mcp-server] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#40 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 done
#40 exporting attestation manifest sha256:c115aa7a3f8058b02b6c89a224509615636fd75b0d9853c13bd166472aaa4e38 0.1s done
#40 exporting manifest list sha256:e949daee405ae3a79899efb5169f1a5ebdcf9a57d37517b857e357fb94f454c3 0.0s done
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
Full-scan fixture environment prepared at tests/fixtures/full-scan
US1 full scan recursive indexing check passed
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-0df1694006454ac589cb98a441adfb7a container=/workspace/tests/fixtures/delta-runtime-0df1694006454ac589cb98a441adfb7a
US1 delta changed-only completed. run=6a86e4c69d5f4e108ac5f63501d660ca
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=d18f748648c94bc59b9fc4e0b8a39b02 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US1 ingestion collection creation passed. runId=30a3338fb1be482f98cee1f0be7fd33b points=15 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-ingestion-collection-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-8323ae802486421d8cc7a9ab2dfc6db0 container=/workspace/tests/fixtures/idempotency-runtime-8323ae802486421d8cc7a9ab2dfc6db0
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=6303b057414747cdb47b59db90716bcf
[US1] runId=6303b057414747cdb47b59db90716bcf status=running attempt=1/120
[US1] runId=6303b057414747cdb47b59db90716bcf status=completed attempt=2/120
[US1] runId=6303b057414747cdb47b59db90716bcf finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=1a54487372174864a9dc7becb545f45e
[US1] runId=1a54487372174864a9dc7becb545f45e status=running attempt=1/120
[US1] runId=1a54487372174864a9dc7becb545f45e status=completed attempt=2/120
[US1] runId=1a54487372174864a9dc7becb545f45e finished status=completed
US1 repeat-run completed. run1=6303b057414747cdb47b59db90716bcf run2=1a54487372174864a9dc7becb545f45e artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-ae631aae5de642898097f76ecd87ca26 container=/workspace/tests/fixtures/idempotency-runtime-ae631aae5de642898097f76ecd87ca26
[US1] waiting for MCP health at http://localhost:18080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=fed972fda46140e2b2f94b272c39452f
[US1] runId=fed972fda46140e2b2f94b272c39452f status=running attempt=1/120
[US1] runId=fed972fda46140e2b2f94b272c39452f status=completed attempt=2/120
[US1] runId=fed972fda46140e2b2f94b272c39452f finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=253f10300fd945eea79b53a6b4e9a4c2
[US1] runId=253f10300fd945eea79b53a6b4e9a4c2 status=running attempt=1/120
[US1] runId=253f10300fd945eea79b53a6b4e9a4c2 status=completed attempt=2/120
[US1] runId=253f10300fd945eea79b53a6b4e9a4c2 finished status=completed
US1 repeat-run completed. run1=fed972fda46140e2b2f94b272c39452f run2=253f10300fd945eea79b53a6b4e9a4c2 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
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
#12 [mcp-server  3/17] WORKDIR /app
#12 CACHED
#13 [mcp-server  2/17] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#13 CACHED
#14 [mcp-server 11/17] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#14 CACHED
#15 [mcp-server 12/17] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#15 CACHED
#16 [mcp-server 14/17] COPY openapi/mcp-transport.openapi.yaml /app/openapi/mcp-transport.openapi.yaml
#16 CACHED
#17 [mcp-server  4/17] COPY src /app/src
#17 CACHED
#18 [mcp-server 10/17] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#18 CACHED
#19 [mcp-server 16/17] RUN chmod +x /app/scripts/entrypoint.sh
#19 CACHED
#20 [mcp-server  9/17] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#20 CACHED
#21 [mcp-server  6/17] COPY config/security-policy.yaml /app/config/security-policy.yaml
#21 CACHED
#22 [mcp-server 15/17] RUN sed -i 's/\r$//' /app/scripts/*.sh
#22 CACHED
#23 [mcp-server  5/17] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#23 CACHED
#24 [mcp-server  7/17] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server 13/17] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#25 CACHED
#26 [mcp-server  8/17] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#26 CACHED
#27 [mcp-server 17/17] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#27 CACHED
#28 [file-indexer  3/12] WORKDIR /app
#28 CACHED
#29 [file-indexer  9/12] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#29 CACHED
#30 [file-indexer  8/12] COPY scripts/startup-preflight.sh /app/scripts/startup-preflight.sh
#30 CACHED
#31 [file-indexer  6/12] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#31 CACHED
#32 [file-indexer  7/12] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#32 CACHED
#33 [file-indexer 11/12] RUN sed -i 's/\r$//' /app/scripts/*.sh
#33 CACHED
#34 [file-indexer  5/12] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#34 CACHED
#35 [file-indexer  2/12] RUN apk add --no-cache bash coreutils
#35 CACHED
#36 [file-indexer  4/12] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#36 CACHED
#37 [file-indexer 10/12] COPY src /app/src
#37 CACHED
#38 [file-indexer 12/12] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh /app/scripts/startup-preflight.sh
#38 CACHED
#39 [mcp-server] exporting to image
#39 exporting layers done
#39 exporting manifest sha256:2277dc55e75453682d480c77b9fb5506aa5a4f0f96da14362b80c3bdd8267593 done
#39 exporting config sha256:20b95d41b1bd006ef362a2a46cf1247609dbc1833ab628e3153f16f1a17b3333 0.0s done
#39 exporting attestation manifest sha256:361a4f10ca95ebea461bb2616819139d7d50c271ee78b5003586021e43472ff7
#39 exporting attestation manifest sha256:361a4f10ca95ebea461bb2616819139d7d50c271ee78b5003586021e43472ff7 0.1s done
#39 exporting manifest list sha256:ded521d2ad69478cd514b88ad6aaeca0e214629c7dbab6c839fb2565dd07aad5 0.0s done
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest
#39 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#39 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#39 DONE 0.2s
#40 [file-indexer] exporting to image
#40 exporting layers done
#40 exporting manifest sha256:331b0f7fb5a2cb86086ecd567bc66ea91f69c4b32af17117f9a19a59a0d95745 done
#40 exporting config sha256:2f7fa714996289b0645df108b37aaf0ca51a4a59354d2674f107718c68c82126 done
#40 exporting attestation manifest sha256:addd4d5f7784e724c0c0b39a57843c15f457d453c38d7de78f7907e9a3b137a0 0.1s done
#40 exporting manifest list sha256:50e8565807ab7381b4bb8b0ee8096a2a2e97b54e8363033f982f83af7caff6f5 0.0s done
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
US2 custom external port scenario passed. runId=a3793343a7d1481faa381a19c77a3a7e artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-custom-port-summary.json
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
[quality] stage 'us3' passed in 60597ms
Quality run passed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-23T03:25:16.0669588+03:00
- exitCode: 0
