# tests/helpers.py

import pendulum


def pdt(value: str) -> pendulum.DateTime:
    result = pendulum.parse(value)
    assert isinstance(result, pendulum.DateTime)
    return result
