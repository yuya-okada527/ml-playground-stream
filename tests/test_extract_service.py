from domain.enums import LogType
from service.extract_service import _extract_log_type, _is_not_app_log, _parse_ltsv

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