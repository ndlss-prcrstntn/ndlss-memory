# Delta-after-commit Fixture Manifest

## Base repository

- `repo-base/docs/stable.md`: файл для сценария modified.
- `repo-base/docs/delete-me.md`: файл для сценария deleted.
- `repo-base/docs/rename-me.md`: файл для сценария renamed.

## Change templates

- `changes/added.md`: шаблон нового файла.
- `changes/modified-extra.txt`: строка для добавления в `stable.md`.

## Expected git statuses

- Added: `A docs/added.md`
- Modified: `M docs/stable.md`
- Deleted: `D docs/delete-me.md`
- Renamed: `R* docs/rename-me.md -> docs/renamed.md`
