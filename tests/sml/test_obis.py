import pytest

from smllib.sml.sml_obis import build_obis


def test_obis():
    assert build_obis('0100010800ff') == '0100010800ff'
    assert build_obis('0100010800ff').obis_code == '1-0:1.8.0*255'
    assert build_obis('0100010800ff').obis_short == '1.8.0'


def test_obis_invalid():
    with pytest.raises(ValueError):
        build_obis(None)
    with pytest.raises(ValueError):
        build_obis(None)
