import inspect
import typing
from binascii import a2b_hex
from typing import Union

import pytest

from smllib import SmlStreamReader
from smllib import crc as crc_module
from smllib.crc.x25 import get_crc as x25_get_crc


@pytest.mark.parametrize('msg', (
    pytest.param('7605032b18116200620072630201710163fa3600', id='crc1'),
    pytest.param('7605171756bd6200620072630201710163170f00', id='crc2'),
    pytest.param('760700070615fce7620062007263010176010107000702e053ce0b0901454d4800004895f701016333aa00', id='crc3'),
    pytest.param('76051c414c02620062007263010176010102310b0a01445a47000282c0b07262016505471c2a620263f93800', id='crc4'),
    pytest.param('76040000016200620072650000010176010107000002dba23c0b0a01484c5902000424a0010163945b00', id='crc5'),
))
def test_crc_x25(msg) -> None:
    _msg = memoryview(a2b_hex(msg))
    crc_msg = f'{_msg[-3]:02x}{_msg[-2]:02x}'
    crc_calc = f'{x25_get_crc(_msg[:-4]):04x}'
    assert crc_msg == crc_calc


def _get_signature() -> inspect.Signature:
    return inspect.Signature(
        parameters=[
            inspect.Parameter('buf', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Union[memoryview, bytes])
        ],
        return_annotation=int
    )


@pytest.mark.parametrize('name', (n for n in dir(crc_module) if not n.startswith('_')))
def test_signature_crc_funcs(name: str) -> None:
    crc_impl = getattr(crc_module, name)
    crc_sig = inspect.signature(crc_impl.get_crc)
    assert crc_sig == _get_signature()


def test_type_hint_reader() -> None:
    # Literal
    available = [n for n in dir(crc_module) if not n.startswith('_')]
    hint = typing.get_type_hints(SmlStreamReader.__init__)
    literal = hint['crc']
    literal_values = typing.get_args(literal)
    assert set(available) == set(literal_values)

    # crc_func variable
    signature = _get_signature()
    a = SmlStreamReader()
    hint = typing.get_type_hints(a.crc_func)
    assert hint.pop('return') is signature.return_annotation

    assert hint
    for name in hint:
        assert hint[name] == signature.parameters[name].annotation



def test_invalid_crc_name() -> None:

    with pytest.raises(ValueError) as e:
        SmlStreamReader(crc='asfd')
    assert str(e.value) == 'Unsupported CRC "asfd"! Available: "kermit", "x25"'
