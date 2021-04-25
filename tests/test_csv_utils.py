from utils.csv_utils import make_record
import pytest

@pytest.mark.parametrize("values, separator, expected", [
    (["str", 0, 0.1, False, True], ",", "str,0,0.1,False,True"),
    (["hoge", None, 0, False, None], "\t", "hoge\t\t0\tFalse\t"),
    (["hoge,fuga", "hogo"], ",", "hogefuga,hogo")
])
def test_make_record(values, separator, expected):
    assert make_record(values, separator) == expected
