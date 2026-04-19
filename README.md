# chlint

A linter for [ClickHouse](https://clickhouse.com/) SQL: it builds a query tree via `chdb` (`EXPLAIN AST`) and runs rules that walk the AST and emit diagnostics.

**Status:** early development (API and rule set may change).

## Features

- Parse query text into an AST using embedded ClickHouse (`chdb`).
- Rules live in `src/rules/CL*.py` as a `Rule` class; load them with `rules.load_all()`.
- Rule behavior is covered by tests under `tests/`.

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) for dependencies and running commands

## Install and run the sample

```bash
git clone https://github.com/walnuttiger8/chlint.git
cd chlint
uv sync
uv run python src/main.py
```

`src/main.py` runs a demo query and logs rule codes that triggered.

## Using from code

Imports (`import core`, `import rules`) expect the `src` directory on `PYTHONPATH` (same as `pytest` in `pyproject.toml`). From the repo root:

```bash
PYTHONPATH=src uv run python
```

Then in a REPL or script:

```python
import core
import rules

root = core.parse("SELECT 1 AS a, 1 AS b")
for Rule in rules.load_all():
    rule = Rule()
    rule.visit(root)
    d = rule.result()
    print(d.code, d.triggered)
```

For a full “parse and run every rule” loop, see `exec_with_rules` in [`src/main.py`](src/main.py).

## Rules

| Code      | Description                                                                                                                                                                       |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **CL001** | The same literal appears more than once in the tree (duplicate literals).                                                                                                         |
| **CL002** | Literals under a `Function` subtree (expression context) to flag magic numbers in expressions, not every literal in the query.                                                    |
| **CL003** | Duplicated expressions in `CASE` / `multiIf` conditions and overlapping sub-expressions across branches; also overlap of non-trivial sub-expressions between `SELECT` list items. |
| **CL004** | Disallow `*` and `alias.*` in the `SELECT` list (excluding `*` inside aggregates like `count(*)`).                                                                                |

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format . --check
uv run mypy .
uv run pytest
```

Agent-oriented conventions and the full command checklist: [AGENTS.md](AGENTS.md).

## License

There is no `LICENSE` file in this repository yet. Add one before publishing and update this section if needed.
