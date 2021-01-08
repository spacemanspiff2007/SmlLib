from datetime import datetime, timedelta, tzinfo
from typing import Optional


class SmlTzOffset(tzinfo):
    def __init__(self, utc_offset: int, dst_offset: int):
        self._utc_offset = timedelta(minutes=utc_offset)
        self._dst_offset = timedelta(minutes=dst_offset)

    def tzname(self, dt: Optional[datetime]) -> Optional[str]:
        return 'SmlTzOffset'

    def utcoffset(self, dt: Optional[datetime]) -> Optional[timedelta]:
        return self._utc_offset

    def dst(self, dt: Optional[datetime]) -> Optional[timedelta]:
        return self._dst_offset


class SmlTime:
    @classmethod
    def from_list(cls, _in):
        _t = _in[0]
        _v = _in[1]
        if _t == 1:
            return _v
        if _t == 2:
            return datetime.fromtimestamp(_v)
        if _t == 3:
            return datetime.fromtimestamp(_v[0], tz=SmlTzOffset(_v[1], _v[2]))
