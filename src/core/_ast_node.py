class AstNode:
    def __init__(self, value: str, children: list["AstNode"] | None = None) -> None:
        self.value: str = value
        self.children: list[AstNode] = [] if children is None else children

    def __repr__(self) -> str:
        return f"AstNode({self.value})"
