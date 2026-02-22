# Contract Check Summary

| Check | Status | Details |
|-------|--------|---------|
| file:tests/contract/quality_stage_result_contract.md | PASS | exists |
| file:tests/contract/mcp_search_tools_contract.md | PASS | exists |
| file:specs/008-quality-stability-tests/contracts/quality-stability-tests.openapi.yaml | PASS | exists |
| file:services/mcp-server/openapi/quality-stability-tests.openapi.yaml | PASS | exists |
| openapi:/v1/indexing/full-scan/jobs | PASS | present |
| openapi:/v1/indexing/delta-after-commit/jobs | PASS | present |
| openapi:/v1/indexing/idempotency/jobs | PASS | present |
| openapi:/v1/search/semantic | PASS | present |
| openapi:/v1/search/results/{resultId}/source | PASS | present |
| openapi:/v1/search/results/{resultId}/metadata | PASS | present |
| openapi:components: | PASS | present |
| openapi:ApiError | PASS | present |
| stage-contract:stageName | PASS | present |
| stage-contract:status | PASS | present |
| stage-contract:durationMs | PASS | present |
| stage-contract:runId | PASS | present |
| stage-contract:failures | PASS | present |

- total: 17
- failed: 0
- generatedAt: 2026-02-22T22:39:15.7274319+03:00
