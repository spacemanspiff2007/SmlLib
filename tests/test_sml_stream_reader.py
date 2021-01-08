import pytest

from smllib.reader import CrcError, SmlStreamReader


def test_strip_start():
    r = SmlStreamReader()
    r.add(b'asdfasdfasdf\x1B\x1B\x1B\x1B\x01\x01\x01\x01')
    assert r.get_frame() is None
    assert r.bytes == b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01'


def test_skip_escape():
    r = SmlStreamReader()
    msg = b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1A\x00\x00\x00'
    r.add(msg)
    assert r.get_frame() is None
    assert r.bytes == msg


def test_exception():
    r = SmlStreamReader()
    msg = b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01\x1B\x1B\x1B\x1B\x1A\x00\x00\x00'
    r.add(msg)
    with pytest.raises(CrcError) as e:
        r.get_frame()
    assert repr(e.value) == '<CrcError msg: 0000 calc: c6e5>'
