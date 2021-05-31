from binascii import a2b_hex

import pytest

from smllib.sml_frame import InvalidBufferPos, SmlFrame


def test_get_int():

    # first some values starting at index 0
    f = SmlFrame(b'\x56\x00\x04\xeb\x09\x6c')
    assert f.get_value(0) == 82512236

    f = SmlFrame(b'\x52\xff')
    assert f.get_value(0) == -1

    f = SmlFrame(b'\x52\x03')
    assert f.get_value(0) == 3

    f = SmlFrame(b'\x62\x1e')
    assert f.get_value(0) == 30

    f = SmlFrame(b'\x65\x0c\x6a\x50\xb5')
    assert f.get_value(0) == 208294069

    # too short stuff
    with pytest.raises(InvalidBufferPos):
        f = SmlFrame(b'\x56\x00\x04\xeb\x09')
        assert f.get_value(0) is None
    with pytest.raises(InvalidBufferPos):
        f = SmlFrame(b'\x65\x0c\x6a')
        assert f.get_value(0) is None

    # now with indexes > 0
    f = SmlFrame(b'\xaa\xbb\x56\x00\x04\xeb\x09\x6c')
    assert f.get_value(2) == 82512236
    f = SmlFrame(b'\x00\x52\xff')
    assert f.get_value(1) == -1
    f = SmlFrame(b'\x01\xff\x33\x62\x1e')
    assert f.get_value(3) == 30
    f = SmlFrame(b'\xab\xcd\x87\x44\x65\x0c\x6a\x50\xb5')
    assert f.get_value(4) == 208294069

    # now with stuff appended
    f = SmlFrame(b'\x56\x00\x04\xeb\x09\x6c\x12\x34')
    assert f.get_value(0) == 82512236
    f = SmlFrame(b'\xaa\xbb\x52\xff\xcc\xdd')
    assert f.get_value(2) == -1
    f = SmlFrame(b'\x52\x62\x1e\x99')
    assert f.get_value(1) == 30
    f = SmlFrame(b'\x65\x0c\x6a\x50\xb5\x77\x88')
    assert f.get_value(0) == 208294069


def test_get_next_pos():
    f = SmlFrame(b'\x52\xff')
    assert f.get_value(0) == -1
    assert f.next_pos == 2

    f = SmlFrame(b'\x71\xff')
    f.next_pos = 9999
    assert f.get_value(0) == [None]
    assert f.next_pos == 1


def test_none():
    f = SmlFrame(b'\x01\x01\x01\xff')
    assert f.get_value() is None
    assert f.next_pos == 1

    f.next_pos = 9999
    assert f.get_value(1) is None
    assert f.next_pos == 2

    assert f.get_value() is None
    assert f.next_pos == 3


def test_get_list():
    f = SmlFrame(b'\x72\x52\xff\x62\x1e')

    r = f.get_value(0)
    assert f.next_pos == 1
    assert r == [None, None]

    f.next_pos = 9999
    assert f.get_value(1) == -1
    assert f.next_pos == 3

    assert f.get_value() == 30
    assert f.next_pos == 5

    f = SmlFrame(a2b_hex(
        '77070100010800ff'
        '6500000782'
        '01'
        '621e'
        '52ff'
        '59000000000dd359d6'
        '01'
        'ff'))
    r = f.get_value(0)
    assert f.next_pos == 1
    assert r == [None, None, None, None, None, None, None]

    assert f.get_value() == '0100010800ff'
    assert f.get_value() == 1922
    assert f.get_value() is None
    assert f.get_value() == 30
    assert f.get_value() == -1

    assert f.get_value() == 231954902
    assert f.get_value() is None

    v_list = f.get_value(0)
    for i, _ in enumerate(v_list):
        v_list[i] = f.get_value()
    assert v_list == ['0100010800ff', 1922, None, 30, -1, 231954902, None]


def test_str():
    f = SmlFrame(b'\x07\x01\x00\x01\x08\x00\xFF')
    f.next_pos = 9999
    assert f.get_value(0) == '0100010800ff'
    assert f.next_pos == 7


def test_bool():
    f = SmlFrame(b'\x42\x01')
    f.next_pos = 9999
    assert f.get_value(0) is True
    assert f.next_pos == 2

    f = SmlFrame(b'\x42\x00')
    assert f.get_value(0) is False


def test_long_str():
    f = SmlFrame(a2b_hex('8302010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102FF'))  # noqa: E501
    assert f.get_value(0) == '010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102'    # noqa: E501
    assert f.next_pos == 50
    assert f.buffer[50] == 0xFF
