from datetime import datetime, timedelta
from typing import Union

from smllib.errors import UnsupportedType

TIME_HINT = Union[None, int, datetime]


def build_time(_in):
    if _in is None:
        return _in

    # This is a workaround for times that are not reported according to specification
    # Instead of a choice list these devices report just the timestamp - however I am unsure about it.
    # todo: remove it and see what happens
    if isinstance(_in, int):
        return _in

    _type, _value = _in
    if _type == 1:
        return _value
    if _type == 2:
        return datetime.utcfromtimestamp(_value)
    if _type == 3:
        ts, offset1, offset2 = _value
        return datetime.utcfromtimestamp(ts) + timedelta(minutes=offset1) + timedelta(minutes=offset2)

    raise UnsupportedType(_type)
