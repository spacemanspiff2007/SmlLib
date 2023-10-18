from typing import Final, Generic, List, Mapping, Tuple, Type

from smllib.errors import UnsupportedChoiceValue, WrongArgCount
from smllib.sml import T_SML_OBJ
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlChoice(Generic[T_SML_OBJ]):
    def __init__(self, choices: Mapping[int, Type[T_SML_OBJ]]):
        self.choices: Final = choices

    def get(self, obj: List[SmlFrameSnippet]) -> Tuple[Type[T_SML_OBJ], SmlFrameSnippet]:
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
