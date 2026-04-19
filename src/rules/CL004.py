import core


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


def _is_select_list_wildcard(expr: core.AstNode) -> bool:
    """Return whether expr is * or alias.* in the SELECT list (not * inside functions like count(*))."""
    return expr.value.startswith("QualifiedAsterisk") or expr.value.startswith("Asterisk")


class Rule(core.BaseRule):
    """Disallow SELECT-list wildcards (*, alias.*)."""

    def __init__(self) -> None:
        self._triggered = False

    def visit(self, node: core.AstNode) -> None:
        projections = _select_projection_expression_list(node)
        if projections is not None:
            for expr in projections.children:
                if _is_select_list_wildcard(expr):
                    self._triggered = True
                    break

        for child in node.children:
            self.visit(child)

    def result(self) -> core.Diagnostic:
        return core.Diagnostic(triggered=self._triggered, code="CL004")
