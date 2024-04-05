class ObisCode(str):
    __slots__ = ('obis_code', 'obis_short')

    def __init__(self, obis_hex: str):
        _a = int(obis_hex[0:2], 16)
        _b = int(obis_hex[2:4], 16)
        _c = int(obis_hex[4:6], 16)
        _d = int(obis_hex[6:8], 16)
        _e = int(obis_hex[8:10], 16)
        _f = int(obis_hex[10:12], 16)
        self.obis_code = f'{_a}-{_b}:{_c}.{_d}.{_e}*{_f}'
        self.obis_short = f'{_c}.{_d}.{_e}'

    def __new__(cls, obis_hex: str):
        return str.__new__(cls, obis_hex)


def build_obis(_in) -> ObisCode:
    if not isinstance(_in, str) or len(_in) != 12:
        msg = f'Obis code must be a 12 char hex str (is "{_in}" {type(_in)})!'
        raise ValueError(msg)

    return ObisCode(_in)
