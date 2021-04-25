import abc
from domain.enums import LogType
from typing import Dict


class Transformer(abc.ABC):

    def transform(self, log_dict: Dict[str, str]) -> str:
        raise NotImplementedError()


class CoreApiAppTransformer(Transformer):

    def __init__(self, separator: str = "\t") -> None:
        super().__init__()
        self.__separator = separator
        self.__COLUMN_NAMES = [
            "Level",
            "Time",
            "File",
            "Message"
        ]

    def transform(self, log_dict: Dict[str, str]) -> str:

        values = [log_dict.get(name) for name in self.__COLUMN_NAMES]

        return self.__separator.join(values)


def create_transformer(log_type: LogType) -> Transformer:

    if log_type == LogType.CORE_API_APP:
        return CoreApiAppTransformer()


    raise ValueError(f"{log_type}は未実装のタイプです")