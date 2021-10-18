from typing import Any, Callable, Dict, get_args, get_origin, get_type_hints, List, Optional, Type, Union

from smllib.sml import SmlBaseObj, SmlChoice


class SmlObjFieldInfo:
    def __init__(self, func: Optional[Callable[[List[Any]], 'SmlBaseObj']] = None, type=None,
                 choice: Optional[SmlChoice] = None, is_container=False):
        self.func = func
        self.type = type
        self.choice = choice
        self.is_container = is_container

    def __eq__(self, other):
        return self.func == other.func and self.type == other.type and \
            self.choice == other.choice and self.is_container == other.is_container

    def copy(self) -> 'SmlObjFieldInfo':
        return self.__class__(func=self.func, type=self.type, choice=self.choice, is_container=self.is_container)


def inspect_obj(cls: Type['SmlBaseObj']) -> Dict[str, SmlObjFieldInfo]:
    fields: Dict[str, SmlObjFieldInfo] = {}

    for name, hint in get_type_hints(cls).items():
        if name == '__sml__':
            continue

        info = cls.__sml__.get(name)
        if info is None:
            info = SmlObjFieldInfo()
        else:
            assert isinstance(info, SmlObjFieldInfo)
            info = info.copy()
        fields[name] = info

        origin = get_origin(hint)
        if origin is None:
            info.type = hint
            continue

        # Union[str, int]
        if origin is Union:
            info.type = get_args(hint)
            continue

        # Tuple[type, ...]
        if origin is tuple:
            info.is_container = True
            args = get_args(hint)
            assert args[1] is ...
            info.type = args[0]
            continue

        raise ValueError(f'Unknown hint: {origin} for {name}')

    return fields
