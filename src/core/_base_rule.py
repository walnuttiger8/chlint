import abc

from . import _ast_node


class BaseRule(abc.ABC):

    @abc.abstractmethod
    def visit(self, node: _ast_node.AstNode) -> None:
        pass

    @abc.abstractmethod
    def result(self) -> list[str]:
        pass
