UNITS = {
    1: 'a',
    2: 'mo',
    3: 'wk',
    4: 'd',
    5: 'h',
    6: 'min',
    7: 's',
    8: '°',
    9: '°C',
    10: 'currency',
    11: 'm',
    12: 'm/s',
    13: 'm³',
    14: 'm³',
    15: 'm³/h',
    16: 'm³/h',
    17: 'm³/d',
    18: 'm³/d',
    19: 'l',
    20: 'kg',
    21: 'N',
    22: 'Nm',
    23: 'Pa',
    24: 'bar',
    25: 'J',
    26: 'J/h',
    27: 'W',
    28: 'VA',
    29: 'var',
    30: 'Wh',
    31: 'VAh',
    32: 'varh',
    33: 'A',
    34: 'C',
    35: 'V',
    36: 'V/m',
    37: 'F',
    38: 'Ω',
    39: 'Ωm²/m',
    40: 'Wb',
    41: 'T',
    42: 'A/m',
    43: 'H',
    44: 'Hz',
    45: '1/(Wh)',
    46: '1/(varh)',
    47: '1/(VAh)',
    48: 'V²h',
    49: 'A²h',
    50: 'kg/s',
    51: 'S',
    52: 'K',
    53: '1/(V²h)',
    54: '1/(A²h)',
    55: '1/m³',
    56: '%',
    57: 'Ah',
    60: 'Wh/m³',
    61: 'J/m³',
    62: 'Mol%',
    63: 'g/m³',
    64: 'Pas',
    65: 'J/kg',
    66: 'g/cm²',
    67: 'arm',
    70: 'dBm',
    71: 'dBµV',
    72: 'dB',
}

# https://www.promotic.eu/en/pmdoc/Subsystems/Comm/PmDrivers/IEC62056_OBIS.htm
OBIS_NAMES = {
    '0100000009ff': 'Geräteeinzelidentifikation',
    '0100010800ff': 'Zählerstand Bezug Total',
    '0100010801ff': 'Zählerstand Bezug Tarif 1',
    '0100010802ff': 'Zählerstand Bezug Tarif 2',
    '0100010803ff': 'Zählerstand Bezug Tarif 3',
    '0100010804ff': 'Zählerstand Bezug Tarif 4',
    '0100011100ff': 'Total-Zählerstand',
    '0100020800ff': 'Zählerstand Einspeisung Total',
    '0100020801ff': 'Zählerstand Einspeisung Tarif 1',
    '0100020802ff': 'Zählerstand Einspeisung Tarif 2',
    '0100020803ff': 'Zählerstand Einspeisung Tarif 3',
    '0100020804ff': 'Zählerstand Einspeisung Tarif 4',
    '01000b0600ff': 'Maximalstrom Total',
    '01000b0700ff': 'Momentanstrom Total',
    '01000c0700ff': 'Momentanspannung Total',
    '01000e0700ff': 'Netzfrequenz',
    '0100100700ff': 'aktuelle Wirkleistung',
    '0100150700ff': 'Momentanwirkleistung Bezug L1',
    '0100160700ff': 'Momentanwirkleistung Einspeisung L1',
    '0100170700ff': 'Momentanblindleistung Bezug L1',
    '0100180700ff': 'Momentanblindleistung Einspeisung L1',
    '01001f0600ff': 'Maximalstrom L1',
    '01001f0700ff': 'Momentanstrom L1',
    '0100200700ff': 'Momentanspannung L1',
    '0100240700ff': 'Summenwirkleistung L1',
    '0100290700ff': 'Momentanwirkleistung Bezug L2',
    '01002a0700ff': 'Momentanwirkleistung Einspeisung L2',
    '01002b0700ff': 'Momentanblindleistung Bezug L2',
    '01002c0700ff': 'Momentanblindleistung Einspeisung L2',
    '0100330600ff': 'Maximalstrom L2',
    '0100330700ff': 'Momentanstrom L2',
    '0100340700ff': 'Momentanspannung L2',
    '0100380700ff': 'Summenwirkleistung L2',
    '01003d0700ff': 'Momentanwirkleistung Bezug L3',
    '01003e0700ff': 'Momentanwirkleistung Einspeisung L3',
    '01003f0700ff': 'Momentanblindleistung Bezug L3',
    '0100400700ff': 'Momentanblindleistung Einspeisung L3',
    '0100470600ff': 'Maximalstrom L3',
    '0100470700ff': 'Momentanstrom L3',
    '0100480700ff': 'Momentanspannung L3',
    '01004c0700ff': 'Summenwirkleistung L3',
    '0100510701ff': 'Phasenabweichung Spannungen L1/L2',
    '0100510702ff': 'Phasenabweichung Spannungen L1/L3',
    '0100510704ff': 'Phasenabweichung Strom/Spannung L1',
    '010051070fff': 'Phasenabweichung Strom/Spannung L2',
    '010051071aff': 'Phasenabweichung Strom/Spannung L3',
    '010060320002': 'Aktuelle Chiptemperatur',
    '010060320003': 'Minimale Chiptemperatur',
    '010060320004': 'Maximale Chiptemperatur',
    '010060320005': 'Gemittelte Chiptemperatur',
    '010060320303': 'Spannungsminimum',
    '010060320304': 'Spannungsmaximum',
    '8181c78203ff': 'Hersteller-Identifikation',
    '8181c78205ff': 'Öffentlicher Schlüssel',
}
