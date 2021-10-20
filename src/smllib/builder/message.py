from typing import Dict, Type

import smllib.sml
from smllib.builder import SmlObjBuilder
from smllib.errors import EndOfSmlMsgExpected
from smllib.sml import EndOfSmlMsg
from smllib.sml._base_obj import SmlBaseObj


class SmlMessageBuilder(SmlObjBuilder):
    BUILDS = smllib.sml.SmlMessage

    def build(self, obj: list, classes: Dict[Type[SmlBaseObj], SmlObjBuilder]) -> smllib.sml.SmlMessage:
        lst = obj.value
        if lst[5].value is not EndOfSmlMsg:
            raise EndOfSmlMsgExpected()
        lst.pop(5)

        return super().build(obj, classes)
