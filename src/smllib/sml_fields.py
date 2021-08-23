from binascii import a2b_hex
from datetime import datetime
from typing import List, Optional, Union, get_args, get_origin

from .const import OBIS_NAMES, UNITS
from .sml import SmlTime


class CEndofSmlMsg:
    def __repr__(self):
        return '<EndofSmlMsg>'


EndofSmlMsg = CEndofSmlMsg()
NoneType = type(None)

INDENT = '    '


class SmlMsgBase:
    @classmethod
    def from_list(cls, _in: list):
        anno = cls.__annotations__
        c_req = len(anno)

        if not isinstance(_in, list) and len(_in) != c_req:
            raise ValueError(f'List with {c_req} entries expected, got {_in} ({type(_in)})')

        c = cls()
        for i, k in enumerate(cls.__annotations__.items()):
            k, _t = k

            # todo: add test that all Unions are short for Optional
            # Optional transforms to Union with two args, e.g. (str, None)
            origin = get_origin(_t)
            if origin is Union or origin is list:
                _t = get_args(_t)[0]

            v = _in[i]
            # if the passed value is a list it's either a new MsgField or
            # a list of MsgFields
            if isinstance(v, list):
                if origin is list:
                    for _i, _v in enumerate(v):
                        v[_i] = _t.from_list(_v)
                else:
                    v = _t.from_list(v)
            setattr(c, k, v)

        # todo: move this to testing
        i = 0
        for k, _t in anno.items():
            v = getattr(c, k)
            i += 1

            origin = get_origin(_t)
            args = get_args(_t)

            if origin is Union or origin is list:
                _t = args[0]

            if origin is list:
                for v in v:
                    assert isinstance(v, _t), f'{k} {v}: {type(v)} != {_t} for {cls}\n{_in}'
            else:
                if origin is Union and v is None:
                    continue
                if _t is SmlTime:
                    _t = (int, datetime)
                assert isinstance(v, _t), f'{k} {v}: {type(v)} != {_t} for {cls}\n{_in}'

        return c

    def format_msg(self, indent: int = 0):
        r = f'<{self.__class__.__name__}>\n'
        w = max(map(len, self.__dict__), default=0)
        for k, v in self.__dict__.items():
            if isinstance(v, SmlMsgBase):
                r += f'{INDENT * indent}{str(k):s} {v.format_msg(indent + 1)}'
            elif isinstance(v, list):
                r += f'{INDENT * indent}{str(k):s}: list\n'
                for e in v:
                    r += f'{INDENT * (indent + 1)}{e.format_msg(indent + 2)}'
            else:
                r += f'{INDENT * indent}{str(k):{w}s}: {v}\n'
        return r


class SmlMessage:
    transaction_id: str
    group_no: int
    abort_on_error: int
    message_body: SmlMsgBase
    crc16: int

    @classmethod
    def from_list(cls, _in: list) -> 'SmlMessage':
        assert isinstance(_in, list) and len(_in) == 6
        if not _in[5] is EndofSmlMsg:
            raise ValueError(f'Last entry is not {EndofSmlMsg}: {_in[5]}')
        # Load Msg Contents
        _in[3] = get_msg_cls(_in[3])
        return cls(*_in)

    def __init__(self, transaction_id: str, group_no: int, abort_on_error: int, message_body: List[SmlMsgBase],
                 crc16: int, eom: CEndofSmlMsg = None):
        self.transaction_id: str = transaction_id
        self.group_no: int = group_no
        self.abort_on_error: int = abort_on_error
        self.message_body: List[SmlMsgBase] = message_body
        self.crc16: int = crc16

    def format_msg(self):
        r = f'{self.__class__.__name__}\n'
        w = max(map(len, self.__dict__), default=0)
        for k, v in self.__dict__.items():
            if isinstance(v, SmlMsgBase):
                r += f'{INDENT}{str(k):s} {v.format_msg(2)}'
            else:
                r += f'{INDENT}{str(k):{w}s}: {v}\n'
        return r


