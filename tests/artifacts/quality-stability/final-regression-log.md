# Quality Stability Run

- startedAt: 2026-02-22T03:14:39.6614714+03:00
- args: -ArtifactsDir tests/artifacts/quality-stability

[quality] stage 'unit' started
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: Z:\WORK\ndlss-memory
configfile: pytest.ini
collected 36 items
tests\unit\file_indexer\test_chunk_identity.py ...                       [  8%]
tests\unit\file_indexer\test_chunker.py .....                            [ 22%]
tests\unit\file_indexer\test_embedding_retry.py ..                       [ 27%]
tests\unit\file_indexer\test_file_filters.py .....                       [ 41%]
tests\unit\file_indexer\test_file_fingerprint.py .....                   [ 55%]
tests\unit\file_indexer\test_git_diff_reader.py ..                       [ 61%]
tests\unit\mcp_server\test_command_audit_store.py ..                     [ 66%]
tests\unit\mcp_server\test_command_execution_policy.py ..                [ 72%]
tests\unit\mcp_server\test_command_workspace_isolation.py ..             [ 77%]
tests\unit\mcp_server\test_search_result_resolution.py ....              [ 88%]
tests\unit\mcp_server\test_semantic_search_filters.py ..                 [ 94%]
tests\unit\mcp_server\test_semantic_search_service.py ..                 [100%]
============================= 36 passed in 0.73s ==============================
[quality] stage 'unit' passed in 1077ms
[quality] stage 'us1' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 2.60kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 686B done
#3 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.6s
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.6s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B 0.0s done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [file-indexer internal] load build context
#9 transferring context: 5.50kB done
#9 DONE 0.0s
#10 [file-indexer  9/11] COPY src /app/src
#10 CACHED
#11 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#11 CACHED
#12 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#12 CACHED
#13 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#13 CACHED
#14 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#14 CACHED
#15 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#15 CACHED
#16 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#16 CACHED
#17 [file-indexer  3/11] WORKDIR /app
#17 CACHED
#18 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#19 CACHED
#20 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#20 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#20 DONE 0.0s
#21 [file-indexer] exporting to image
#21 exporting layers
#21 ...
#22 [mcp-server internal] load build context
#22 transferring context: 1.64kB done
#22 DONE 0.0s
#23 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#23 CACHED
#24 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#24 CACHED
#25 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#25 CACHED
#26 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#26 CACHED
#27 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#27 CACHED
#28 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#28 CACHED
#29 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#30 CACHED
#31 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#31 CACHED
#32 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#32 CACHED
#33 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#33 CACHED
#34 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#34 CACHED
#35 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#35 CACHED
#36 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#36 CACHED
#37 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#37 CACHED
#38 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#38 CACHED
#39 [mcp-server  3/37] WORKDIR /app
#39 CACHED
#40 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#40 CACHED
#41 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#41 CACHED
#42 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#42 CACHED
#43 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#43 CACHED
#44 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#44 CACHED
#45 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#45 CACHED
#46 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#46 CACHED
#47 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#47 CACHED
#48 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#48 CACHED
#49 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#49 CACHED
#50 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#50 CACHED
#51 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#51 CACHED
#52 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#52 CACHED
#53 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#53 CACHED
#54 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#54 CACHED
#55 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#55 CACHED
#56 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#56 CACHED
#57 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#57 CACHED
#58 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#58 CACHED
#21 [file-indexer] exporting to image
#21 exporting layers done
#21 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#21 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#21 exporting attestation manifest sha256:93454f12bac6b13b94d84303460cbb649606bc1d2a2711c603fcd1fe3a5823b4 0.1s done
#21 exporting manifest list sha256:c9edc01a2487c9e385f46923deda478dc3142c7cb3316c31d3ef5ea831afc16f
#21 exporting manifest list sha256:c9edc01a2487c9e385f46923deda478dc3142c7cb3316c31d3ef5ea831afc16f 0.1s done
#21 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#21 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#21 DONE 0.2s
#59 [mcp-server] exporting to image
#59 exporting layers done
#59 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 done
#59 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 0.0s done
#59 exporting attestation manifest sha256:7e34402d890a1c4312c02352304b382135067590b95139e83a6259b583eecf86 0.1s done
#59 exporting manifest list sha256:f699d7533a7118d69eeb475ced018ed3938cf95667ee88a75c42bdd4fc11884b
#59 exporting manifest list sha256:f699d7533a7118d69eeb475ced018ed3938cf95667ee88a75c42bdd4fc11884b 0.0s done
#59 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 DONE 0.3s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 15 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-e3a05a6b8b9a49e09b6431b172758959 container=/workspace/tests/fixtures/idempotency-runtime-e3a05a6b8b9a49e09b6431b172758959
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=1c161b45eb1f4d34957f33658ac2811c
[US1] runId=1c161b45eb1f4d34957f33658ac2811c status=running attempt=1/120
[US1] runId=1c161b45eb1f4d34957f33658ac2811c status=completed attempt=2/120
[US1] runId=1c161b45eb1f4d34957f33658ac2811c finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=730c887e091545848c4a43e580530f25
[US1] runId=730c887e091545848c4a43e580530f25 status=running attempt=1/120
[US1] runId=730c887e091545848c4a43e580530f25 status=completed attempt=2/120
[US1] runId=730c887e091545848c4a43e580530f25 finished status=completed
US1 repeat-run completed. run1=1c161b45eb1f4d34957f33658ac2811c run2=730c887e091545848c4a43e580530f25 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-e6d0fc5b3ba940e7ab2692d82fc21d87 container=/workspace/tests/fixtures/idempotency-runtime-e6d0fc5b3ba940e7ab2692d82fc21d87
US2 deterministic update completed. run1=52c2ae24683248de8c9e8a21b4cf5b1d run2=d3bd6e0c6c864768949b5eacc25ff447
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-127e3d2cc3bf41d6bd996769ad611964 container=/workspace/tests/fixtures/idempotency-runtime-127e3d2cc3bf41d6bd996769ad611964
US3 stale cleanup completed. run2=8a461db8c0534485bdff1173d714ed16
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
[quality] stage 'us1' passed in 27940ms
[quality] stage 'integration' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 2.60kB 0.0s done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 686B 0.0s done
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
#9 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#9 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [mcp-server internal] load build context
#11 transferring context: 1.64kB done
#11 DONE 0.0s
#12 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#12 CACHED
#13 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#14 CACHED
#15 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#15 CACHED
#16 [file-indexer  9/11] COPY src /app/src
#16 CACHED
#17 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#17 CACHED
#18 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#18 CACHED
#19 [file-indexer  3/11] WORKDIR /app
#19 CACHED
#20 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#22 CACHED
#23 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#23 CACHED
#24 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#24 CACHED
#25 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#25 CACHED
#26 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#26 CACHED
#27 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#27 CACHED
#28 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#28 CACHED
#29 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#29 CACHED
#30 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#30 CACHED
#31 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#31 CACHED
#32 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#32 CACHED
#33 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#33 CACHED
#34 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#34 CACHED
#35 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#35 CACHED
#36 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#36 CACHED
#37 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#37 CACHED
#38 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#38 CACHED
#39 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#39 CACHED
#40 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#40 CACHED
#41 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#41 CACHED
#42 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#42 CACHED
#43 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#43 CACHED
#44 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#44 CACHED
#45 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#45 CACHED
#46 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#46 CACHED
#47 [mcp-server  3/37] WORKDIR /app
#47 CACHED
#48 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#48 CACHED
#49 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#49 CACHED
#50 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#50 CACHED
#51 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#51 CACHED
#52 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#52 CACHED
#53 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#53 CACHED
#54 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#54 CACHED
#55 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#55 CACHED
#56 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#56 CACHED
#57 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#57 CACHED
#58 [file-indexer] exporting to image
#58 exporting layers done
#58 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#58 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#58 exporting attestation manifest sha256:f4960a50206a56f75cd4a1f5bede784b82b06337dd48c4d554800a7408cacd7e 0.1s done
#58 exporting manifest list sha256:a298b48283aaaea14aec43760c380e5b4062ae6d86b99e16c722b447b4a2003d
#58 exporting manifest list sha256:a298b48283aaaea14aec43760c380e5b4062ae6d86b99e16c722b447b4a2003d 0.0s done
#58 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 DONE 0.2s
#59 [mcp-server] exporting to image
#59 exporting layers done
#59 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 done
#59 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 0.0s done
#59 exporting attestation manifest sha256:7e7f3df148be91a906ebf063bd75af33acf60939be92d330b8ac8de9b8f9ce26 0.1s done
#59 exporting manifest list sha256:269a796110b1942f2001d6eb40ff74accd8a6022a0a89f22f24c72409c0d6623
#59 exporting manifest list sha256:269a796110b1942f2001d6eb40ff74accd8a6022a0a89f22f24c72409c0d6623 0.0s done
#59 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#59 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 DONE 0.3s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
#2 [mcp-server internal] load build definition from Dockerfile
#2 transferring dockerfile: 2.60kB done
#2 DONE 0.0s
#3 [file-indexer internal] load build definition from Dockerfile
#3 transferring dockerfile: 686B done
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
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#8 [mcp-server internal] load build context
#8 transferring context: 1.64kB done
#8 DONE 0.0s
#12 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#12 CACHED
#13 [file-indexer  3/11] WORKDIR /app
#13 CACHED
#14 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#14 CACHED
#15 [file-indexer  9/11] COPY src /app/src
#15 CACHED
#16 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#16 CACHED
#17 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#18 CACHED
#19 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#19 CACHED
#20 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#22 CACHED
#23 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#23 CACHED
#24 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#24 CACHED
#25 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#25 CACHED
#26 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#26 CACHED
#27 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#27 CACHED
#28 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#28 CACHED
#29 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#29 CACHED
#30 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#30 CACHED
#31 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#32 CACHED
#33 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#33 CACHED
#34 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#34 CACHED
#35 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#35 CACHED
#36 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#36 CACHED
#37 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#37 CACHED
#38 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#38 CACHED
#39 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#39 CACHED
#40 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#40 CACHED
#41 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#41 CACHED
#42 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#42 CACHED
#43 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#43 CACHED
#44 [mcp-server  3/37] WORKDIR /app
#44 CACHED
#45 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#45 CACHED
#46 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#46 CACHED
#47 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#47 CACHED
#48 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#48 CACHED
#49 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#49 CACHED
#50 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#50 CACHED
#51 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#51 CACHED
#52 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#52 CACHED
#53 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#53 CACHED
#54 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#54 CACHED
#55 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#55 CACHED
#56 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#56 CACHED
#57 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#57 CACHED
#58 [mcp-server] exporting to image
#58 exporting layers done
#58 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 done
#58 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 0.0s done
#58 exporting attestation manifest sha256:f164de861108cd07c476b7d0b9dbadb3e1a97fb08ea54381a26073d9e9ebcb6b
#58 exporting attestation manifest sha256:f164de861108cd07c476b7d0b9dbadb3e1a97fb08ea54381a26073d9e9ebcb6b 0.1s done
#58 exporting manifest list sha256:df71a89e4ab5a7f8455d6ed49ae79afe78b6955b091cc411ee73604a634e9bd3
#58 exporting manifest list sha256:df71a89e4ab5a7f8455d6ed49ae79afe78b6955b091cc411ee73604a634e9bd3 0.0s done
#58 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#58 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#58 DONE 0.3s
#59 [file-indexer] exporting to image
#59 exporting layers done
#59 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#59 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#59 exporting attestation manifest sha256:c5328441333a2325023bcd759254884bb0eb85a22c50b6e0659fe7b72f9d5f81 0.1s done
#59 exporting manifest list sha256:9cba577154bd8fdbcf73f80647738e94e51807ab74a40b5d6492c3df23e829f4 0.0s done
#59 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#59 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#59 DONE 0.3s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
#2 transferring dockerfile: 686B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 2.60kB done
#3 DONE 0.0s
#4 [auth] library/alpine:pull token for registry-1.docker.io
#4 DONE 0.0s
#5 [auth] library/python:pull token for registry-1.docker.io
#5 DONE 0.0s
#6 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#6 DONE 1.0s
#7 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#7 DONE 1.0s
#8 [mcp-server internal] load .dockerignore
#8 transferring context: 2B done
#8 DONE 0.0s
#9 [file-indexer internal] load .dockerignore
#9 transferring context: 2B done
#9 DONE 0.0s
#10 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#11 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#11 DONE 0.0s
#12 [mcp-server internal] load build context
#12 transferring context: 1.64kB done
#12 DONE 0.0s
#13 [file-indexer internal] load build context
#13 transferring context: 5.50kB done
#13 DONE 0.0s
#14 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#14 CACHED
#15 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#15 CACHED
#16 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#16 CACHED
#17 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#17 CACHED
#18 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#18 CACHED
#19 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#19 CACHED
#20 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#20 CACHED
#21 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#21 CACHED
#22 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#22 CACHED
#23 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#23 CACHED
#24 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#24 CACHED
#25 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#25 CACHED
#26 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#26 CACHED
#27 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#27 CACHED
#28 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#28 CACHED
#29 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#29 CACHED
#30 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#30 CACHED
#31 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#31 CACHED
#32 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#32 CACHED
#33 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#33 CACHED
#34 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#34 CACHED
#35 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#35 CACHED
#36 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#36 CACHED
#37 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#37 CACHED
#38 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#38 CACHED
#39 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#39 CACHED
#40 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#40 CACHED
#41 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#41 CACHED
#42 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#42 CACHED
#43 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#43 CACHED
#44 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#44 CACHED
#45 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#45 CACHED
#46 [mcp-server  3/37] WORKDIR /app
#46 CACHED
#47 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#47 CACHED
#48 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#48 CACHED
#49 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#49 CACHED
#50 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#50 CACHED
#51 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#51 CACHED
#52 [file-indexer  3/11] WORKDIR /app
#52 CACHED
#53 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#53 CACHED
#54 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#54 CACHED
#55 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#55 CACHED
#56 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#56 CACHED
#57 [file-indexer  9/11] COPY src /app/src
#57 CACHED
#58 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#58 CACHED
#59 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#59 CACHED
#60 [file-indexer] exporting to image
#60 exporting layers done
#60 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 0.0s done
#60 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 0.0s done
#60 exporting attestation manifest sha256:191b7dff8a741f1c251c7d604b72bb46d05935a246556644bb22484a934eed0b
#60 exporting attestation manifest sha256:191b7dff8a741f1c251c7d604b72bb46d05935a246556644bb22484a934eed0b 0.1s done
#60 exporting manifest list sha256:37704662d7056bc8fc919b9123c0e79c680b74ba0dd8e530b345d76c281a4738
#60 exporting manifest list sha256:37704662d7056bc8fc919b9123c0e79c680b74ba0dd8e530b345d76c281a4738 0.0s done
#60 naming to docker.io/library/ndlss-memory-file-indexer:latest done
#60 unpacking to docker.io/library/ndlss-memory-file-indexer:latest done
#60 DONE 0.2s
#61 [mcp-server] exporting to image
#61 exporting layers done
#61 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 done
#61 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 done
#61 exporting attestation manifest sha256:f2bd3cda0e1526ed8d4caec8931c8bf46c19613db5c13b75e5d865a0a3d3a6e7 0.1s done
#61 exporting manifest list sha256:775fc59efb8ff34b3e3899feb25260aa80634e9f742aaf7877f8f0e735d81665 0.1s done
#61 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#61 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#61 DONE 0.3s
#62 [file-indexer] resolving provenance for metadata file
#62 DONE 0.0s
#63 [mcp-server] resolving provenance for metadata file
#63 DONE 0.0s
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
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     16 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         16 seconds ago   Up 15 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-c79eee62336942ca8629d2e4c0799cf5 container=/workspace/tests/fixtures/delta-runtime-c79eee62336942ca8629d2e4c0799cf5
US1 delta changed-only completed. run=584820ed47264f50b374b253fdd504e4
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-9f54548f6b67458b8a4c6e6e4c4abda3 container=/workspace/tests/fixtures/delta-runtime-9f54548f6b67458b8a4c6e6e4c4abda3
US2 delta delete+rename completed. run=5f812f84c45a4eeba4a2ec1f1731384a
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-f39d3842b74742f3a3cad4e6fb35d35f container=/workspace/tests/fixtures/delta-runtime-f39d3842b74742f3a3cad4e6fb35d35f
US3 delta fallback completed. run=10e8a8380d7e444fa06a6e2104da7fb4 reason=BASE_REF_NOT_FOUND
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
#2 transferring dockerfile: 686B 0.0s done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 2.60kB done
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
#9 [mcp-server internal] load build context
#9 DONE 0.0s
#10 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#10 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#10 DONE 0.0s
#11 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#11 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#11 DONE 0.0s
#8 [file-indexer internal] load build context
#8 transferring context: 5.50kB done
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 transferring context: 1.64kB done
#9 DONE 0.0s
#12 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#12 CACHED
#13 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#13 CACHED
#14 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#14 CACHED
#15 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#15 CACHED
#16 [file-indexer  3/11] WORKDIR /app
#16 CACHED
#17 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#17 CACHED
#18 [file-indexer  9/11] COPY src /app/src
#18 CACHED
#19 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#19 CACHED
#20 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#22 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#22 CACHED
#23 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#23 CACHED
#24 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#24 CACHED
#25 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#25 CACHED
#26 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#26 CACHED
#27 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#27 CACHED
#28 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#28 CACHED
#29 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#29 CACHED
#30 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#30 CACHED
#31 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#31 CACHED
#32 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#32 CACHED
#33 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#33 CACHED
#34 [mcp-server  3/37] WORKDIR /app
#34 CACHED
#35 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#35 CACHED
#36 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#36 CACHED
#37 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#37 CACHED
#38 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#38 CACHED
#39 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#39 CACHED
#40 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#40 CACHED
#41 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#41 CACHED
#42 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#42 CACHED
#43 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#43 CACHED
#44 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#44 CACHED
#45 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#45 CACHED
#46 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#46 CACHED
#47 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#47 CACHED
#48 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#48 CACHED
#49 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#49 CACHED
#50 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#50 CACHED
#51 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#51 CACHED
#52 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#52 CACHED
#53 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#53 CACHED
#54 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#54 CACHED
#55 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#55 CACHED
#56 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#56 CACHED
#57 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#57 CACHED
#58 [mcp-server] exporting to image
#58 exporting layers done
#58 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 0.0s done
#58 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 done
#58 exporting attestation manifest sha256:735e3e5c94ba3ff5357a5e88813f6157a043bf86e517dbfbc85164f1a5a9ba68
#58 exporting attestation manifest sha256:735e3e5c94ba3ff5357a5e88813f6157a043bf86e517dbfbc85164f1a5a9ba68 0.1s done
#58 exporting manifest list sha256:43dab9f5c8863cfff910bdf06e0065ae9328f840e88ea9d1f7996dde1c0c47fc
#58 exporting manifest list sha256:43dab9f5c8863cfff910bdf06e0065ae9328f840e88ea9d1f7996dde1c0c47fc 0.0s done
#58 naming to docker.io/library/ndlss-memory-mcp-server:latest done
#58 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#58 DONE 0.3s
#59 [file-indexer] exporting to image
#59 exporting layers done
#59 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#59 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#59 exporting attestation manifest sha256:f27674079f9d53b0d17dd987630c140512ad9746c9fd0c044c2139836520a506 0.1s done
#59 exporting manifest list sha256:ad43c44f986654698a1b0375d901454306e487ba6d8a55a1c138e65b44e1c4cc 0.0s done
#59 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#59 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#59 DONE 0.2s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
ndlss-memory-mcp-server     ndlss-memory-mcp-server     "/app/scripts/entrypвЂ¦"   mcp-server     15 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
ndlss-memory-qdrant         qdrant/qdrant:v1.9.5        "./entrypoint.sh"        qdrant         15 seconds ago   Up 14 seconds (healthy)           0.0.0.0:6333->6333/tcp, [::]:6333->6333/tcp
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US1 deterministic chunking scenario finished for runId=0047bfeb3d4a4949ba5762b00ee1beb6
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US2 retry+upsert scenario finished for runId=065d5420d66f4c048d939bf02e981f44 retryCount=0
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=3ed81697552a4379a0dd1ba3aacacec4 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\chunking-embeddings
US3 metadata traceability scenario finished for runId=c960f69f749741e7828ce84268bf37e4
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
[quality] stage 'integration' passed in 235406ms
[quality] stage 'us2' started
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 686B done
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 2.60kB done
#3 DONE 0.0s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 ...
#5 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#5 DONE 0.6s
#4 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#4 DONE 0.6s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [mcp-server internal] load build context
#8 DONE 0.0s
#9 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#9 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#9 DONE 0.0s
#10 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#10 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#10 DONE 0.0s
#11 [file-indexer internal] load build context
#11 transferring context: 5.50kB done
#11 DONE 0.0s
#12 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#12 CACHED
#13 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#13 CACHED
#14 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#14 CACHED
#15 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#15 CACHED
#16 [file-indexer  9/11] COPY src /app/src
#16 CACHED
#17 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#17 CACHED
#18 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#18 CACHED
#19 [file-indexer  3/11] WORKDIR /app
#19 CACHED
#20 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#20 CACHED
#21 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#21 CACHED
#8 [mcp-server internal] load build context
#8 transferring context: 1.64kB done
#8 DONE 0.1s
#22 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#22 CACHED
#23 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#23 CACHED
#24 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#24 CACHED
#25 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#25 CACHED
#26 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#26 CACHED
#27 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#27 CACHED
#28 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#28 CACHED
#29 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#29 CACHED
#30 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#30 CACHED
#31 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#31 CACHED
#32 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#32 CACHED
#33 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#33 CACHED
#34 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#34 CACHED
#35 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#35 CACHED
#36 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#36 CACHED
#37 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#37 CACHED
#38 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#38 CACHED
#39 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#39 CACHED
#40 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#40 CACHED
#41 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#41 CACHED
#42 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#42 CACHED
#43 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#43 CACHED
#44 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#44 CACHED
#45 [mcp-server  3/37] WORKDIR /app
#45 CACHED
#46 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#46 CACHED
#47 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#47 CACHED
#48 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#48 CACHED
#49 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#49 CACHED
#50 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#50 CACHED
#51 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#51 CACHED
#52 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#52 CACHED
#53 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#53 CACHED
#54 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#54 CACHED
#55 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#55 CACHED
#56 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#56 CACHED
#57 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#57 CACHED
#58 [file-indexer] exporting to image
#58 exporting layers done
#58 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#58 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#58 exporting attestation manifest sha256:67d821c246a1d6e03ce1742d86fc4f8ef4b0fedc326a24c8295513270dd22806
#58 exporting attestation manifest sha256:67d821c246a1d6e03ce1742d86fc4f8ef4b0fedc326a24c8295513270dd22806 0.1s done
#58 exporting manifest list sha256:841b2ca4faa65a7fa9fd35a01f8ddd130eb354eeabec2be64b5697b3d23cdb30 0.0s done
#58 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 unpacking to docker.io/library/ndlss-memory-file-indexer:latest
#58 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 DONE 0.2s
#59 [mcp-server] exporting to image
#59 exporting layers 0.0s done
#59 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 0.0s done
#59 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 0.0s done
#59 exporting attestation manifest sha256:9626a3241dc7434718c2df315604fc9e643d0887f6b0d7bb3be6a2edab77b630 0.1s done
#59 exporting manifest list sha256:9936a1110b7282cca44052f781dc231a286fc4897369599e2a765502f608604c 0.0s done
#59 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 unpacking to docker.io/library/ndlss-memory-mcp-server:latest
#59 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 DONE 0.3s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
US2 search flow completed. ingestionRunId=fffd985d686f477a8fb75bf1707782b8 results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
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
[quality] stage 'us2' passed in 23773ms
[quality] stage 'contract' started
Contract checks passed. Summary: Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\contract-check-summary.md
[quality] stage 'contract' passed in 35ms
[quality] stage 'us3' started
#1 [internal] load local bake definitions
#1 reading from stdin 1.06kB 0.0s done
#1 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 DONE 0.0s
#3 [mcp-server internal] load build definition from Dockerfile
#3 transferring dockerfile: 2.60kB done
#3 DONE 0.0s
#2 [file-indexer internal] load build definition from Dockerfile
#2 transferring dockerfile: 686B done
#2 DONE 0.0s
#4 [file-indexer internal] load metadata for docker.io/library/alpine:3.20
#4 DONE 0.8s
#5 [mcp-server internal] load metadata for docker.io/library/python:3.12-alpine
#5 DONE 0.9s
#6 [file-indexer internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s
#7 [mcp-server internal] load .dockerignore
#7 transferring context: 2B done
#7 DONE 0.0s
#8 [file-indexer  1/11] FROM docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805
#8 resolve docker.io/library/alpine:3.20@sha256:a4f4213abb84c497377b8544c81b3564f313746700372ec4fe84653e4fb03805 0.0s done
#8 DONE 0.0s
#9 [mcp-server internal] load build context
#9 DONE 0.0s
#10 [file-indexer internal] load build context
#10 transferring context: 5.50kB done
#10 DONE 0.0s
#11 [file-indexer  4/11] COPY scripts/validate-config.sh /app/scripts/validate-config.sh
#11 CACHED
#12 [file-indexer  8/11] COPY config/runtime-config.schema.json /app/config/runtime-config.schema.json
#12 CACHED
#13 [file-indexer  9/11] COPY src /app/src
#13 CACHED
#14 [file-indexer 10/11] RUN sed -i 's/\r$//' /app/scripts/*.sh
#14 CACHED
#15 [file-indexer  5/11] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#15 CACHED
#16 [file-indexer  7/11] COPY scripts/ingestion-worker.sh /app/scripts/ingestion-worker.sh
#16 CACHED
#17 [file-indexer  2/11] RUN apk add --no-cache bash coreutils
#17 CACHED
#18 [file-indexer  3/11] WORKDIR /app
#18 CACHED
#19 [file-indexer  6/11] COPY scripts/full-scan-worker.sh /app/scripts/full-scan-worker.sh
#19 CACHED
#20 [file-indexer 11/11] RUN chmod +x /app/scripts/validate-config.sh /app/scripts/entrypoint.sh /app/scripts/full-scan-worker.sh /app/scripts/ingestion-worker.sh
#20 CACHED
#21 [mcp-server  1/37] FROM docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#21 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0
#21 resolve docker.io/library/python:3.12-alpine@sha256:2d91681153dd4b8cdb52d4fd34a17b9edbafa4dd3086143cfd4b6c3a84c1acb0 0.0s done
#21 DONE 0.0s
#9 [mcp-server internal] load build context
#9 transferring context: 1.64kB done
#9 DONE 0.0s
#22 [mcp-server  3/37] WORKDIR /app
#22 CACHED
#23 [mcp-server 33/37] COPY openapi/mcp-search-tools.openapi.yaml /app/openapi/mcp-search-tools.openapi.yaml
#23 CACHED
#24 [mcp-server 28/37] COPY openapi/compose-observability.openapi.yaml /app/openapi/compose-observability.openapi.yaml
#24 CACHED
#25 [mcp-server  4/37] COPY src/system_status_handler.py /app/src/system_status_handler.py
#25 CACHED
#26 [mcp-server  6/37] COPY src/full_scan_errors.py /app/src/full_scan_errors.py
#26 CACHED
#27 [mcp-server 21/37] COPY src/search_models.py /app/src/search_models.py
#27 CACHED
#28 [mcp-server 26/37] COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
#28 CACHED
#29 [mcp-server 15/37] COPY src/command_execution_models.py /app/src/command_execution_models.py
#29 CACHED
#30 [mcp-server 23/37] COPY src/search_result_ref.py /app/src/search_result_ref.py
#30 CACHED
#31 [mcp-server 32/37] COPY openapi/delta-after-commit-indexing.openapi.yaml /app/openapi/delta-after-commit-indexing.openapi.yaml
#31 CACHED
#32 [mcp-server  7/37] COPY src/ingestion_state.py /app/src/ingestion_state.py
#32 CACHED
#33 [mcp-server 16/37] COPY src/command_execution_state.py /app/src/command_execution_state.py
#33 CACHED
#34 [mcp-server 13/37] COPY src/command_security_policy.py /app/src/command_security_policy.py
#34 CACHED
#35 [mcp-server 20/37] COPY src/command_execution_service.py /app/src/command_execution_service.py
#35 CACHED
#36 [mcp-server 22/37] COPY src/search_errors.py /app/src/search_errors.py
#36 CACHED
#37 [mcp-server 18/37] COPY src/command_workspace_guard.py /app/src/command_workspace_guard.py
#37 CACHED
#38 [mcp-server 19/37] COPY src/command_audit_store.py /app/src/command_audit_store.py
#38 CACHED
#39 [mcp-server 30/37] COPY openapi/chunking-embeddings.openapi.yaml /app/openapi/chunking-embeddings.openapi.yaml
#39 CACHED
#40 [mcp-server  8/37] COPY src/ingestion_errors.py /app/src/ingestion_errors.py
#40 CACHED
#41 [mcp-server 27/37] COPY config/security-policy.yaml /app/config/security-policy.yaml
#41 CACHED
#42 [mcp-server 14/37] COPY src/command_execution_errors.py /app/src/command_execution_errors.py
#42 CACHED
#43 [mcp-server  5/37] COPY src/full_scan_state.py /app/src/full_scan_state.py
#43 CACHED
#44 [mcp-server  9/37] COPY src/idempotency_state.py /app/src/idempotency_state.py
#44 CACHED
#45 [mcp-server 35/37] RUN sed -i 's/\r$//' /app/scripts/*.sh
#45 CACHED
#46 [mcp-server 11/37] COPY src/delta_after_commit_state.py /app/src/delta_after_commit_state.py
#46 CACHED
#47 [mcp-server 31/37] COPY openapi/idempotency-indexing.openapi.yaml /app/openapi/idempotency-indexing.openapi.yaml
#47 CACHED
#48 [mcp-server 12/37] COPY src/delta_after_commit_errors.py /app/src/delta_after_commit_errors.py
#48 CACHED
#49 [mcp-server 24/37] COPY src/search_repository.py /app/src/search_repository.py
#49 CACHED
#50 [mcp-server 17/37] COPY src/command_process_runner.py /app/src/command_process_runner.py
#50 CACHED
#51 [mcp-server 10/37] COPY src/idempotency_errors.py /app/src/idempotency_errors.py
#51 CACHED
#52 [mcp-server 29/37] COPY openapi/full-scan-indexing.openapi.yaml /app/openapi/full-scan-indexing.openapi.yaml
#52 CACHED
#53 [mcp-server 36/37] RUN chmod +x /app/scripts/entrypoint.sh
#53 CACHED
#54 [mcp-server 25/37] COPY src/search_service.py /app/src/search_service.py
#54 CACHED
#55 [mcp-server  2/37] RUN apk add --no-cache curl git && pip install --no-cache-dir flask pyyaml
#55 CACHED
#56 [mcp-server 34/37] COPY openapi/mcp-command-security.openapi.yaml /app/openapi/mcp-command-security.openapi.yaml
#56 CACHED
#57 [mcp-server 37/37] RUN addgroup -S appgroup && adduser -S appuser -G appgroup
#57 CACHED
#58 [file-indexer] exporting to image
#58 exporting layers done
#58 exporting manifest sha256:fe720310b214f49fc1a84e6550da9bc789749c6fe2fe2d68fbd421e77cc24281 done
#58 exporting config sha256:c567a07e699737c3d4a9d907256881c10d9ef0272993f012b98d577121c1e2c6 done
#58 exporting attestation manifest sha256:c17e071fad012451d7a2c7bfe4780a9e4fb7886aa4e81743e6c6c88a12a980cc 0.0s done
#58 exporting manifest list sha256:16dec9ab68f768f0158876093dba55b870c2bdf27af1ae66442dd9e074dbd579
#58 exporting manifest list sha256:16dec9ab68f768f0158876093dba55b870c2bdf27af1ae66442dd9e074dbd579 0.0s done
#58 naming to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 unpacking to docker.io/library/ndlss-memory-file-indexer:latest 0.0s done
#58 DONE 0.2s
#59 [mcp-server] exporting to image
#59 exporting layers done
#59 exporting manifest sha256:6c81dcdc9a1e873f0e0ed1b60f2e21b6502515d3b84fe769a17653bf8c231de9 done
#59 exporting config sha256:e63be372a35c9060148821404791773a7880041c1d1144b3998c17f6d9c136b9 0.0s done
#59 exporting attestation manifest sha256:e3c6bf2fcccf3f1568d3e6663a3f2df8d995857e1ef1b8b088d8595044dc36fd 0.1s done
#59 exporting manifest list sha256:659c7856487154f76a3b7a7cce0c0cab2591445ea4f8497ff4393d5951262a44 0.0s done
#59 naming to docker.io/library/ndlss-memory-mcp-server:latest
#59 naming to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 unpacking to docker.io/library/ndlss-memory-mcp-server:latest 0.0s done
#59 DONE 0.2s
#60 [file-indexer] resolving provenance for metadata file
#60 DONE 0.0s
#61 [mcp-server] resolving provenance for metadata file
#61 DONE 0.0s
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
Prepared delta-after-commit test env host=Z:\WORK\ndlss-memory\tests\fixtures\delta-runtime-2a070b14ad0349d0b7371d0638aa40a1 container=/workspace/tests/fixtures/delta-runtime-2a070b14ad0349d0b7371d0638aa40a1
US1 delta changed-only completed. run=82e8b273e9e4424eb2bc19aeff8cb949
Prepared ingestion test env for workspace: Z:\WORK\ndlss-memory\tests\fixtures\idempotency
US2 search flow completed. ingestionRunId=94d9d257357d495eadfc5e2c0e33604c results=5 artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us2-integration-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-3cdd041f2be7413391f1f595ca7ffd94 container=/workspace/tests/fixtures/idempotency-runtime-3cdd041f2be7413391f1f595ca7ffd94
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=9780ca05b1c04677be3b0e544310d9f7
[US1] runId=9780ca05b1c04677be3b0e544310d9f7 status=running attempt=1/120
[US1] runId=9780ca05b1c04677be3b0e544310d9f7 status=completed attempt=2/120
[US1] runId=9780ca05b1c04677be3b0e544310d9f7 finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=7e8c2b6da68f45209b14be27758558ec
[US1] runId=7e8c2b6da68f45209b14be27758558ec status=running attempt=1/120
[US1] runId=7e8c2b6da68f45209b14be27758558ec status=completed attempt=2/120
[US1] runId=7e8c2b6da68f45209b14be27758558ec finished status=completed
US1 repeat-run completed. run1=9780ca05b1c04677be3b0e544310d9f7 run2=7e8c2b6da68f45209b14be27758558ec artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
Prepared idempotency test env host=Z:\WORK\ndlss-memory\tests\\fixtures\idempotency-runtime-154b5d89f2c4489fb92a1783ecacd37a container=/workspace/tests/fixtures/idempotency-runtime-154b5d89f2c4489fb92a1783ecacd37a
[US1] waiting for MCP health at http://localhost:8080/health
[US1] health is ok after 1 attempts
[US1] starting first idempotency run
[US1] waiting for idempotency job status runId=7daeb92524944610a471e367cc5566ce
[US1] runId=7daeb92524944610a471e367cc5566ce status=running attempt=1/120
[US1] runId=7daeb92524944610a471e367cc5566ce status=completed attempt=2/120
[US1] runId=7daeb92524944610a471e367cc5566ce finished status=completed
[US1] starting second idempotency run
[US1] waiting for idempotency job status runId=d5f4b2ad45d0463c85117294f7ea210e
[US1] runId=d5f4b2ad45d0463c85117294f7ea210e status=running attempt=1/120
[US1] runId=d5f4b2ad45d0463c85117294f7ea210e status=completed attempt=2/120
[US1] runId=d5f4b2ad45d0463c85117294f7ea210e finished status=completed
US1 repeat-run completed. run1=7daeb92524944610a471e367cc5566ce run2=d5f4b2ad45d0463c85117294f7ea210e artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us1-idempotency-summary.json
US3 E2E quality scenario passed. artifact=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\us3-e2e-summary.json
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
[quality] stage 'us3' passed in 29160ms
Quality run passed. report=Z:\WORK\ndlss-memory\tests\artifacts\quality-stability\quality-run-report.json

- finishedAt: 2026-02-22T03:19:57.2057118+03:00
- exitCode: 0
