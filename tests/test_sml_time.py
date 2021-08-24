from datetime import datetime

from smllib.sml import SmlTime


def test_sml_time():
    assert SmlTime.from_list(None) is None
    assert SmlTime.from_list([1, 253]) == 253
    assert SmlTime.from_list([2, 1609466461]) == datetime(2021, 1, 1, 3, 1, 1)

    assert SmlTime.from_list([3, [1609466461, 120,  0]]) == datetime(2021, 1, 1, 5, 1, 1)
    assert SmlTime.from_list([3, [1622509261, 120, 60]]) == datetime(2021, 6, 1, 6, 1, 1)
    assert SmlTime.from_list([3, [1622509261, 120, 30]]) == datetime(2021, 6, 1, 5, 31, 1)
