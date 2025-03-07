from smllib.errors import UnsupportedChoiceValue
from smllib.sml.sml_time import build_time


def build_sml_value(_in):
    if _in is None:
        return _in

    if not isinstance(_in, list):
        return _in

    type_s, value_s = _in
    _type = type_s.value
    if _type == 1:  # SML_Time
        return build_time(value_s.value)

    raise UnsupportedChoiceValue(_type)
