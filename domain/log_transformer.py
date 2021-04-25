import abc
from domain.enums import LogType
from typing import Dict


class Transformer(abc.ABC):

    def __init__(self, separator: str) -> None:
        super().__init__()
        self._separator = separator

    def transform(self, log_dict: Dict[str, str]) -> str:
        raise NotImplementedError()


class CoreApiAppTransformer(Transformer):

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

        return self._separator.join(values)


class CoreApiAccessTransformer(Transformer):

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
        values = [str(log_dict.get(name)) for name in self.__COLUMN_NAMES]

        return self._separator.join(values)


def create_transformer(log_type: LogType) -> Transformer:

    if log_type == LogType.CORE_API_APP:
        return CoreApiAppTransformer()


    raise ValueError(f"{log_type}は未実装のタイプです")