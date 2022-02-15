from typing import Optional, Type, TypeVar, Union

from smllib.errors import WrongValueType
from smllib.sml.sml_eom import CEndOfSmlMsg

SNIP_TYPE = TypeVar('SNIP_TYPE', bound=object)


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

    def get_value(self, val_type: Type[SNIP_TYPE]) -> SNIP_TYPE:
        value = self.value
        if not isinstance(value, val_type):
            raise WrongValueType(f'Expected type {val_type.__name__} but got type {type(value).__name__}')
        return value
