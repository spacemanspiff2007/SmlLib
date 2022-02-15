import typing


class SmlLibException(Exception):
    pass


class CrcError(SmlLibException):
    def __init__(self, msg: bytes, crc_msg: int, crc_calc: int):
        self.msg = msg
        self.crc_msg = crc_msg
        self.crc_calc = crc_calc

    def __repr__(self):
        return f'<{self.__class__.__name__} msg: {self.crc_msg:04x} calc: {self.crc_calc:04x}>'


class InvalidBufferPos(SmlLibException):
    pass


class EndOfSmlMsgExpected(SmlLibException):
    pass


class WrongArgCount(SmlLibException):
    pass


class WrongValueType(SmlLibException):
    pass


class FieldValueTypeDoesNotMatch(SmlLibException):
    def __init__(self, cls, field: str, type: typing.Type[typing.Union[str, int, float]], *args: object) -> None:
        super().__init__(*args)
        self.cls = cls
        self.field: str = field
        self.type: typing.Type[typing.Union[str, int, float]] = type

    def __str__(self) -> str:
        return f'Field value type does not match for for {self.field} in {self.cls.__name__}: {self.type.__name__}'


class UnsupportedChoiceValue(SmlLibException):
    def __init__(self, type: int, *args: object) -> None:
        super().__init__(*args)
        self.type: int = type

    def __str__(self) -> str:
        width = 2 if self.type <= 255 else 4
        return f'Unsupported type 0x{self.type:0{width}x}'
