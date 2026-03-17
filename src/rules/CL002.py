import core


class Rule(core.BaseRule):
    """Avoid 'magic' numbers in expressions."""

    def __init__(self) -> None:
        self._in_expression = False
        self._seen_literals: set[str] = set()

        self._triggered = False

    def visit(self, node: core.AstNode) -> None:
        if not self._in_expression:
            self._visit_not_in_expression(node)
        else:
            self._visit_in_expression(node)

    def _visit_in_expression(self, node: core.AstNode) -> None:
        if node.value.__contains__("Literal"):
            if node.value in self._seen_literals:
                self._triggered = True

            self._seen_literals.add(node.value)

        self._base_visit(node)

    def _visit_not_in_expression(self, node: core.AstNode) -> None:
        if node.value.__contains__("Function plus"):
            self._in_expression = True

        self._base_visit(node)

        self._in_expression = False

    def _base_visit(self, node: core.AstNode) -> None:
        for child in node.children:
            self.visit(child)

    def result(self) -> core.Diagnostic:
        return core.Diagnostic(triggered=self._triggered)
