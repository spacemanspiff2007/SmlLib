from datetime import datetime

import pytest

from smllib.errors import UnsupportedChoiceValue
from smllib.sml.sml_time import build_time
from tests.helper import in_snip


def test_sml_time():
    assert build_time(None) is None
    assert build_time(in_snip([1, 253], pack_top=False)) == 253
    assert build_time(in_snip([2, 1609466461], pack_top=False)) == datetime(2021, 1, 1, 2, 1, 1)

    assert build_time(in_snip([3, [1609466461, 120,  0]], pack_top=False)) == datetime(2021, 1, 1, 4, 1, 1)
    assert build_time(in_snip([3, [1622509261, 120, 60]], pack_top=False)) == datetime(2021, 6, 1, 4, 1, 1)
    assert build_time(in_snip([3, [1622509261, 120, 30]], pack_top=False)) == datetime(2021, 6, 1, 3, 31, 1)


def test_exception():
    with pytest.raises(UnsupportedChoiceValue) as e:
        build_time([in_snip(5), in_snip(55)])
    assert e.value.type == 5
    assert str(e.value) == 'Unsupported type 0x05'
