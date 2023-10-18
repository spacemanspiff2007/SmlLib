from typing import Dict, Type

from smllib.sml import SmlBaseObj, SmlCloseResponse, SmlGetListResponse, SmlListEntry, SmlMessage, SmlOpenResponse

from . import SmlCloseResponseBuilder, SmlGetListResponseBuilder, \
    SmlListEntryBuilder, SmlMessageBuilder, SmlOpenResponseBuilder, T_SML_BUILDER

CTX_HINT = Dict[Type[SmlBaseObj], T_SML_BUILDER]


def create_context() -> CTX_HINT:
    return {
        SmlListEntry: SmlListEntryBuilder(),
        SmlGetListResponse: SmlGetListResponseBuilder(),
        SmlMessage: SmlMessageBuilder(),
        SmlCloseResponse: SmlCloseResponseBuilder(),
        SmlOpenResponse: SmlOpenResponseBuilder()
    }
