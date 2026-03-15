# AGENTS.md

Operational guide for coding agents working in this repository.

## 1) Repository Snapshot
- Language: Python (requires `>=3.13`).
- Package manager and task runner: `uv`.
- Project layout is `src/`-based (`src/main.py`).
- Primary configuration is in `pyproject.toml`.
- Current dev tools already configured: `ruff`, `mypy`, `pytest`.

## 2) Source of Truth
- Treat `pyproject.toml` as canonical for tool behavior.
- Treat `.gitignore` as canonical for ignored paths.
- There is no separate `pytest.ini`, `mypy.ini`, `ruff.toml`, `tox.ini`, or `setup.cfg`.
- If this file conflicts with tool config, follow tool config.

## 3) Cursor / Copilot Rules
Checked on 2026-03-15:
- `.cursorrules`: not present.
- `.cursor/rules/`: not present.
- `.github/copilot-instructions.md`: not present.
Implication:
- No editor-specific rule files are currently enforced.
- If any of these files are added later, treat them as mandatory and update this document.

## 4) Environment Setup
- Verify Python: `python3 --version`
- Verify uv: `uv --version`
- Sync environment: `uv sync`
- Run commands in environment: `uv run <command>`
One-time bootstrap:
```bash
uv sync
```

## 5) Build / Run / Lint / Test Commands
### Run / Smoke
- Run app entrypoint: `uv run python src/main.py`
- Run as module: `uv run python -m src.main`

### Lint and Format (Ruff)
- Lint all files: `uv run ruff check .`
- Lint and auto-fix: `uv run ruff check . --fix`
- Check formatting only: `uv run ruff format . --check`
- Apply formatting: `uv run ruff format .`

### Type Check (Mypy)
- Type-check project: `uv run mypy .`
- Type-check one file: `uv run mypy src/main.py`

### Tests (Pytest)
- Run full suite: `uv run pytest`
- Quiet output: `uv run pytest -q`
- Stop on first failure: `uv run pytest -x`
- Verbose failures summary: `uv run pytest -ra`

### Single-Test Execution (Important)
- Run one file: `uv run pytest tests/test_example.py`
- Run one test function: `uv run pytest tests/test_example.py::test_happy_path`
- Run one test method: `uv run pytest tests/test_example.py::TestParser::test_happy_path`
- Run one test class: `uv run pytest tests/test_example.py::TestParser`
- Filter by name: `uv run pytest -k "happy_path and not slow"`
- Show stdout/stderr: `uv run pytest -s tests/test_example.py::test_happy_path`

### Optional Coverage
- Add plugin: `uv add --dev pytest-cov`
- Run coverage: `uv run pytest --cov=. --cov-report=term-missing`

## 6) Tooling Constraints from pyproject.toml
- Ruff line length is set to `120` (not 88).
- Ruff lint rule set is broad: `select = ["ALL"]` with explicit ignores.
- Mypy runs in strict mode: `[tool.mypy] strict = true`.
- Write code that is fully typed and strict-mypy clean.
- Keep lines <=120 chars unless unavoidable.
- Do not rely on import sorting by Ruff (`I` rules are ignored), but still keep imports tidy.

## 7) Code Style Guidelines
### General
- Favor clear, explicit, boring code over clever abstractions.
- Keep functions small and focused on one responsibility.
- Avoid hidden side effects; make data flow obvious.

### Formatting
- Use 4-space indentation.
- Keep line length at or below 120 chars.
- Prefer trailing commas in multiline literals/calls to reduce diff churn.
- Prefer one statement per line.

### Imports
- Use absolute imports by default.
- Group imports in order: stdlib, third-party, local.
- Separate groups with one blank line.
- Do not use wildcard imports (`from module import *`).
- Remove unused imports promptly.

### Typing
- Type annotate all new/modified function parameters and return values.
- Prefer built-in generics (`list[str]`, `dict[str, int]`).
- Use `X | None` style unions where appropriate.
- Prefer `TypedDict`/`dataclass`/`Protocol` over unstructured `dict` and `Any`.
- Keep `Any` usage minimal and local; document why when unavoidable.

### Naming
- Modules/files: `snake_case.py`
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Internal helpers: prefix with `_`

### Docstrings
- Add docstrings for public modules, classes, and non-trivial public functions.
- Start with a short imperative summary line.
- Include args/returns/raises when behavior is non-obvious.

### Error Handling
- Fail fast with actionable messages.
- Catch specific exceptions, not broad `Exception` unless re-raising with context.
- Never silently swallow errors.
- Preserve tracebacks when wrapping errors: `raise NewError(...) from exc`.
- Validate input at boundaries (CLI args, file I/O, env vars, external data).

### Logging and CLI Output
- Use `logging` for diagnostics in reusable/library code.
- Use `print` only for user-facing CLI output.
- Keep error output concise and actionable.

### Testing
- Put tests in `tests/`.
- Name files `test_*.py`.
- Name tests by behavior (what), not implementation (how).
- Use Arrange / Act / Assert structure.
- Cover at least one failure path for non-trivial logic.

## 8) Change Management for Agents
- Keep diffs minimal and focused on the requested task.
- Do not add dependencies unless necessary for the task.
- When adding tools/dependencies, update `pyproject.toml` and lockfile.
- Do not rewrite unrelated files just for style consistency.
- Preserve existing behavior unless a change is explicitly requested.

## 9) Quick Agent Checklist
- Read `pyproject.toml` before implementing.
- Implement minimal code changes.
- Run targeted checks first, then broader checks.
- At minimum after edits, run: `uv run ruff check .`, `uv run mypy .`, and `uv run pytest`.
- For test-related changes, include at least one single-test command in handoff notes.
