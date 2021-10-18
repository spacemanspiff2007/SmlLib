from typing import Dict, Type

from smllib.sml import SmlCloseResponse, SmlGetListResponse, SmlListEntry, SmlMessage, SmlOpenResponse, T_SML_OBJ

from . import SmlCloseResponseBuilder, SmlGetListResponseBuilder, \
    SmlListEntryBuilder, SmlMessageBuilder, SmlOpenResponseBuilder, T_SML_BUILDER

CTX_HINT = Dict[Type[T_SML_OBJ], T_SML_BUILDER]


def create_context() -> CTX_HINT:
    return {
        SmlListEntry: SmlListEntryBuilder(),
        SmlGetListResponse: SmlGetListResponseBuilder(),
        SmlMessage: SmlMessageBuilder(),
        SmlCloseResponse: SmlCloseResponseBuilder(),
        SmlOpenResponse: SmlOpenResponseBuilder()
    }
