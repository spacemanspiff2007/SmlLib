import pytest

from smllib.sml.sml_obis import build_obis


def test_obis() -> None:
    assert build_obis('0100010800ff') == '0100010800ff'
    assert build_obis('0100010800ff').obis_code == '1-0:1.8.0*255'
    assert build_obis('0100010800ff').obis_short == '1.8.0'


def test_obis_invalid() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        build_obis(None)
    with pytest.raises(ValueError):  # noqa: PT011
        build_obis('0100010800')