class SmlOpenResponse(SmlMsgBase):
    codepage: Optional[str]
    client_id: Optional[str]
    req_file_id: str
    server_id: str
    ref_time: Optional[SmlTime]
    sml_version: Optional[int]


class SmlCloseResponse(SmlMsgBase):
    global_signature: Optional[str]


class SmlListEntry:

    @classmethod
    def from_list(cls, _in):
        if not isinstance(_in, list) and len(_in) != 7:
            raise ValueError(f'List with 7 entries expected, got {_in} ({type(_in)})')
        if _in[0] is None:
            raise ValueError('Obis field is required!')
        if _in[5] is None:
            raise ValueError('value is required!')

        # Maybe it's ascii so we try to decode it
        if isinstance(_in[5], str):
            v = a2b_hex(_in[5]).decode(errors='ignore')
            if v.isalnum():
                _in[5] = v

        return cls(*_in)

    def __init__(self, obis: str, status: Optional[int], val_time, unit: Optional[int], scaler: Optional[int] = None,
                 value: Union[None, str, int, float] = None, value_signature: Optional[str] = None):
        self.obis = obis
        self.status: Optional[int] = status
        self.val_time = val_time
        self.unit: Optional[int] = unit
        self.scaler: Optional[int] = scaler
        self.value = value
        self.value_signature = value_signature

    def __repr__(self):
        r = []
        for k, v in self.__dict__.items():
            if v is not None:
                r.append(f'{k}: {v}')
        return f'<{", ".join(r)}>'

    def format_msg(self, indent: int = 0):
        r = f'<{self.__class__.__name__}>\n'
        w = max(map(len, self.__dict__), default=0)
        for k, v in self.__dict__.items():
            r += f'{INDENT*indent}{str(k):{w}s}: {v}\n'

        summary = ''
        if self.unit:
            val = self.get_value()
            u = UNITS.get(self.unit)
            if u is None:
                u = f" ?:{self.unit}"
            summary += f'{val}{u}'

        desc = OBIS_NAMES.get(self.obis)
        if desc is not None:
            summary += f'{" " if summary else ""}({desc})'
        if summary:
            r += f'{INDENT*indent}-> {summary:s}\n'
        return r

    def get_value(self) -> float:
        if self.scaler is None:
            return self.value

        return round(self.value * 10**self.scaler, abs(self.scaler) + 3)


class SmlGetListResponse(SmlMsgBase):
    client_id: Optional[str]
    sever_id: str
    list_name: Optional[str]
    act_sensor_time: Optional[SmlTime]
    val_list: List[SmlListEntry]
    list_signature: Optional[str]
    act_gateway_time: Optional[SmlTime]


def get_msg_cls(_in: list) -> SmlMsgBase:
    types = {
        0x0100: 'SmlOpenRequest',
        0x0101: SmlOpenResponse,
        0x0200: 'SmlCloseRequest',
        0x0201: SmlCloseResponse,
        0x0300: 'SmlGetProfilePackRequest',
        0x0301: 'SmlGetProfilePackResponse',
        0x0400: 'SmlGetProfileListRequest',
        0x0401: 'SmlGetProfileListResponse',
        0x0500: 'SmlGetProcParameterRequest',
        0x0501: 'SmlGetProcParameterResponse',
        0x0600: 'SmlSetProcParameterRequest',
        0x0601: 'SmlSetProcParameterResponse',
        0x0700: 'SmlGetListRequest',
        0x0701: SmlGetListResponse,
        0xff01: 'SmlAttentionResponse',
    }

    if len(_in) != 2:
        raise ValueError(f'Not a class container: {_in}')

    _msg_type = _in[0]
    cls = types.get(_msg_type)
    if cls is None:
        raise ValueError(f'Unknown message type: {_msg_type:x}')

    if isinstance(cls, str):
        raise ValueError(f'{cls} is not yet supported!')

    return cls.from_list(_in[1])
