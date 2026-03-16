class AstNode:
    def __init__(self, value: str, children: list["AstNode"] = None):
        self.value = value
        self.children = children

    def __repr__(self):
        return f"AstNode({self.value})"
