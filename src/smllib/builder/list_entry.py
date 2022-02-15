from binascii import a2b_hex
from typing import Dict, Type

from smllib.builder import SmlObjBuilder
from smllib.sml import SmlListEntry
from smllib.sml._base_obj import SmlBaseObj
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlListEntryBuilder(SmlObjBuilder[SmlListEntry]):
    BUILDS = SmlListEntry

    def build(self, obj: SmlFrameSnippet, classes: Dict[Type[SmlBaseObj], 'SmlObjBuilder']) -> SmlListEntry:
        ret = super().build(obj, classes)    # type: SmlListEntry

        value = ret.value
        if value is None:
            raise ValueError('value is required!')

        # Maybe it's ascii so we try to decode it
        if isinstance(value, str):
            v = a2b_hex(value).decode(errors='ignore')
            if v.isalnum():
                ret.value = v

        return ret
