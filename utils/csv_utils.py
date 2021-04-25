from typing import Any, List


def make_record(values: List[Any], separator: str) -> str:

    value_strings = []
    for v in values:
        if v is None:
            v = ""
        v = str(v)
        v = v.replace(separator, "")
        value_strings.append(v)

    return separator.join(value_strings)