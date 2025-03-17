from datetime import datetime

import pytest
from tests.helper import in_snip

from smllib.errors import UnsupportedChoiceValue
from smllib.sml.sml_value import build_sml_value


def test_sml_value() -> None:
    assert build_sml_value(None) is None
    assert build_sml_value(12) == 12
    assert build_sml_value(in_snip([1, [2, 1609466461]], pack_top=False)) == datetime(2021, 1, 1, 2, 1, 1)

def test_sml_value_with_unsupported_choice() -> None:
    with pytest.raises(UnsupportedChoiceValue) as e:
        build_sml_value(in_snip([2, 3], pack_top=False))
    assert e.value.type == 2
    assert str(e.value) == 'Unsupported type 0x02'
