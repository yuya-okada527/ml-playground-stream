import pytest
from domain.enums import LogType
from service.extract_service import _extract_log_type, _is_not_app_log, _make_message, _make_object_key, _parse_ltsv

def test_parse_ltsv():

    # テストデータ
    ltsv_log = "Key1:Value1\tKey2:Value2"

    # 期待値
    expected = {
        "Key1": "Value1",
        "Key2": "Value2"
    }

    # 検証
    assert _parse_ltsv(ltsv_log) == expected


def test_extract_log_type():

    # テストデータ
    log_dict = {
        "Level": "info",
        "Type": "UserFeedbackLikeSimilarMovie",
        "Time": "",
        "Message": ""
    }

    # 期待値
    expected = LogType.USER_FEEDBACK_LIKE_SIM_MOVIE

    # 検証
    assert _extract_log_type(log_dict) == expected


def test_is_not_app_log_false():

    # テストデータ
    log_message = "Level:info\tType:UserFeedbackLikeSimilarMovie"

    # 検証
    assert _is_not_app_log(log_message) == False


def test_is_not_app_log_true():

    # テストデータ
    log_message = "LEVEL:info\tType:UserFeedbackLikeSimilarMovie"

    # 検証
    assert _is_not_app_log(log_message) == True

def test_is_not_app_log_none():

    # テストデータ
    log_message = None

    # 検証
    assert _is_not_app_log(log_message) == True


def test_make_object_key():

    # テストデータ
    table_name = "table"
    object_id = "stdout/2021/04/21/001.json"
    chunk_num = 3

    # 期待値
    expected = "table/stdout/2021/04/21/001/3.tsv"

    assert _make_object_key(table_name, object_id, chunk_num) == expected


@pytest.mark.parametrize("records, columns, separator, expected", [
    (["value1,value2", "value1,value2"], ["column1", "column2"], ",", "column1,column2\nvalue1,value2\nvalue1,value2")
])
def test_make_message(records, columns, separator, expected):
    assert _make_message(records, columns, separator) == expected
