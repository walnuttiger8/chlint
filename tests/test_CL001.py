from src import main
from src.rules.CL001 import Rule


def _assert_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert diagnostics[0].triggered


def _assert_not_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert not diagnostics[0].triggered


def test_not_triggered_for_single_literal() -> None:
    _assert_not_triggered("select 1")


def test_duplicate_ints() -> None:
    _assert_triggered("select 1, 1")


def test_duplicate_strings() -> None:
    _assert_not_triggered("""
    select id
    , status = 'new' as is_finished
    from orders
    """)

    _assert_triggered("""
    select id
    , status = 'new' as is_finished
    , status = 'new' and price > 100 as is_high_priority
    from orders
    """)


def test_duplicate_tuples() -> None:

    _assert_not_triggered("""
    select id
    , status in ('new', 'pending') as is_finished
    from orders
    """)

    _assert_triggered("""
    select id
    , status in ('new', 'pending') as is_finished
    , status in ('new', 'pending') and price > 100 as is_high_priority
    from orders
    """)
