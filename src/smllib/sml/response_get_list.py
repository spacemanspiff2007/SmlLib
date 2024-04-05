from typing import ClassVar, Dict, Optional, Tuple

from smllib.sml import SmlBaseObj, SmlListEntry, SmlObjFieldInfo

from .sml_time import TIME_HINT, build_time


class SmlGetListResponse(SmlBaseObj):
    __sml__: ClassVar[Dict[str, SmlObjFieldInfo]] = {
        'act_sensor_time': SmlObjFieldInfo(func=build_time),
        'act_gateway_time': SmlObjFieldInfo(func=build_time),
    }

    client_id: Optional[str]
    server_id: str
    list_name: Optional[str]
    act_sensor_time: TIME_HINT
    val_list: Tuple[SmlListEntry, ...]
    list_signature: Optional[str]
    act_gateway_time: TIME_HINT
