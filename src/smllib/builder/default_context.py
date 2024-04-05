from typing import Dict, Type

from smllib.sml import SmlBaseObj, SmlCloseResponse, SmlGetListResponse, SmlListEntry, SmlMessage, SmlOpenResponse

from . import (
    T_SML_BUILDER,
    SmlCloseResponseBuilder,
    SmlGetListResponseBuilder,
    SmlListEntryBuilder,
    SmlMessageBuilder,
    SmlOpenResponseBuilder,
)


CTX_HINT = Dict[Type[SmlBaseObj], T_SML_BUILDER]


def create_context() -> CTX_HINT:
    return {
        SmlListEntry: SmlListEntryBuilder(),
        SmlGetListResponse: SmlGetListResponseBuilder(),
        SmlMessage: SmlMessageBuilder(),
        SmlCloseResponse: SmlCloseResponseBuilder(),
        SmlOpenResponse: SmlOpenResponseBuilder()
    }
