import logging

import core
import rules

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("rules")


def exec_with_rules(query: str, rule_types: list[type[core.BaseRule]]) -> list[core.Diagnostic]:
    root = core.parse(query)

    def _exec_rule(rule_type: type[core.BaseRule]) -> core.Diagnostic:
        rule = rule_type()
        rule.visit(root)

        return rule.result()

    diagnostics = [_exec_rule(rule_type) for rule_type in rule_types]

    return diagnostics


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
    diagnostics = exec_with_rules(query, rule_types)

    for diagnostic in diagnostics:
        if diagnostic.triggered:
            logger.info("[%s] triggered", diagnostic.code)


if __name__ == "__main__":
    main()
