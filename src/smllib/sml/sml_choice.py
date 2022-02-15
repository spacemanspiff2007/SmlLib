from typing import Any, List, Mapping, Tuple, Type, Union

from smllib.errors import UnsupportedChoiceValue, WrongArgCount
from smllib.sml import T_SML_OBJ
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlChoice:
    def __init__(self, choices: Mapping[int, Type[T_SML_OBJ]]):
        self.choices = choices

    def get(self, obj: List[SmlFrameSnippet]) -> Union[Tuple[None, Any], Tuple[Type[T_SML_OBJ], Any]]:
        if len(obj) != 2:
            raise WrongArgCount()

        _type, _value = obj  # type: SmlFrameSnippet, SmlFrameSnippet
        choice_value = _type.get_value(int)

        ret = self.choices.get(choice_value)
        if ret is None:
            raise UnsupportedChoiceValue(choice_value)

        return ret, _value

    def __eq__(self, other):
        return self.choices == other.choices
