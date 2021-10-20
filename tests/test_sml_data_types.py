from binascii import a2b_hex

from smllib.sml_frame import EndOfSmlMsg, SmlFrame, SmlFrameSnippet


def check(f: SmlFrameSnippet, value, msg: str):
    if value is True or value is False or value is None or value is EndOfSmlMsg:
        assert f.value is value
    else:
        if isinstance(value, (tuple, list)):
            for i, _value in enumerate(value):
                assert f.value[i].value == _value
        else:
            assert f.value == value
    assert f.msg.hex() == msg


def test_get_int8():
    f = SmlFrame(b'\x52\xff')
    check(f.get_value(0), -1, '52ff')
    assert f.next_pos == 2

    f = SmlFrame(b'\x52\x03')
    check(f.get_value(0), 3, '5203')
    assert f.next_pos == 2

    f = SmlFrame(b'\x00\x52\x03')
    f.next_pos = 9999
    check(f.get_value(1), 3, '5203')
    assert f.next_pos == 3


def test_get_uint8():
    f = SmlFrame(b'\x62\xff')
    check(f.get_value(0), 255, '62ff')
    assert f.next_pos == 2

    f = SmlFrame(b'\x62\x03')
    check(f.get_value(0), 3, '6203')
    assert f.next_pos == 2

    f = SmlFrame(b'\x00\x62\xff')
    f.next_pos = 9999
    check(f.get_value(1), 255, '62ff')
    assert f.next_pos == 3


def test_get_int16():
    f = SmlFrame(b'\x53\xff\x00')
    check(f.get_value(0), -256, '53ff00')
    assert f.next_pos == 3

    f = SmlFrame(b'\x53\x00\x03')
    check(f.get_value(0), 3, '530003')
    assert f.next_pos == 3

    f = SmlFrame(b'\x00\x53\xff\x01')
    f.next_pos = 9999
    check(f.get_value(1), -255, '53ff01')
    assert f.next_pos == 4


def test_get_uint16():
    f = SmlFrame(b'\x63\xff\x00')
    check(f.get_value(0), 65280, '63ff00')
    assert f.next_pos == 3

    f = SmlFrame(b'\x63\x00\x03')
    check(f.get_value(0), 3, '630003')
    assert f.next_pos == 3

    f = SmlFrame(b'\x00\x63\xff\x01')
    f.next_pos = 9999
    check(f.get_value(1), 65281, '63ff01')
    assert f.next_pos == 4


def test_get_int32():
    f = SmlFrame(b'\x55\x00\x00\x0a\x8c')
    check(f.get_value(0), 2700, '5500000a8c')
    assert f.next_pos == 5

    f = SmlFrame(b'\x01\x01\x55\x00\x00\x0a\x8c')
    f.next_pos = 9999
    check(f.get_value(2), 2700, '5500000a8c')
    assert f.next_pos == 7


def test_get_uint32():
    f = SmlFrame(b'\x55\x00\x00\x0a\x8c')
    check(f.get_value(0), 2700, '5500000a8c')
    assert f.next_pos == 5


# def test_int():
#
#     f = SmlFrame(b'\x65\x0c\x6a\x50\xb5')
#     assert f.get_value(0) == 208294069
#
#     # too short stuff
#     with pytest.raises(InvalidBufferPos):
#         f = SmlFrame(b'\x56\x00\x04\xeb\x09')
#         assert f.get_value(0) is None
#     with pytest.raises(InvalidBufferPos):
#         f = SmlFrame(b'\x65\x0c\x6a')
#         assert f.get_value(0) is None
#
#     # now with indexes > 0
#     f = SmlFrame(b'\xaa\xbb\x56\x00\x04\xeb\x09\x6c')
#     assert f.get_value(2) == 82512236
#     f = SmlFrame(b'\x00\x52\xff')
#     assert f.get_value(1) == -1
#     f = SmlFrame(b'\x01\xff\x33\x62\x1e')
#     assert f.get_value(3) == 30
#     f = SmlFrame(b'\xab\xcd\x87\x44\x65\x0c\x6a\x50\xb5')
#     assert f.get_value(4) == 208294069
#
#     # now with stuff appended
#     f = SmlFrame(b'\x56\x00\x04\xeb\x09\x6c\x12\x34')
#     assert f.get_value(0) == 82512236
#     f = SmlFrame(b'\xaa\xbb\x52\xff\xcc\xdd')
#     assert f.get_value(2) == -1
#     f = SmlFrame(b'\x52\x62\x1e\x99')
#     assert f.get_value(1) == 30
#     f = SmlFrame(b'\x65\x0c\x6a\x50\xb5\x77\x88')
#     assert f.get_value(0) == 208294069
#
#     # first some values starting at index 0
#     f = SmlFrame(b'\x56\x00\x04\xeb\x09\x6c')
#     assert check(f.get_value(0), 82512236, '5600')
#

def test_none():
    f = SmlFrame(b'\x01\x01\x01')
    assert f.get_value().value is None
    assert f.next_pos == 1

    f.next_pos = 9999
    assert f.get_value(1).value is None
    assert f.next_pos == 2

    assert f.get_value().value is None
    assert f.next_pos == 3


def test_get_list():
    f = SmlFrame(b'\x71\x01')
    f.next_pos = 9999
    check(f._parse_msg(f.get_value(0)), [None], '7101')
    assert f.next_pos == 2

    f = SmlFrame(b'\x72\x01\x00')
    f.next_pos = 9999
    check(f._parse_msg(f.get_value(0)), [None, EndOfSmlMsg], '720100')
    assert f.next_pos == 3

    f = SmlFrame(b'\x72\x52\xff\x62\x1e')
    check(f._parse_msg(f.get_value(0)), [-1, 30], '7252ff621e')
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
    check(f._parse_msg(f.get_value(0)),
          ['0100010800ff', 1922, None, 30, -1, 231954902, None],
          '77070100010800ff650000078201621e52ff59000000000dd359d601')
    assert f.next_pos == 28


def test_str():
    f = SmlFrame(b'\x07\x01\x00\x01\x08\x00\xFF')
    f.next_pos = 9999
    check(f.get_value(0), '0100010800ff', '070100010800ff')
    assert f.next_pos == 7


def test_long_str():
    f = SmlFrame(a2b_hex('8302010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102'))  # noqa: E501
    check(
        f.get_value(0),
        '010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102',
        '8302010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102')
    assert f.next_pos == 50

    f = SmlFrame(a2b_hex('8302010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102FF'))  # noqa: E501
    check(
        f.get_value(0),
        '010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102',
        '8302010203040101010101010101010101010101010101010101010101010101010101010101010101010101010101010102')
    assert f.next_pos == 50
    assert f.buffer[f.next_pos] == 0xFF


def test_bool():
    f = SmlFrame(b'\x42\x01')
    f.next_pos = 9999
    check(f.get_value(0), True, '4201')
    assert f.next_pos == 2

    f = SmlFrame(b'\x42\x00')
    check(f.get_value(0), False, '4200')
    assert f.next_pos == 2


def test_eom():
    f = SmlFrame(b'\x00')
    check(f.get_value(0), EndOfSmlMsg, '00')
    assert f.next_pos == 1

    f = SmlFrame(b'\x00\x00')
    check(f.get_value(1), EndOfSmlMsg, '00')
    assert f.next_pos == 2
