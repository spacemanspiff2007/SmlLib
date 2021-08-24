from datetime import datetime, timedelta
from typing import Union


class SmlTime:
    HINT = Union[None, int, datetime]

    @staticmethod
    def from_list(_in):
        if _in is None:
            return _in

        # This is a workaround for times that are not reported according to specification
        # Instead of a choice list these devices report just the timestamp - however I am unsure about it.
        if isinstance(_in, int):
            return _in

        _t = _in[0]
        _v = _in[1]
        if _t == 1:
            return _v
        if _t == 2:
            return datetime.fromtimestamp(_v)
        if _t == 3:
            return datetime.fromtimestamp(_v[0]) + timedelta(minutes=_v[1]) + timedelta(minutes=_v[2])

        raise ValueError(f'Can not build SmlTime from {_in}')
