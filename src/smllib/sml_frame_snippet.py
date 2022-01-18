from typing import Optional, Union

from smllib.sml.sml_eom import CEndOfSmlMsg


class SmlFrameSnippet:
    __slots__ = ('pos', 'value', 'msg')

    def __init__(self, value: Union[None, bool, int, str, float, list, CEndOfSmlMsg], start: int,
                 stop: Optional[int] = None, buf: Optional[memoryview] = None):

        msg = None
        if stop is not None:
            if buf is None:
                raise ValueError('Arg stop und buf must be used together')
            msg = buf[start: stop]

        self.value = value
        self.pos = start
        self.msg: Optional[memoryview] = msg

    def stop_pos(self, pos: int, buf: memoryview) -> 'SmlFrameSnippet':
        assert self.msg is None
        self.msg = buf[self.pos: pos]
        return self
