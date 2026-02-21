# Data Model: Delta-after-commit режим

## 1. DeltaIndexRun

Описание: жизненный цикл одного запуска delta индексации.

Поля:

- `run_id` (string, required): уникальный идентификатор запуска.
- `requested_mode` (string, required): `delta-after-commit`.
- `effective_mode` (string, required): `delta-after-commit | full-scan-fallback`.
- `status` (string, required): `queued | running | completed | partial | failed`.
- `base_ref` (string, required): базовая ревизия сравнения.
- `target_ref` (string, required): целевая ревизия сравнения.
- `fallback_reason_code` (string, optional): код причины fallback.
- `started_at` (datetime, required)
- `finished_at` (datetime, optional)

Валидация:

- `effective_mode=full-scan-fallback` требует заполненный `fallback_reason_code`.
- `finished_at` обязателен для финальных статусов.

Переходы состояния:

- `queued -> running`
- `running -> completed`
- `running -> partial`
- `running -> failed`

## 2. GitChangeSet

Описание: нормализованный набор изменений между `base_ref` и `target_ref`.

Поля:

- `change_id` (string, required)
- `change_type` (string, required): `added | modified | deleted | renamed`.
- `path` (string, required): актуальный путь (для rename - новый путь).
- `old_path` (string, optional): старый путь для rename.
- `detected_at` (datetime, required)

Валидация:

- `change_type=renamed` требует непустой `old_path`.
- Пара (`change_type`, `path`, `old_path`) уникальна в рамках одного `run_id`.

## 3. DeltaCandidateFile

Описание: файл, прошедший классификацию и правила обработки.

Поля:

- `run_id` (string, required)
- `path` (string, required)
- `source_change_type` (string, required)
- `decision` (string, required): `index | delete | skip`.
- `decision_reason_code` (string, required)
- `filtered_out` (boolean, required)

Валидация:

- `decision=index` допускается только для `added | modified | renamed` после фильтров.
- `decision=delete` обязателен для `deleted` и stale части `renamed`.
- `decision=skip` требует явный `decision_reason_code`.

## 4. PathTransition

Описание: соответствие старого и нового пути для rename-операций.

Поля:

- `run_id` (string, required)
- `old_path` (string, required)
- `new_path` (string, required)
- `transition_status` (string, required): `pending | relinked | failed`.

Валидация:

- `old_path` и `new_path` не могут быть одинаковыми.
- Для `transition_status=relinked` старая привязка должна отсутствовать в итоговом индексе.

## 5. DeltaRunSummary

Описание: агрегированный итог запуска delta-after-commit.

Поля:

- `run_id` (string, required)
- `status` (string, required): `completed | partial | failed`.
- `effective_mode` (string, required)
- `added_files` (integer, required)
- `modified_files` (integer, required)
- `deleted_files` (integer, required)
- `renamed_files` (integer, required)
- `indexed_files` (integer, required)
- `removed_records` (integer, required)
- `skipped_files` (integer, required)
- `failed_files` (integer, required)
- `reason_breakdown` (array[ReasonCount], required)

Подсущность `ReasonCount`:

- `code` (string, required)
- `count` (integer, required)

Валидация:

- Все числовые поля >= 0.
- `reason_breakdown.count` в сумме соответствует количеству non-success решений (`skip` + `failed` + fallback).
