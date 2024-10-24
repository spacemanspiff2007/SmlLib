from typing import Dict, Generic, Type, TypeVar

from smllib.errors import WrongArgCount, WrongValueType
from smllib.sml import T_SML_OBJ, SmlBaseObj, SmlObjFieldInfo, inspect_obj
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlObjBuilder(Generic[T_SML_OBJ]):
    BUILDS: Type[T_SML_OBJ]

    def __init__(self) -> None:
        assert issubclass(self.BUILDS, SmlBaseObj), self.BUILDS
        self.fields: Dict[str, SmlObjFieldInfo] = inspect_obj(self.BUILDS)

    def build(self, obj: SmlFrameSnippet, classes: Dict[Type[SmlBaseObj], 'SmlObjBuilder']) -> T_SML_OBJ:
        # check length
        lst = obj.get_value(list)
        if len(self.fields) != len(lst):
            raise WrongArgCount()

        out = self.BUILDS()
        for i, a in enumerate(self.fields.items()):   # type: int, tuple[str, SmlObjFieldInfo]
            name, field = a
            value = lst[i].value

            # rebuild with choice
            if field.choice is not None:
                choice_cls, value = field.choice.get(value)
                value = classes[choice_cls].build(value, classes)

            func = field.func
            if func is not None:
                value = func(value)

            if field.is_container:
                cls_builder = classes[field.type]
                value = tuple([cls_builder.build(v, classes) for v in value])
            else:
                if not isinstance(value, field.type):
                    msg = f'{value} ({type(value)}) != {field.type}'
                    raise WrongValueType(msg)

            setattr(out, name, value)
        return out


T_SML_BUILDER = TypeVar('T_SML_BUILDER', bound=SmlObjBuilder, covariant=True)
