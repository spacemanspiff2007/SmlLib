from typing import Final, TypeVar

INDENT: Final = '  '


class SmlBaseObj:
    __sml__: dict

    def format_msg(self, indent: int = 0):
        indent += 1
        r = f'<{self.__class__.__name__}>\n'
        w = max(map(len, self.__dict__), default=0)
        for k, v in self.__dict__.items():
            if isinstance(v, SmlBaseObj):
                r += f'{INDENT * indent}{str(k):s} {v.format_msg(indent)}'
            elif isinstance(v, (tuple, list)):
                r += f'{INDENT * indent}{str(k):s}:\n'
                for e in v:
                    r += f'{INDENT * (indent + 1)}{e.format_msg(indent + 1)}'
            else:
                r += f'{INDENT * indent}{str(k):{w}s}: {v}\n'
        return r


T_SML_OBJ = TypeVar('T_SML_OBJ', bound=SmlBaseObj, covariant=True)
