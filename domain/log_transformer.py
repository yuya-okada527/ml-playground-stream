import json
import abc
from typing import Dict
from utils import csv_utils, format_utils


class LogTransformer(abc.ABC):

    def __init__(self, separator: str) -> None:
        super().__init__()
        self.separator = separator

    def __call__(self, log_dict: Dict[str, str]) -> str:
        raise NotImplementedError()


class CoreApiAppTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator=separator)
        self.__COLUMN_NAMES = [
            "Level",
            "Time",
            "File",
            "Message"
        ]

    def __call__(self, log_dict: Dict[str, str]) -> str:

        # 日時データをフォーマット
        log_dict = _convert_datetime_format(log_dict)

        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return csv_utils.make_record(values, self.separator)


class CoreApiAccessTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator=separator)
        self.__COLUMN_NAMES = [
            "Time",
            "ProcessTime",
            "Client",
            "Method",
            "Path",
            "Query",
            "StatusCode"
        ]

    def __call__(self, log_dict: Dict[str, str]) -> str:

        # 日時データをフォーマット
        log_dict = _convert_datetime_format(log_dict)


        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return csv_utils.make_record(values, self.separator)


class UserFeedbackLikeSimilarMovieTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator=separator)
        self.__JSON_FIELDS = [
            "movie_id",
            "model_type",
            "like"
        ]

    def __call__(self, log_dict: Dict[str, str]) -> str:

        # 日時データをフォーマット
        log_dict = _convert_datetime_format(log_dict)

        # 一階層目の項目を取得
        values = [
            log_dict.get("Time")
        ]

        # JSONでログ出力されている項目を取得
        json_message = json.loads(log_dict.get("Message"))
        for field in self.__JSON_FIELDS:
            values.append(json_message.get(field))

        return csv_utils.make_record(values, self.separator)


class MovieSimModelUsedCountTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator)
        self.__COLUMN_NAMES = [
            "Time",
            "Message"
        ]

    def __call__(self, log_dict: Dict[str, str]) -> str:
        # 日時データをフォーマット
        log_dict = _convert_datetime_format(log_dict)

        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return csv_utils.make_record(values, self.separator)


def _convert_datetime_format(log_dict: Dict[str, str]) -> Dict[str, str]:
    if "Time" in log_dict:
        log_dict["Time"] = format_utils.format_datetime_string(log_dict["Time"])

    return log_dict