from typing import Optional, Union


class SmlFrameSnippet:
    __slots__ = ('pos', 'value', 'msg')

    def __init__(self, value: Union[None, bool, int, str, float, list], start: int,
                 stop: Optional[int] = None, buf: Optional[memoryview] = None):
        self.value = value

        self.pos = start
        self.msg: Optional[memoryview] = None if stop is None else buf[start: stop]

    def stop_pos(self, pos: int, buf: memoryview) -> 'SmlFrameSnippet':
        assert self.msg is None
        self.msg = buf[self.pos: pos]
        return self
