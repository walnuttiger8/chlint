from src import main
from src.rules.CL002 import Rule


def _assert_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert diagnostics[0].triggered


def _assert_not_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert not diagnostics[0].triggered


def test_not_triggered_for_literal_without_plus() -> None:
    _assert_not_triggered("select 1")


def test_not_triggered_for_addition_of_identifiers() -> None:
    _assert_not_triggered("""
    select a + b
    from t
    """)


def test_triggered_for_magic_number_in_where_clause() -> None:
    _assert_triggered("""
    select id
    from t
    where id > 100
    """)

    _assert_not_triggered("""
    with 100 as _new_threshold
    select id
    from t
    where id > _new_threshold
    """)
