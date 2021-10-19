from binascii import a2b_hex

import pytest

from smllib.crc import get_crc


@pytest.mark.parametrize(('msg', ), (
    ('7605032b18116200620072630201710163fa3600', ),
    ('7605171756bd6200620072630201710163170f00',),
    ('760700070615fce7620062007263010176010107000702e053ce0b0901454d4800004895f701016333aa00',),
))
def test_crc(msg):
    _msg = a2b_hex(msg)
    crc_msg = f'{_msg[-3]:02x}{_msg[-2]:02x}'
    assert crc_msg == f'{get_crc(_msg[:-4]):04x}'
