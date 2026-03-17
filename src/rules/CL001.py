import core


class Rule(core.BaseRule):
    """Duplicate literal."""

    def __init__(self) -> None:
        self._seen_literals: set[str] = set()
        self._duplicate_literals: set[str] = set()

    def visit(self, node: core.AstNode) -> None:
        if node.value.startswith("Literal"):
            if node.value in self._seen_literals:
                self._duplicate_literals.add(node.value)
            else:
                self._seen_literals.add(node.value)
        for child in node.children:
            self.visit(child)

    def result(self) -> core.Diagnostic:
        return core.Diagnostic(triggered=len(self._duplicate_literals) > 0)
