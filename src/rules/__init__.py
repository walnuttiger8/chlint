from importlib import import_module
from pathlib import Path

import core

RuleClass = type[core.BaseRule]


def load_all() -> list[RuleClass]:
    discovered: list[RuleClass] = []

    for path in sorted(Path(__file__).parent.glob("CL*.py")):
        module_name = path.stem
        module = import_module(f"{__name__}.{module_name}")
        rule_class: type[core.BaseRule] = getattr(module, "Rule", None)

        rule_class.__name__ = module_name

        if isinstance(rule_class, type) and issubclass(rule_class, core.BaseRule) and rule_class is not core.BaseRule:
            discovered.append(rule_class)

    return discovered


__all__ = ["load_all"]
