from . import _ast_node


def print_tree(node: _ast_node.AstNode, indent=0):
    print("  " * indent + node.value)
    for c in node.children:
        print_tree(c, indent + 1)
