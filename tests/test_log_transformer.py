import json
import time
from datetime import datetime
from domain.log_transformer import CoreApiAccessTransformer, CoreApiAppTransformer, MovieSimModelUsedCountTransformer, UserFeedbackLikeSimilarMovieTransformer, _convert_datetime_format

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
    assert transformer(log_dict) == expected


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
    assert transformer(log_dict) == expected


def test_user_feedback_transformer_transform():

    # テストデータ
    transformer = UserFeedbackLikeSimilarMovieTransformer()
    date_time = datetime.now().isoformat()
    log_dict = {
        "Level": "info",
        "Time": date_time,
        "Message": json.dumps({
            "movie_id": 0,
            "model_type": "tmdb-sim",
            "like": 0
        })
    }

    # 期待値
    expected = f"{date_time}\t0\ttmdb-sim\t0"

    # 検証
    assert transformer(log_dict) == expected


def test_movie_sim_model_used_count_transformer():

    # テストデータ
    transformer = MovieSimModelUsedCountTransformer()
    date_time = datetime.now().isoformat()
    log_dict = {
        "Level": "info",
        "Time": date_time,
        "Message": "tmdb-sim"
    }

    # 期待値
    expected = f"{date_time}\ttmdb-sim"

    # 検証
    assert transformer(log_dict) == expected


def test_convert_datetime_format():

    log_dict = {
        "Time": "2021-04-25 08:19:37,404"
    }

    expected = {
        "Time": "2021-04-25 08:19:37"
    }

    assert _convert_datetime_format(log_dict) == expected