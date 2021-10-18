from smllib.builder import SmlObjBuilder
from smllib.sml import SmlCloseResponse, SmlOpenResponse


class SmlOpenResponseBuilder(SmlObjBuilder):
    BUILDS = SmlOpenResponse


class SmlCloseResponseBuilder(SmlObjBuilder):
    BUILDS = SmlCloseResponse
