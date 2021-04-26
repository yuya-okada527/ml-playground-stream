from utils.format_utils import format_datetime_string


def test_format_datetime_string():
    # テストデータ
    datetime_str = "2021-04-25 08:19:37,404"

    assert format_datetime_string(datetime_str) == "2021-04-25 08:19:37"