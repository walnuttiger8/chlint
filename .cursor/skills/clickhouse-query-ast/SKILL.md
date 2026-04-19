---
name: clickhouse-query-ast
description: Fetches ClickHouse query AST as text via chdb EXPLAIN AST, explains the line-oriented dump format, and how to build a tree from it. Use when debugging lint rules on AST, writing AST-focused tests, inspecting SELECT/WHERE/JOIN structure, or when the user mentions chdb, EXPLAIN AST, query AST, or AST tree generation in Python.
---

# ClickHouse query AST with chdb

## When to use

- Inspect how the engine represents a query (`SelectQuery`, `Function`, `Identifier`, etc.).
- Debug or author **lint rules** that walk this repo’s parsed AST.
- Compare how different SQL surface syntax maps to the same tree (for example `CASE` vs `multiIf`).

## Generate AST text (chdb)

Dependency: `chdb`.

```python
import chdb

query = "SELECT 1"
ast_text = str(chdb.query(f"EXPLAIN AST {query}"))
print(ast_text)
```

## Text dump format

- One node per line; **leading spaces** encode nesting depth.
- A line with less or equal indentation than the current parent ends that parent’s subtree (walk up the stack).
- Node labels match the engine dump; exact shapes depend on the bundled ClickHouse version inside `chdb`.
- Lines may be wrapped in **double quotes**; strip outer `"` per line if you parse manually.
