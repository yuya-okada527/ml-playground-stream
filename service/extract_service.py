from domain.enums import LogType
import json
from typing import Dict, Generator
from collections import defaultdict
from infra.object_storage_repository import ObjectStorageRepository


def extract_logs_service(
    bucket_name: str,
    object_key: str,
    repository: ObjectStorageRepository
) -> None:

    # データを取得
    data = repository.download_contents(
        bucket_name=bucket_name,
        key=object_key
    )

    # 1レコードずつ処理していく
    log_data = defaultdict(list)
    for log_message in _generate_app_log(data):
        # LTSVをパース
        log_dict = _parse_ltsv(log_message)

        # ログタイプを取得
        log_type = _extract_log_type(log_dict)

        # 取得できない場合スキップ
        if log_type is None:
            continue

        # ログタイプごとにデータを保持
        log_data[log_type].append(log_type.transformer.transform(log_dict))


def _is_not_app_log(log_message: str) -> bool:
    # Noneの場合、アプリログではない
    if log_message is None:
        return True
    return not log_message.startswith("Level")


def _generate_app_log(data: str) -> Generator[str, None, None]:

    for log in data.split("\n"):
        json_log = json.loads(log)
        log_message = json_log.get("textPayload")

        # アプリケーションログでない場合スキップ
        if _is_not_app_log(log_message):
            continue

        yield log_message


def _parse_ltsv(ltsv_log: str) -> Dict[str, str]:

    log_dict = {}
    for log_item in ltsv_log.split("\t"):
        column = log_item.split(":")
        log_dict[column[0]] = column[1]

    return log_dict


def _extract_log_type(log_dict: Dict[str, str]) -> LogType:

    log_type = log_dict.get("Type")

    return LogType.from_value(log_type)
