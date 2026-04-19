# AGENTS.md

Operational guide for coding agents working in this repository.

## 1) Repository Snapshot
- Language: Python (`requires-python = ">=3.13"`).
- Package manager and runner: `uv`.
- Layout: `src/` package with runtime entrypoint in `src/main.py`.
- Core runtime dependency: `chdb`.
- Dev toolchain from `pyproject.toml`: `ruff`, `mypy`, `pytest`.

## 2) Source of Truth
- Treat `pyproject.toml` as canonical for lint/type/test behavior.
- Treat `.gitignore` as canonical for ignored/ephemeral files.
- There is no `ruff.toml`, `mypy.ini`, `pytest.ini`, `setup.cfg`, or `tox.ini`.
- If this document conflicts with tool config, follow the tool config.

## 3) Cursor / Copilot Rules
Checked on 2026-03-16:
- `.cursorrules`: not present.
- `.cursor/rules/`: not present.
- `.github/copilot-instructions.md`: not present.

Implications for agents:
- No editor-specific policy files are currently active.
- Re-check these paths before major edits because these files can be added later.
- If found, treat their instructions as mandatory and update this document.

## 4) Environment Setup
- Verify Python: `python3 --version`
- Verify uv: `uv --version`
- Bootstrap environment: `uv sync`
- Run any tool inside environment: `uv run <command>`

Recommended bootstrap sequence:
```bash
python3 --version
uv --version
uv sync
```

## 5) Build / Run / Lint / Test Commands

### Run / Smoke
- Run script entrypoint: `uv run python src/main.py` (puts `src/` on `sys.path` via script location, so `import core` works).
- Custom scripts from repo root: `PYTHONPATH=src uv run python your_script.py` (or run with cwd `src/`).

### Lint + Format (Ruff)
- Lint all files: `uv run ruff check .`
- Lint and auto-fix: `uv run ruff check . --fix`
- Check formatting only: `uv run ruff format . --check`
- Apply formatting: `uv run ruff format .`

### Type Checking (Mypy)
- Type-check full repo: `uv run mypy .`
- Type-check single file: `uv run mypy src/main.py`

### Tests (Pytest)
- Run full test suite: `uv run pytest`
- Quiet output: `uv run pytest -q`
- Stop on first failure: `uv run pytest -x`
- Show extra summary: `uv run pytest -ra`

### Single-Test Execution (Important)
Use these patterns whenever tests exist in `tests/`:
- One file: `uv run pytest tests/test_parser.py`
- One function: `uv run pytest tests/test_parser.py::test_parses_valid_query`
- One class: `uv run pytest tests/test_parser.py::TestParser`
- One test method: `uv run pytest tests/test_parser.py::TestParser::test_parses_valid_query`
- Name filter: `uv run pytest -k "parser and not slow"`
- Show print/debug output: `uv run pytest -s tests/test_parser.py::test_parses_valid_query`

Current repo status note:
- `tests/` currently has no tracked `test_*.py` files, so add tests before relying on commands above.

### Optional Coverage
- Add coverage plugin: `uv add --dev pytest-cov`
- Run coverage report: `uv run pytest --cov=. --cov-report=term-missing`

## 6) Codebase Structure (Quick Map)
- `src/main.py`: example CLI-style driver that parses SQL and runs all rules.
- `src/core/_parser.py`: wraps `chdb` `EXPLAIN AST` and constructs AST nodes.
- `src/core/_ast_node.py`: minimal AST node model.
- `src/core/_base_rule.py`: abstract contract for lint rules (`visit`, `result`).
- `src/rules/CL*.py`: concrete rule implementations discovered at runtime.
- `src/rules/__init__.py`: dynamic rule loader via `importlib` + file globbing.

## 7) Tooling Constraints from `pyproject.toml`
- Ruff line length is `120`.
- Ruff lint policy is broad: `select = ["ALL"]` with explicit ignores.
- Ruff import sorting rules (`I`) are ignored; keep imports tidy manually.
- Mypy strict mode is enabled (`strict = true`).
- New/changed code should pass strict mypy without local relaxations.

## 8) Code Style Guidelines

### General Design
- Prefer explicit, straightforward code over clever abstractions.
- Keep functions focused and side effects obvious.
- Preserve existing behavior unless change is requested.

### Imports
- Prefer absolute imports that match existing package layout.
- Order groups as: stdlib, third-party, local.
- Use one blank line between import groups.
- Avoid wildcard imports.
- Remove unused imports promptly.

### Formatting
- Use 4-space indentation.
- Keep lines at or below 120 chars.
- Prefer trailing commas in multiline constructs.
- Avoid packing multiple statements onto one line.

### Typing
- Add type hints for all new/modified function parameters and return values.
- Prefer built-in generic types (`list[str]`, `dict[str, int]`).
- Use `X | None` instead of `Optional[X]` unless context requires otherwise.
- Avoid `Any`; if unavoidable, keep scope narrow and justify it in code.
- Favor small, typed data structures (`dataclass`, `TypedDict`, `Protocol`) over loose dicts.

### Naming
- Modules/files: `snake_case.py`.
- Functions/variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Internal helpers: prefix with `_`.

### Docstrings and Comments
- Add docstrings for public modules/classes and non-trivial public functions.
- Start docstrings with a short imperative summary line.
- Keep comments for non-obvious intent, not for restating code.

### Error Handling
- Fail fast with actionable errors.
- Validate external inputs (CLI args, file I/O, query text boundaries).
- Catch specific exceptions only; avoid blanket `except Exception`.
- When wrapping errors, preserve traceback via `raise NewError(...) from exc`.

### Logging and Output
- Use `print` for user-facing CLI output.
- Prefer `logging` for reusable internals or diagnostic traces.
- Keep outputs concise and directly actionable.

## 9) Testing Guidance
- Place tests in `tests/` and name files `test_*.py`.
- Name tests by behavior (what), not implementation details (how).
- Follow Arrange / Act / Assert structure.
- Include failure-path tests for non-trivial logic.
- For parser/rule changes, prefer focused single-test runs first, then full suite.

## 10) Change Management for Agents
- Keep diffs minimal and task-focused.
- Do not refactor unrelated files opportunistically.
- Do not add dependencies unless required by the task.
- If dependencies change, update both `pyproject.toml` and `uv.lock`.
- Do not edit generated caches (`.mypy_cache`, `.ruff_cache`, `.pytest_cache`).

## 11) Agent Workflow Checklist
- Read `pyproject.toml` before implementing.
- Locate affected modules and keep edits local.
- Run targeted checks first (single file/test), then broader checks.
- Minimum post-edit validation: `uv run ruff check .`, `uv run mypy .`, `uv run pytest`.
- In handoff notes, include at least one concrete single-test command.

## Learned User Preferences

- When the user writes a request in Russian, answer in Russian for that exchange.

## Learned Workspace Facts

- Pytest is configured with `[tool.pytest.ini_options] pythonpath = ["src"]` in `pyproject.toml`, so `uv run pytest` resolves imports from `src/`.
- Ruff ignores rule `N999` for `tests/**/*.py` and `src/rules/**/*.py`, so `test_CL00N.py` and `CL00N.py` filenames stay valid for rule tests and rule modules.
- In chdb `EXPLAIN AST` text, SQL `CASE ... WHEN ...` is represented as `Function multiIf` with one `ExpressionList` child: alternating when-condition and then-result nodes, ending with an else branch.
- CL002 flags literals that appear under an AST `Function` subtree (expression context), not every literal in the query.
- Rule-focused tests live under `tests/` (for example `test_CL001.py`, `test_CL002.py`, `test_CL003.py`).
