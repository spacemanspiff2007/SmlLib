from typing import Optional

from .crc import get_crc
from .sml_frame import SmlFrame


class CrcError(Exception):
    def __init__(self, msg: bytes, crc_msg: int, crc_calc: int):
        self.msg = msg
        self.crc_msg = crc_msg
        self.crc_calc = crc_calc

    def __repr__(self):
        return f'<{self.__class__.__name__} msg: {self.crc_msg:04x} calc: {self.crc_calc:04x}>'


class SmlStreamReader:
    MAX_SIZE = 50 * 1024

    def __init__(self):
        self.bytes: bytes = b''

    def add(self, _bytes: bytes):
        self.bytes += _bytes
        if len(self.bytes) > SmlStreamReader.MAX_SIZE:
            self.bytes = self.bytes[-1 * SmlStreamReader.MAX_SIZE:]

    def clear(self):
        self.bytes = b''

    def get_frame(self) -> Optional[SmlFrame]:
        start = self.bytes.find(b'\x1B\x1B\x1B\x1B\x01\x01\x01\x01')
        if start == -1:
            return None

        # if we start reading in the mid of a message
        if start != 0:
            self.bytes = self.bytes[start:]
            start = 0

        end = -1
        while (end := self.bytes.find(b'\x1B\x1B\x1B\x1B\x1A', end + 1)) != -1:
            pre = self.bytes[end - 4: end]
            if pre != b'\x1B\x1B\x1B\x1B':
                break

        if end == -1:
            return None

        end += 8
        if len(self.bytes) < end:
            return None

        # remove msg from buffer
        msg = self.bytes[start:end]
        self.bytes = self.bytes[end:]

        # Last three bytes are PADDING, CRC PART 1, CRC PART 2
        padding = msg[-3]

        # check crc
        crc_msg = msg[-2] << 8 | msg[-1]
        crc_calc = get_crc(msg[:-2])
        if crc_msg != crc_calc:
            raise CrcError(msg, crc_msg, crc_calc)

        return SmlFrame(msg[8: -1 * (8 + padding)].replace(b'\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1B', b'\x1B\x1B\x1B\x1B'))
