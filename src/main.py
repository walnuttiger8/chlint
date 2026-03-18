import logging

import core
import rules

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("rules")


def exec_with_rules(query: str, rule_types: list[type[core.BaseRule]]) -> None:
    root = core.parse(query)
    for rule_type in rule_types:
        rule = rule_type()
        rule.visit(root)

        result = rule.result()
        logger.info("[%s] triggered %s", rule_type.__name__, result.triggered)


def main() -> None:
    query = """
            select *
                 , 1               as literal_one
                 , 1 + literal_one as literal_result
            from yandex_tracker.issues i
                     left join yandex_tracker.issue_tracker it on it.issue = i.issue
            where true
              and is_closed
              and issue_type not in ('appeal', 'a_note')
              and issue_type not in ('appeal', 'a_note') \
            """
    rule_types = rules.load_all()
    exec_with_rules(query, rule_types)


if __name__ == "__main__":
    main()
