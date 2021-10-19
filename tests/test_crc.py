from binascii import a2b_hex

import pytest

from smllib.crc import get_crc


@pytest.mark.parametrize('msg', (
    pytest.param('7605032b18116200620072630201710163fa3600', id='crc1'),
    pytest.param('7605171756bd6200620072630201710163170f00', id='crc2'),
    pytest.param('760700070615fce7620062007263010176010107000702e053ce0b0901454d4800004895f701016333aa00', id='crc3'),
    pytest.param('76051c414c02620062007263010176010102310b0a01445a47000282c0b07262016505471c2a620263f93800', id='crc4'),
    pytest.param('76040000016200620072650000010176010107000002dba23c0b0a01484c5902000424a0010163945b00', id='crc5'),
))
def test_crc(msg):
    _msg = memoryview(a2b_hex(msg))
    crc_msg = f'{_msg[-3]:02x}{_msg[-2]:02x}'
    crc_calc = f'{get_crc(_msg[:-4]):04x}'
    assert crc_msg == crc_calc
