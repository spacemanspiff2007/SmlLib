from datetime import datetime, timedelta
from typing import Union

from smllib.errors import UnsupportedType

TIME_HINT = Union[None, int, datetime]


def build_time(_in):
    if _in is None:
        return _in

    # This is a workaround for times that are not reported according to specification
    # Instead of a choice list these devices report just the timestamp - however I am unsure about it.
    if isinstance(_in, int):
        return _in

    type_s, value_s = _in
    _type = type_s.value
    if _type == 1:
        return value_s.value
    if _type == 2:
        return datetime.utcfromtimestamp(value_s.value)
    if _type == 3:
        ts, offset1, offset2 = value_s.value
        return datetime.utcfromtimestamp(ts.value) + timedelta(minutes=offset1.value) + timedelta(minutes=offset2.value)

    raise UnsupportedType(_type)
