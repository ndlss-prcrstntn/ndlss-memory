# Contributing

## Branching and specs

- Use incremental feature numbering: `002`, `003`, `004`, ... (do not reuse `001`).
- Keep `specs/<feature>/spec.md`, `plan.md`, and `tasks.md` up to date before implementation.
- Save markdown files in UTF-8.

## Local workflow

1. Create a virtual environment and install dependencies.
2. Run unit tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit
```

3. For compose/integration changes, run relevant scripts from `scripts/tests/`.

## Code and docs quality

- Keep changes atomic and use clear commit messages.
- Do not commit temporary files, secrets, or local `.env` overrides.
- For shell scripts, use LF line endings and a valid shebang.
- Update user-facing docs when behavior changes:
  - [README](README.md)
  - [Quickstart](docs/quickstart.md)
  - [Compose presets](docs/compose-presets.md)
  - [Configuration](docs/configuration.md)
  - [Roadmaps](docs/roadmaps/README.md)

## Pull requests

- Add a short problem/solution summary.
- Attach test results (at minimum unit tests; add integration/e2e where relevant).
- Link related spec/plan/tasks files if the change is part of a feature branch.
