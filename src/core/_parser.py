import chdb  # type: ignore[import-untyped]

from . import _ast_node


def _remove_prefix_and_suffix(string: str, pattern: str) -> str:
    return string.removeprefix(pattern).removesuffix(pattern)


def _count_space_prefix(ast_row: str) -> int:
    i = 0
    depth = 0
    while i < len(ast_row) and ast_row[i].isspace():
        depth += 1
        i += 1

    return depth


def _parse(lines: list[tuple[int, str]]) -> _ast_node.AstNode:
    pos = 0
    n = len(lines)

    def parse_children(parent_level: int) -> list[_ast_node.AstNode]:
        nonlocal pos
        children = []

        while pos < n:
            level, value = lines[pos]

            if level <= parent_level:
                break

            pos += 1
            node = _ast_node.AstNode(value, parse_children(level))
            children.append(node)

        return children

    root_level, root_val = lines[pos]
    pos += 1

    root = _ast_node.AstNode(root_val)
    root.children = parse_children(root_level)

    return root


def parse(query: str) -> _ast_node.AstNode:
    ast_result = str(chdb.query(f"explain ast {query}"))

    rows = []

    for row in ast_result.split("\n"):
        if not row:
            continue

        clear_row = _remove_prefix_and_suffix(row, '"')

        depth = _count_space_prefix(clear_row)

        row_info = (depth, clear_row.strip())
        rows.append(row_info)

    return _parse(rows)
