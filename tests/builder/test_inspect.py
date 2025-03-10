from datetime import datetime

from smllib.sml import (
    SmlChoice,
    SmlCloseResponse,
    SmlGetListResponse,
    SmlListEntry,
    SmlObjFieldInfo,
    SmlOpenResponse,
    inspect_obj,
)
from smllib.sml.message import MSG_TYPES, SmlMessage
from smllib.sml.sml_obis import build_obis, ObisCode
from smllib.sml.sml_time import build_time
from smllib.sml.sml_value import build_sml_value


def test_inspect_sml_message() -> None:
    fields = inspect_obj(SmlMessage)
    assert list(fields.keys()) == ['transaction_id', 'group_no', 'abort_on_error', 'message_body', 'crc16']
    assert fields['transaction_id'] == SmlObjFieldInfo(type=str)
    assert fields['group_no'] == SmlObjFieldInfo(type=int)
    assert fields['abort_on_error'] == SmlObjFieldInfo(type=int)
    assert fields['message_body'] == SmlObjFieldInfo(
        type=(SmlOpenResponse, SmlCloseResponse, SmlGetListResponse), choice=SmlChoice(MSG_TYPES))
    assert fields['crc16'] == SmlObjFieldInfo(type=int)


def test_inspect_sml_list_entry() -> None:
    fields = inspect_obj(SmlListEntry)
    assert list(fields.keys()) == ['obis', 'status', 'val_time', 'unit', 'scaler', 'value', 'value_signature']
    assert fields['obis'] == SmlObjFieldInfo(type=ObisCode, func=build_obis)
    assert fields['status'] == SmlObjFieldInfo(type=(int, type(None)))
    assert fields['val_time'] == SmlObjFieldInfo(type=(type(None), int, datetime), func=build_time)
    assert fields['unit'] == SmlObjFieldInfo(type=(int, type(None)))
    assert fields['scaler'] == SmlObjFieldInfo(type=(int, type(None)))
    assert fields['value'] == SmlObjFieldInfo(type=(type(None), str, int, float, datetime), func=build_sml_value)
    assert fields['value_signature'] == SmlObjFieldInfo(type=(str, type(None)))
