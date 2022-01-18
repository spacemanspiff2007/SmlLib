from smllib.builder import SmlObjBuilder
from smllib.sml import SmlCloseResponse, SmlOpenResponse


class SmlOpenResponseBuilder(SmlObjBuilder[SmlOpenResponse]):
    BUILDS = SmlOpenResponse


class SmlCloseResponseBuilder(SmlObjBuilder[SmlCloseResponse]):
    BUILDS = SmlCloseResponse
