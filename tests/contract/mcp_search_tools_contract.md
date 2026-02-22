# Contract Smoke: MCP Search Tools

## Preconditions

- `mcp-server` доступен на `http://localhost:8080`
- В коллекции `workspace_chunks` есть как минимум один документ

## Semantic Search Contract

- [ ] `POST /v1/search/semantic` с валидным телом возвращает HTTP 200
- [ ] Ответ содержит `status`, `results`, `meta`
- [ ] `meta` содержит `count`, `limit`, `requestedAt`
- [ ] При `status=empty` поле `results` равно `[]`
- [ ] При невалидном запросе возвращается HTTP 400 и поля `errorCode`, `message`

## Source By ID Contract

- [ ] `GET /v1/search/results/{resultId}/source` для валидного ID возвращает HTTP 200
- [ ] Ответ содержит `status=ok`, `source`, `meta`
- [ ] `source` содержит `resultId`, `content`, `sourcePath`
- [ ] Для неизвестного ID возвращается HTTP 404 с `errorCode=RESULT_NOT_FOUND`

## Metadata By ID Contract

- [ ] `GET /v1/search/results/{resultId}/metadata` для валидного ID возвращает HTTP 200
- [ ] Ответ содержит `status=ok`, `metadata`, `meta`
- [ ] `metadata` содержит `resultId`, `fileName`, `fileType`, `sourcePath`
- [ ] Для неизвестного ID возвращается HTTP 404 с машиночитаемым `errorCode`

## Filter & Empty Contract

- [ ] Фильтры `path/folder/fileType` применяются как логическое И
- [ ] Запрос без совпадений возвращает HTTP 200, `status=empty`, без internal error
- [ ] Для `status=ok` каждый элемент `results` содержит валидный `resultId`
- [ ] Для `status=empty` endpoint-ы `/source` и `/metadata` не вызываются без `resultId`
- [ ] Ответы `/source` и `/metadata` для валидного `resultId` содержат `status=ok`
