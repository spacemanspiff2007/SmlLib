from typing import Any, Callable, Dict, List, Tuple, Type, Union

from smllib.errors import UnsupportedType, WrongArgCount
from smllib.sml import SmlBaseObj


class SmlChoice:
    def __init__(self, choices: Dict[int, Union[Type[SmlBaseObj], Callable[[List[Any]], Any]]]):
        self.choices = choices

    def get(self, obj) -> Union[Tuple[None, Any], Tuple[Type[SmlBaseObj], Any]]:
        if len(obj) != 2:
            raise WrongArgCount()

        _type, _value = obj
        ret = self.choices.get(_type)
        if ret is None:
            raise UnsupportedType(_type)

        if issubclass(ret, SmlBaseObj):
            return ret, _value
        return None, ret(_value)

    def __eq__(self, other):
        return self.choices == other.choices
