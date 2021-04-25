from service.extract_service import extract_logs_service
from infra.object_storage_repository import create_object_storage_repository

def extract_logs(event, context):

    # ログ取得先をAttributesから取得
    bucket_name = event["attributes"]["bucketId"]
    object_key = event["attributes"]["objectId"]

    # JSON出ない場合、スキップ
    if not object_key.endswith(".json"):
        return

    # リポジトリを取得
    repository = create_object_storage_repository()

    # データを取得
    extract_logs_service(
        bucket_name=bucket_name,
        object_key=object_key,
        repository=repository
    )


def load_to_gcs(event, context):

    print("event: {event}")
