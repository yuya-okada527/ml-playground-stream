from datetime import datetime
from domain.log_transformer import CoreApiAppTransformer, create_transformer
from domain.enums import LogType


def test_create_transformer_core_api_app():
    actual = create_transformer(LogType.CORE_API_APP)
    assert isinstance(actual, CoreApiAppTransformer)


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

    assert transformer.transform(log_dict) == expected