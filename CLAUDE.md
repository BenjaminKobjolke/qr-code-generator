# Project Rules — QR Code Generator

This file mirrors the relevant rules from
`D:\GIT\BenjaminKobjolke\claude-code\coding-rules\COMMON_RULES.md` and `PYTHON_RULES.md`.
Keep in sync when source rules change.

---

## Common Rules

### Use Objects for Related Values
Bundle related values into a DTO/Settings object instead of long parameter lists.

### Test-Driven Development
Write tests first → confirm fail → implement → confirm pass.

### Integration Tests
Required in addition to unit tests. Live in `tests/integration/`.

### Test Runner Scripts
- `tools/run_tests.bat` — unit tests
- `tools/run_integration_tests.bat` — integration tests

### Prefer Type-Safe Values
Typed DTOs, enums, frozen dataclasses. No stringly-typed values.

### String Constants
Centralize in `app/config/constants.py`. Never scatter raw strings.

### DRY
Extract shared logic. Use constants for repeated values.

### Confirm Dependency Versions
Ask before adding packages. Versions confirmed for this project:
- `qrcode[pil] >= 8.0`
- `Pillow >= 11.0`
- Dev: `pytest`, `ruff`, `mypy`

### Error Handling & Logging
Centralized handler in `app/main.py`. Structured logging via `app/logging_config.py`.
No `print()`. Log levels: debug/info/warning/error.

### Input Validation at Boundaries
All CLI argument validation lives in `app/cli/arg_parser.py`. Fail fast with clear messages.

### Maximum File Length — 300 Lines
Split when exceeded.

### Naming
- Files: `snake_case`
- Classes: `PascalCase`
- Functions/methods/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Security Baseline
No secrets committed. Validate user input at boundaries.

### No God Classes
One responsibility per class. Current split:
- `QrOptions` — DTO
- `QrGenerator` — QR creation
- `CanvasComposer` — canvas layout
- `parse_args` — CLI parsing/validation
- `main.run` — orchestration only

### Self-Describing Classes
N/A for this scope (no cross-cutting field iteration).

---

## Python Rules

### pyproject.toml as single source of truth
All tool config (ruff, mypy, pytest) lives in `pyproject.toml`. `uv.lock` is committed.

### Linting + Type Checking
- `uv run ruff check`
- `uv run ruff format --check`
- `uv run mypy app`

### Type Hints on Public APIs
All public functions and methods have typed parameters + return types.

### Centralized Configuration
`app/config/settings.py` reads env vars. No scattered `os.getenv()`.

### Tests Mandatory + Isolated
pytest. No network. Use tmp dirs / fixtures.

### Mocking with `spec=`
If MagicMock is used, always pass `spec=ClassName`.

### Required Batch Files
- `start.bat` — runs example
- `qr-create.bat` — CLI entry
- `install.bat`, `update.bat`
- `tools/run_tests.bat`, `tools/run_integration_tests.bat`

### Structured Logging
`logging` module configured in `app/logging_config.py`. Used consistently across modules.
