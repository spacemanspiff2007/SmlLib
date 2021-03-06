from binascii import a2b_hex

from smllib.sml_fields import SmlListEntry
from smllib.sml_frame import SmlFrame


def test_sml_fileds():
    f = SmlFrame(a2b_hex('77078181c78203ff010101010449534b0177070100000009ff010101010b'))
    val_list = f.get_value(0)
    for i, _ in enumerate(val_list):
        val_list[i] = f.get_value()
    o = SmlListEntry.from_list(val_list)
    assert o.obis == '8181c78203ff'
    assert o.value == 'ISK'

    f = SmlFrame(a2b_hex('77070100010800ff650000018201621e52ff590000000001122334017707'))
    val_list = f.get_value(0)
    for i, _ in enumerate(val_list):
        val_list[i] = f.get_value()
    o = SmlListEntry.from_list(val_list)

    assert o.obis == '0100010800ff'
    assert o.status == 386
    assert o.unit == 30
    assert o.scaler == -1
    assert o.value == 17965876
    assert o.get_value() == 1796587.6
