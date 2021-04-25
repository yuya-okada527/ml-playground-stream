from domain.enums import LogType
from core.config import CoreSettings
import json
from google.cloud import pubsub
from more_itertools import chunked
from typing import Dict, Generator, List
from collections import defaultdict
from infra.object_storage_repository import ObjectStorageRepository


CHUNK_SIZE = 100
SETTINGS = CoreSettings()


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

    # Pub/Subクライアントを初期化
    client = pubsub.PublisherClient()

    # 1レコードずつ処理していく
    log_data: Dict[LogType, List[str]] = defaultdict(list)
    for log_message in _generate_app_log(data):
        # LTSVをパース
        log_dict = _parse_ltsv(log_message)

        # ログタイプを取得
        log_type = _extract_log_type(log_dict)

        # 取得できない場合スキップ
        if log_type is None:
            continue

        # ログタイプごとにデータを保持
        log_data[log_type].append(log_type.transform(log_dict))

    # チャンクごとに、メッセージ化
    for log_type, records in log_data.items():
        for i, record_chunk in enumerate(chunked(records, CHUNK_SIZE)):
            # オブジェクトのキーを作成
            object_key = _make_object_key(
                table_name=log_type.table_name,
                object_id=object_key,
                chunk_num=i
            )

            # メッセージを作成
            message = _make_message(
                records=record_chunk,
                columns=log_type.columns,
                separator=log_type.transform.separator
            )

            # メッセージを公開
            topic = client.topic_path(SETTINGS.gcp_project_id, "load-to-gcs-topic")
            client.publish(
                topic=topic,
                data=message,
                bucket="ml-playground-log-table-bucket",
                object_key=object_key
            )


def _make_object_key(table_name: str, object_id: str, chunk_num: int) -> str:
    # JSON拡張子を削除
    object_id_without_extension = object_id[:-5]
    return f"{table_name}/{object_id_without_extension}/{chunk_num}.tsv"


def _make_message(records: List[str], columns: List[str], separator: str) -> str:
    header = separator.join(columns)
    return header + "\n" + "\n".join(records)


def _is_not_app_log(log_message: str) -> bool:
    # Noneの場合、アプリログではない
    if log_message is None:
        return True
    return not log_message.startswith("Level")


def _generate_app_log(data: str) -> Generator[str, None, None]:

    for log in data.split("\n"):

        # 空のログはスキップ
        if not log:
            continue

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
