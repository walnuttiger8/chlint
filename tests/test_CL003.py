import main
from rules.CL003 import Rule


def _assert_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert diagnostics[0].triggered


def _assert_not_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert not diagnostics[0].triggered


def test_duplicate_when_subexpression_across_two_case() -> None:
    _assert_triggered("""
        select
            case when 1 + 1 in (2, 3, 4) then 'yes' end,
            case when 1 + 1 in (2, 3, 4) and 2 + 2 in (4, 5) then 'no' end
    """)


def test_duplicate_full_predicate_two_case() -> None:
    _assert_triggered("""
        select
            case when 1 + 1 in (2, 3, 4) then 'a' end,
            case when 1 + 1 in (2, 3, 4) then 'b' end
    """)


def test_two_identical_when_in_one_case() -> None:
    _assert_triggered("select case when 1 then 2 when 1 then 3 else 4 end")


def test_no_duplicate_distinct_conditions() -> None:
    _assert_not_triggered("""
        select
            case when 1 + 1 in (2, 3, 4) then 'a' end,
            case when 2 + 2 in (4, 5, 6) then 'b' end
    """)


def test_single_case_no_duplicate() -> None:
    _assert_not_triggered("select case when 1 + 1 in (2, 3, 4) then 'yes' end")


def test_triggered_for_different_cols() -> None:
    _assert_triggered("""
        select now()
        , case
            when 1 + 1 in (2, 3, 4)
            then 'yes'
        end as first

        , case
            when 1 + 1 in (2, 3, 4)
            and 2 + 2 in (4, 5)
            then 'no'
        end as second
    """)

    _assert_not_triggered("""
        select now()
        , 1 + 1 in (2, 3, 4) as _flg
        , case
            when _flg
            then 'yes'
        end as first

        , case
            when _flg
            and 2 + 2 in (4, 5)
            then 'no'
        end as second
    """)


def test_triggered_for_simple_conditions() -> None:
    _assert_triggered("""
        select 1 + 1 > 0 as first
        , 1 + 1 > 0 and 2 + 2 = 4 as second
    """)

    _assert_not_triggered("""
        select 1 + 1 as _flg
        , _flg as first
        , _flg and 2 + 2 = 4 as second
    """)
