# Integration: Search Traceability Flow

## Цель

Проверить цепочку `search -> source -> metadata`.

## Шаги

1. Выполнить `POST /v1/search/semantic` с валидным запросом.
2. Взять `resultId` первого результата.
3. Запросить источник:
   - `GET /v1/search/results/{resultId}/source`
4. Запросить метаданные:
   - `GET /v1/search/results/{resultId}/metadata`
5. Проверить:
   - в обоих ответах `status=ok`
   - `source.resultId == metadata.resultId`
   - `source.sourcePath == metadata.sourcePath`
6. Для несуществующего ID проверить HTTP 404 и `errorCode=RESULT_NOT_FOUND`.
