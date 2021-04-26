from datetime import datetime


def format_datetime_string(datetime_str: str) -> str:
    # 例: 2021-04-25 08:19:37,404
    return datetime_str.split(",")[0]
