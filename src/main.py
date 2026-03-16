import core
import rules

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


def main() -> None:
    root = core.parse(query)

    for rule_type in rules.load_all():
        rule = rule_type()
        rule.visit(root)
        print(rule.result())


if __name__ == "__main__":
    main()
