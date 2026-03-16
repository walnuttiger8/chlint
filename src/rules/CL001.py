import core


class Rule(core.BaseRule):
    """
    Duplicate literal
    """

    def __init__(self):
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

    def result(self) -> list[str]:
        return list(self._duplicate_literals)
