class ObisCode(str):
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
        obj = str.__new__(cls, obis_hex)
        return obj


def build_obis(_in) -> ObisCode:
    if not isinstance(_in, str) or len(_in) != 12:
        raise ValueError(f'Obis code must be a 12 char hex str (is "{_in}" {type(_in)})!')

    return ObisCode(_in)
