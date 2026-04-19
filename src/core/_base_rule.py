import abc
import dataclasses

from . import _ast_node


@dataclasses.dataclass(frozen=True)
class Diagnostic:
    triggered: bool
    code: str


class BaseRule(abc.ABC):

    @abc.abstractmethod
    def visit(self, node: _ast_node.AstNode) -> None:
        pass

    @abc.abstractmethod
    def result(self) -> Diagnostic:
        pass
