from src import main
from src.rules.CL001 import Rule


def test_exec_with_rules_smoke() -> None:
    r = main.exec_with_rules("select 1", [Rule])
    assert not r[0].triggered
