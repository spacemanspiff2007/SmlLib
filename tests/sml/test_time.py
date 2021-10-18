from datetime import datetime

import pytest

from smllib.errors import UnsupportedType
from smllib.sml.sml_time import build_time


def test_sml_time():
    assert build_time(None) is None
    assert build_time([1, 253]) == 253
    assert build_time([2, 1609466461]) == datetime(2021, 1, 1, 2, 1, 1)

    assert build_time([3, [1609466461, 120,  0]]) == datetime(2021, 1, 1, 4, 1, 1)
    assert build_time([3, [1622509261, 120, 60]]) == datetime(2021, 6, 1, 4, 1, 1)
    assert build_time([3, [1622509261, 120, 30]]) == datetime(2021, 6, 1, 3, 31, 1)


def test_exception():
    with pytest.raises(UnsupportedType) as e:
        build_time([5, 55])
    assert e.value.type == 5
    assert str(e.value) == 'Unsupported type 0x05'
