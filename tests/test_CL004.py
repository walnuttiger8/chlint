import main
from rules.CL004 import Rule


def _assert_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert diagnostics[0].triggered


def _assert_not_triggered(query: str) -> None:
    diagnostics = main.exec_with_rules(query, [Rule])
    assert not diagnostics[0].triggered


def test_select_star_from_table() -> None:
    _assert_triggered("SELECT * FROM users")
    _assert_not_triggered("SELECT id, name FROM users")


def test_qualified_table_star() -> None:
    _assert_triggered("SELECT u.* FROM users AS u")
    _assert_not_triggered("SELECT u.id, u.name FROM users AS u")


def test_column_list_with_trailing_star() -> None:
    _assert_triggered("SELECT id, * FROM users")
    _assert_not_triggered("SELECT id, name, email FROM users")


def test_star_over_subquery() -> None:
    _assert_triggered("SELECT * FROM (SELECT id, name FROM users) AS s")
    _assert_not_triggered("SELECT s.id, s.name FROM (SELECT id, name FROM users) AS s")


def test_star_with_join() -> None:
    _assert_triggered(
        """
        SELECT *
        FROM orders AS o
        INNER JOIN customers AS c ON o.customer_id = c.id
        """,
    )
    _assert_not_triggered(
        """
        SELECT o.id, o.amount, c.id, c.name
        FROM orders AS o
        INNER JOIN customers AS c ON o.customer_id = c.id
        """,
    )


def test_star_except_still_counts_as_star() -> None:
    _assert_triggered("SELECT * EXCEPT (password) FROM users")
    _assert_not_triggered("SELECT id, name, email FROM users")


def test_star_inside_cte() -> None:
    _assert_triggered(
        """
        WITH cte AS (SELECT * FROM users)
        SELECT cte.id, cte.name FROM cte
        """,
    )
    _assert_not_triggered(
        """
        WITH cte AS (SELECT id, name FROM users)
        SELECT cte.id, cte.name FROM cte
        """,
    )


def test_star_on_cte_reference() -> None:
    _assert_triggered(
        """
        WITH cte AS (SELECT id, name FROM users)
        SELECT * FROM cte
        """,
    )
    _assert_not_triggered(
        """
        WITH cte AS (SELECT id, name FROM users)
        SELECT cte.id, cte.name FROM cte
        """,
    )


def test_star_in_multiple_ctes() -> None:
    _assert_triggered(
        """
        WITH a AS (SELECT * FROM users), b AS (SELECT * FROM orders)
        SELECT a.id, b.amount FROM a CROSS JOIN b
        """,
    )
    _assert_not_triggered(
        """
        WITH a AS (SELECT id FROM users), b AS (SELECT amount FROM orders)
        SELECT a.id, b.amount FROM a CROSS JOIN b
        """,
    )


def test_qualified_star_inside_cte() -> None:
    _assert_triggered(
        """
        WITH cte AS (SELECT u.* FROM users AS u)
        SELECT 1 FROM cte
        """,
    )
    _assert_not_triggered(
        """
        WITH cte AS (SELECT u.id, u.name FROM users AS u)
        SELECT 1 FROM cte
        """,
    )


def test_star_inside_function_not_select_list_wildcard() -> None:
    _assert_not_triggered("SELECT count(*) FROM users")


def test_literal_select() -> None:
    _assert_not_triggered("SELECT 1")
