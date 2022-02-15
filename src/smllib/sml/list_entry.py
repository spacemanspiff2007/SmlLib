from typing import Dict, Optional, Union

from smllib.const import OBIS_NAMES, UNITS
from smllib.sml import SmlObjFieldInfo
from smllib.sml._base_obj import INDENT, SmlBaseObj

from .sml_obis import build_obis, ObisCode
from .sml_time import build_time, TIME_HINT


class SmlListEntry(SmlBaseObj):
    __sml__: Dict[str, SmlObjFieldInfo] = {
        'val_time': SmlObjFieldInfo(func=build_time),
        'obis': SmlObjFieldInfo(func=build_obis)
    }

    obis: ObisCode
    status: Optional[int]
    val_time: TIME_HINT
    unit: Optional[int]
    scaler: Optional[int]
    value: Union[None, str, int, float]
    value_signature: Optional[str]

    def __repr__(self):
        r = []
        for k, v in self.__dict__.items():
            if v is not None:
                r.append(f'{k}: {v}')
        return f'<{", ".join(r)}>'

    def format_msg(self, indent: int = 0):
        indent += 1
        r = f'<{self.__class__.__name__}>\n'
        w = max(map(len, self.__dict__), default=0)

        for k, v in self.__dict__.items():
            r += f'{INDENT*indent}{str(k):{w}s}: {v}{f" ({self.obis.obis_code})" if k == "obis" else ""}\n'

        summary = ''
        if self.unit:
            val = self.get_value()
            u = UNITS.get(self.unit)
            if u is None:
                u = f" ?:{self.unit}"
            summary += f'{val}{u}'

        desc = OBIS_NAMES.get(self.obis)
        if desc is not None:
            summary += f'{" " if summary else ""}({desc})'
        if summary:
            r += f'{INDENT*indent}-> {summary:s}\n'
        return r

    def get_value(self) -> Union[None, float, str]:
        if self.value is None:
            return None

        # Some devices report the texts with scaler 0
        if self.scaler is None or isinstance(self.value, str):
            return self.value

        return round(self.value * 10**self.scaler, abs(self.scaler) + 3)
