import time
from datetime import datetime
from domain.log_transformer import CoreApiAccessTransformer, CoreApiAppTransformer, UserFeedbackLikeSimilarMovieTransformer, create_transformer
from domain.enums import LogType


def test_create_transformer_core_api_app():
    actual = create_transformer(LogType.CORE_API_APP)
    assert isinstance(actual, CoreApiAppTransformer)

def test_create_transformer_core_api_access():
    actual = create_transformer(LogType.CORE_API_ACCESS)
    assert isinstance(actual, CoreApiAccessTransformer)


def test_create_transformer_user_feedback():
    actual = create_transformer(LogType.USER_FEEDBACK_LIKE_SIM_MOVIE)
    assert isinstance(actual, UserFeedbackLikeSimilarMovieTransformer)


def test_core_api_transformer_transform():

    # テスト準備
    transformer = CoreApiAppTransformer()
    time = datetime.now().isoformat()
    log_dict = {
        "Level": "info",
        "Time": time,
        "File": __file__,
        "Message": "message"
    }

    # 期待値
    expected = f"info\t{time}\t{__file__}\tmessage"

    # 検証
    assert transformer.transform(log_dict) == expected


def test_core_api_access_transformer_transform():

    # テスト準備
    transformer = CoreApiAccessTransformer()
    date_time = datetime.now().isoformat()
    process_time = time.time()
    log_dict = {
        "Time": date_time,
        "ProcessTime": process_time,
        "Client": "127.0.0.1",
        "Method": "GET",
        "Path": "/path",
        "Query": "key=value",
        "StatusCode": 200
    }

    # 期待値
    expected = f"{date_time}\t{process_time}\t127.0.0.1\tGET\t/path\tkey=value\t200"

    # 検証
    assert transformer.transform(log_dict) == expected
