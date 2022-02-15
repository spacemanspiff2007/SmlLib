import pytest

from smllib.errors import WrongValueType
from smllib.sml_frame_snippet import SmlFrameSnippet


def test_snippet_type():
    s = SmlFrameSnippet(8, 0)

    with pytest.raises(WrongValueType) as e:
        s.get_value(float)
    assert str(e.value) == 'Expected type float but got type int'

    with pytest.raises(WrongValueType) as e:
        s.get_value(list)
    assert str(e.value) == 'Expected type list but got type int'

    s = SmlFrameSnippet([8], 0)

    with pytest.raises(WrongValueType) as e:
        s.get_value(float)
    assert str(e.value) == 'Expected type float but got type list'
