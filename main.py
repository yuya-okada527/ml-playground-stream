from infra.object_storage_repository import create_object_storage_repository

def extract_logs(event, context):

    # ログ取得先をメッセージから取得
    bucket_name = event["attributes"]["bucketId"]
    object_key = event["attributes"]["objectId"]

    # JSON出ない場合、スキップ
    if not object_key.endswith(".json"):
        return

    # リポジトリを取得
    repository = create_object_storage_repository()

    # データを取得
    data = repository.download_contents(
        bucket_name=bucket_name,
        key=object_key
    )

    for log in data.split("\n"):
        print(log)
