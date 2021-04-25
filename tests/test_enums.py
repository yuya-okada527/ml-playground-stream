from domain.enums import LogType
import pytest


@pytest.mark.parametrize("value", [
    e.value for e in LogType
])
def test_log_type_from_value_success(value):

    assert isinstance(LogType.from_value(value), LogType)

@pytest.mark.parametrize("value", [
    "DifferenetValue",
    None
])
def test_log_type_from_value_failure(value):

    assert LogType.from_value(value) is None
