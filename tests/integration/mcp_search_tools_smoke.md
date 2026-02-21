# Integration: MCP Search Tools Smoke

1. Запустить стек:
   - `pwsh scripts/dev/up.ps1`
2. Проверить health:
   - `curl http://localhost:8080/health`
3. Выполнить semantic search:
   - `POST /v1/search/semantic` с `{"query":"compose healthcheck","limit":5}`
4. Проверить:
   - ответ HTTP 200
   - есть поля `status`, `results`, `meta`
5. Если `results` не пустой, взять первый `resultId` и проверить:
   - `GET /v1/search/results/{resultId}/source`
   - `GET /v1/search/results/{resultId}/metadata`
6. Проверить корректную ошибку:
   - `GET /v1/search/results/chunk:0000000000000000000000000000000000000000000000000000000000000000/source`
   - ожидается HTTP 404 и `errorCode=RESULT_NOT_FOUND`
