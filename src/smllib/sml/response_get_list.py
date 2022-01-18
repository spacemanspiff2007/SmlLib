from typing import Dict, Optional, Tuple

from smllib.sml import SmlBaseObj, SmlListEntry, SmlObjFieldInfo

from .sml_time import build_time, TIME_HINT


class SmlGetListResponse(SmlBaseObj):
    __sml__: Dict[str, SmlObjFieldInfo] = {
        'act_sensor_time': SmlObjFieldInfo(func=build_time),
        'act_gateway_time': SmlObjFieldInfo(func=build_time),
    }

    client_id: Optional[str]
    sever_id: str
    list_name: Optional[str]
    act_sensor_time: TIME_HINT
    val_list: Tuple[SmlListEntry, ...]
    list_signature: Optional[str]
    act_gateway_time: TIME_HINT
