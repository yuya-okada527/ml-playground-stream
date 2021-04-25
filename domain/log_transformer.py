import json
import abc
from typing import Dict
from utils import csv_utils


class LogTransformer(abc.ABC):

    def __init__(self, separator: str) -> None:
        super().__init__()
        self._separator = separator

    def transform(self, log_dict: Dict[str, str]) -> str:
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

    def transform(self, log_dict: Dict[str, str]) -> str:
        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return csv_utils.make_record(values, self._separator)


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

    def transform(self, log_dict: Dict[str, str]) -> str:
        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return csv_utils.make_record(values, self._separator)


class UserFeedbackLikeSimilarMovieTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator=separator)
        self.__JSON_FIELDS = [
            "movie_id",
            "model_type",
            "like"
        ]

    def transform(self, log_dict: Dict[str, str]) -> str:

        # 一階層目の項目を取得
        values = [
            log_dict.get("Time")
        ]

        # JSONでログ出力されている項目を取得
        json_message = json.loads(log_dict.get("Message"))
        for field in self.__JSON_FIELDS:
            values.append(json_message.get(field))

        return csv_utils.make_record(values, self._separator)


class MovieSimModelUsedCountTransformer(LogTransformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__(separator)
        self.__COLUMN_NAMES = [
            "Time",
            "Message"
        ]

    def transform(self, log_dict: Dict[str, str]) -> str:
        pass
