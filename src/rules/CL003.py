import core

_MULTI_IF = "Function multiIf"
# multiIf is (cond, then)+ with a trailing else branch (at least three list items).
_MIN_MULTI_IF_LIST_LEN = 3


def _fingerprint(node: core.AstNode) -> str:
    child_prints = "".join(_fingerprint(child) for child in node.children)
    return f"{node.value}{child_prints}"


def _multi_if_condition_nodes(node: core.AstNode) -> list[core.AstNode]:
    if not node.value.startswith(_MULTI_IF):
        return []
    if len(node.children) != 1:
        return []
    args = node.children[0]
    if not args.value.startswith("ExpressionList"):
        return []
    ch = args.children
    if len(ch) < _MIN_MULTI_IF_LIST_LEN or len(ch) % 2 == 0:
        return []
    return [ch[i] for i in range(0, len(ch) - 1, 2)]


def _is_leaf_identifier(node: core.AstNode) -> bool:
    """Column refs alone are DRY aliases, not duplicated expression trees."""
    return node.value.startswith("Identifier") and not node.children


def _when_condition_subtree_fingerprints(cond: core.AstNode) -> set[str]:
    """Fingerprints of cond and descendants; nested CASE (multiIf) is one blob."""

    def collect(n: core.AstNode, out: set[str]) -> None:
        if not _is_leaf_identifier(n):
            out.add(_fingerprint(n))
        if n.value.startswith(_MULTI_IF):
            return
        for child in n.children:
            collect(child, out)

    found: set[str] = set()
    collect(cond, found)
    return found


def _projection_subtree_fingerprints(root: core.AstNode) -> set[str]:
    """Like WHEN fingerprints but descends into multiIf (SELECT expressions, not WHEN-only)."""

    def collect(n: core.AstNode, out: set[str]) -> None:
        if _is_leaf_identifier(n) or n.value.startswith("Literal"):
            return
        out.add(_fingerprint(n))
        for child in n.children:
            collect(child, out)

    found: set[str] = set()
    collect(root, found)
    return found


def _select_projection_expression_list(node: core.AstNode) -> core.AstNode | None:
    """First ExpressionList of a SelectQuery that is the SELECT list (skips WITH ...)."""
    if not node.value.startswith("SelectQuery"):
        return None
    for child in node.children:
        if not child.value.startswith("ExpressionList"):
            continue
        if any(c.value.startswith("WithElement") for c in child.children):
            continue
        return child
    return None


class Rule(core.BaseRule):
    """Duplicate expression inside CASE WHEN conditions (including shared sub-expressions)."""

    def __init__(self) -> None:
        self._seen_subtrees: set[str] = set()
        self._triggered = False

    def visit(self, node: core.AstNode) -> None:
        for cond in _multi_if_condition_nodes(node):
            fps = _when_condition_subtree_fingerprints(cond)
            if not self._triggered and not self._seen_subtrees.isdisjoint(fps):
                self._triggered = True
            self._seen_subtrees |= fps

        projections = _select_projection_expression_list(node)
        if projections is not None:
            seen_in_select: set[str] = set()
            for expr in projections.children:
                fps = _projection_subtree_fingerprints(expr)
                if not self._triggered and not seen_in_select.isdisjoint(fps):
                    self._triggered = True
                seen_in_select |= fps

        for child in node.children:
            self.visit(child)

    def result(self) -> core.Diagnostic:
        return core.Diagnostic(triggered=self._triggered, code="CL003")
