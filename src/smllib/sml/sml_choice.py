from typing import Any, Callable, List, Mapping, Tuple, Type, Union

from smllib.errors import UnsupportedType, WrongArgCount
from smllib.sml import SmlBaseObj
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlChoice:
    def __init__(self, choices: Mapping[int, Union[Type[SmlBaseObj], Callable[[List[Any]], Any]]]):
        self.choices = choices

    def get(self, obj: List[SmlFrameSnippet]) -> Union[Tuple[None, Any], Tuple[Type[SmlBaseObj], Any]]:
        if len(obj) != 2:
            raise WrongArgCount()

        _type, _value = obj
        ret = self.choices.get(_type.value)
        if ret is None:
            raise UnsupportedType(_type.value)

        if issubclass(ret, SmlBaseObj):
            return ret, _value
        return None, ret(_value)

    def __eq__(self, other):
        return self.choices == other.choices
