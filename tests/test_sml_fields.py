from binascii import a2b_hex
from datetime import datetime

from smllib.builder import SmlListEntryBuilder, create_context
from smllib.sml_frame import SmlFrame


def test_sml_fields() -> None:
    f = SmlFrame(a2b_hex('77078181c78203ff010101010449534b0177070100000009ff010101010b'))
    val_list = f._parse_msg(f.get_value(0))
    o = SmlListEntryBuilder().build(val_list, create_context())
    assert o.obis == '8181c78203ff'
    assert o.value == 'ISK'

    f = SmlFrame(a2b_hex('77070100010800ff650000018201621e52ff590000000001122334017707'))
    val_list = f._parse_msg(f.get_value(0))
    o = SmlListEntryBuilder().build(val_list, create_context())

    assert o.obis == '0100010800ff'
    assert o.status == 386
    assert o.unit == 30
    assert o.scaler == -1
    assert o.value == 17965876
    assert o.get_value() == 1796587.6


def test_val_time() -> None:
    # Frame where time is None
    f = SmlFrame(a2b_hex('77070100600100ff010101010b0a01484c5902000424a001'))
    val_list = f._parse_msg(f.get_value(0))
    o = SmlListEntryBuilder().build(val_list, create_context())
    assert o.val_time is None

    # Frame where secIndex == 1 and time == 0
    # -> 7262016200
    f = SmlFrame(a2b_hex('77070100600100ff017262016200620052000b0a01445a47000282c0b001'))
    val_list = f._parse_msg(f.get_value(0))
    o = SmlListEntryBuilder().build(val_list, create_context())
    assert o.val_time == 0


def test_value_sml_time() -> None:
    f = SmlFrame(a2b_hex('770781006008000101010101726201726202655FEE825D01'))
    val_list = f._parse_msg(f.get_value(0))
    o = SmlListEntryBuilder().build(val_list, create_context())

    assert o.obis == '810060080001'
    assert o.status is None
    assert o.unit is None
    assert o.scaler is None
    assert o.value == datetime(2021, 1, 1, 2, 1, 1)
