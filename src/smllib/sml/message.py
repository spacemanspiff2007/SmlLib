from typing import Dict, Type, Union

from smllib.sml import SmlBaseObj, SmlChoice, SmlCloseResponse, SmlGetListResponse, SmlObjFieldInfo, SmlOpenResponse
from smllib.sml._base_obj import T_SML_OBJ as _T_SML_OBJ

MSG_TYPES: Dict[int, Type[_T_SML_OBJ]] = {
    # 0x0100: 'SmlOpenRequest',
    0x0101: SmlOpenResponse,
    # 0x0200: 'SmlCloseRequest',
    0x0201: SmlCloseResponse,
    # 0x0300: 'SmlGetProfilePackRequest',
    # 0x0301: 'SmlGetProfilePackResponse',
    # 0x0400: 'SmlGetProfileListRequest',
    # 0x0401: 'SmlGetProfileListResponse',
    # 0x0500: 'SmlGetProcParameterRequest',
    # 0x0501: 'SmlGetProcParameterResponse',
    # 0x0600: 'SmlSetProcParameterRequest',
    # 0x0601: 'SmlSetProcParameterResponse',
    # 0x0700: 'SmlGetListRequest',
    0x0701: SmlGetListResponse,
    # 0xff01: 'SmlAttentionResponse',
}


class SmlMessage(SmlBaseObj):
    __sml__: Dict[str, SmlObjFieldInfo] = {
        'message_body': SmlObjFieldInfo(choice=SmlChoice(MSG_TYPES))
    }

    transaction_id: str
    group_no: int
    abort_on_error: int
    message_body: Union[SmlOpenResponse, SmlCloseResponse, SmlGetListResponse]
    crc16: int
