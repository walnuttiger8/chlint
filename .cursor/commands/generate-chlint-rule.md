# Generate a chlint rule (TDD)

You are working in the **chlint** repository: a ClickHouse SQL linter built on the AST from `chdb` `EXPLAIN AST`. Follow the steps **in order**. Do not add rule or test code until the user explicitly confirms at step 4.

## Repository map

- Workflow and verification commands: `AGENTS.md`
- Rule contract: `src/core/_base_rule.py` — class `Rule`, methods `visit`, `result`, return `Diagnostic(triggered=..., code="CL00N")`
- AST node: `src/core/_ast_node.py`, parsing: `src/core/_parser.py`
- Rules: `src/rules/CL00N.py` — **exactly one** public class named `Rule`
- Auto-discovery: `src/rules/__init__.py` — any new `CL*.py` that defines `Rule` is picked up automatically; do not change the loader for a normal new rule
- Test examples: `main.exec_with_rules(query, [Rule])`, helpers `_assert_triggered` / `_assert_not_triggered` (see **Test layout** below); reference `tests/test_CL004.py` for preferred structure, `tests/test_CL001.py` / `tests/test_CL003.py` for older patterns
- AST and debugging: `.cursor/skills/clickhouse-query-ast/SKILL.md`; if the tree shape is unclear, use `chdb.query(f"EXPLAIN AST {query}")` and interpret the dump per that skill

## Constraints

- Python 3.13+, use `uv run …` for ruff, mypy, pytest (see `AGENTS.md`)
- Strict mypy, Ruff line length 120, avoid ad-hoc type relaxations unless necessary
- Rule module name: use the next free id — sort `src/rules/CL*.py` and take the next number after the maximum (for example after `CL003` use `CL004`)

### Test layout (mandatory for new rule tests)

- Imports: `import main` and `from rules.CL00N import Rule` (pytest `pythonpath` includes `src`; do **not** use `from src import …` in tests — it breaks `mypy .`).
- For every **bad → good** pair from step 3, use **one** test function that shows the fix in place:
  1. `_assert_triggered(<bad query>)`
  2. `_assert_not_triggered(<good query>)`
- Name tests by **behavior** (what is wrong / what is allowed), not `pair_1`, `pair_2`.
- **False-positive** or “allowed shape” cases with **no** violating query: a separate test with only `_assert_not_triggered` (no paired `_assert_triggered`) is fine.

---

## Step 1 — Understand what the user wants

Summarize in your reply:

- What counts as a **violation** (one sentence plus 1–2 natural-language examples)
- What is **not** a violation (boundaries to limit false positives)
- Whether this needs a **new** `CL00N` rule or changes to an existing one (if unsure, ask)

If the request is vague, ask **1–2 clarifying questions**, then continue.

---

## Step 2 — Example queries that violate the rule

Produce a set of ClickHouse SQL queries that are **invalid relative to the intended rule** (they must **trigger** the rule once it exists).

Requirements:

- SQL that parses cleanly enough for `chdb` / this repo’s parser (avoid syntax that breaks `EXPLAIN AST` unless the rule is specifically about parse errors)
- Cover the **main** case and **edge** cases (nesting, aliases, multiple SELECT items, etc., as relevant to the rule)

---

## Step 3 — Fixed query for each “bad” example

For **each** query from step 2, provide a pair: **bad** → **good** (the good query must not trigger the rule, or must reflect the agreed “good” practice — align with step 1).

---

## Step 4 — User confirmation

Show a compact table or numbered list of **bad / good** pairs.

**Stop.** Explicitly ask whether the user confirms the pairs and the violation definition, or what to change.

**Do not create** `tests/test_CL00N.py` or `src/rules/CL00N.py` until you get a positive answer.

---

## Step 5 — TDD: tests

After confirmation:

1. Add `tests/test_CL00N.py` (use the id from Constraints).
2. Follow **Test layout** in Constraints: `import main`, `from rules.CL00N import Rule`, local helpers `_assert_triggered` / `_assert_not_triggered` (same shape as in `tests/test_CL004.py`).
3. For each confirmed bad / good pair: **one** test containing **both** assertions in order: `_assert_triggered` on the bad query, then `_assert_not_triggered` on the good query. Add separate `_assert_not_triggered`-only tests only where there is no natural “bad” twin (false positives, allowed syntax).
4. Run **only the new tests** and confirm they **fail** without the rule implementation (or with a minimal stub if the rule file already exists — prefer tests first, then logic).

---

## Step 6 — Implement the rule

1. Add `src/rules/CL00N.py` with class `Rule` and diagnostic code `CL00N` in `result()`.
2. Walk the tree: recursive `visit` over `node.children`, predicates on `node.value` and structure (see existing `CL001`–`CL003`).
3. Drive to **green**: `uv run pytest tests/test_CL00N.py -q`

---

## Step 7 — Refactor and verify

- Remove duplication, improve readability, extract small pure helpers with a `_` prefix when helpful
- Do not change behavior that the tests encode
- Final checks from `AGENTS.md`:

```bash
uv run ruff check .
uv run mypy .
uv run pytest
```

Fix everything until all pass cleanly.

---

## Flow summary

Clarify intent → bad query examples → fixed pairs → **stop for confirmation** → tests (red; each pair: `_assert_triggered` then `_assert_not_triggered` in one test) → rule (green) → refactor → ruff + mypy + pytest.
