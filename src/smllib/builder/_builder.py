from typing import Dict, Generic, Tuple, Type, TypeVar

from smllib.errors import WrongArgCount, WrongValueType
from smllib.sml import inspect_obj, SmlBaseObj, SmlObjFieldInfo, T_SML_OBJ
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlObjBuilder(Generic[T_SML_OBJ]):
    BUILDS: Type[T_SML_OBJ]

    def __init__(self):
        assert issubclass(self.BUILDS, SmlBaseObj), self.BUILDS
        self.fields: Dict[str, SmlObjFieldInfo] = inspect_obj(self.BUILDS)

    def build(self, obj: SmlFrameSnippet, classes: Dict[Type[SmlBaseObj], 'SmlObjBuilder']) -> T_SML_OBJ:
        # check length
        lst = obj.value
        if len(self.fields) != len(lst):
            raise WrongArgCount()

        out = self.BUILDS()
        for i, a in enumerate(self.fields.items()):   # type: int, Tuple[str, SmlObjFieldInfo]
            name, field = a
            value = lst[i].value

            # rebuild with choice
            if field.choice is not None:
                cls, value = field.choice.get(value)
                if cls is not None:
                    value = classes[cls].build(value, classes)

            func = field.func
            if func is not None:
                value = func(value)

            if field.is_container:
                cls = classes[field.type]
                value = tuple([cls.build(v, classes) for v in value])
            else:
                if not isinstance(value, field.type):
                    raise WrongValueType(f'{value} ({type(value)}) != {field.type}')

            setattr(out, name, value)
        return out


T_SML_BUILDER = TypeVar('T_SML_BUILDER', bound=SmlObjBuilder, covariant=True)
