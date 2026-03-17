class AstNode:
    def __init__(self, value: str, children: list["AstNode"] | None = None) -> None:
        self.value = value
        self.children = children

    def __repr__(self) -> str:
        return f"AstNode({self.value})"
