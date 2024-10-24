from typing import Callable, Literal, Optional, Union

import smllib.crc as crc_module
from smllib.builder import CTX_HINT, create_context
from smllib.errors import CrcError
from smllib.sml_frame import SmlFrame


class SmlStreamReader:
    MAX_SIZE = 50 * 1024

    def __init__(self, build_ctx: Optional[CTX_HINT] = None, crc: Literal['kermit', 'x25'] = 'x25') -> None:
        self.bytes: bytes = b''
        self.build_ctx: CTX_HINT = build_ctx if build_ctx is not None else create_context()

        # This makes it easy to patch additional crc functions to the module
        try:
            self.crc_func: Callable[[Union[memoryview, bytes]], int] = getattr(crc_module, crc).get_crc
        except AttributeError:
            available = [f'"{n:s}"' for n in dir(crc_module) if not n.startswith('_')]
            raise ValueError(f'Unsupported CRC "{crc}"! Available: {", ".join(available):s}')

    def add(self, _bytes: bytes) -> None:
        self.bytes += _bytes
        if len(self.bytes) > SmlStreamReader.MAX_SIZE:
            self.bytes = self.bytes[-1 * SmlStreamReader.MAX_SIZE:]

    def clear(self) -> None:
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
        crc_calc = self.crc_func(msg[:-2])
        if crc_msg != crc_calc:
            raise CrcError(msg, crc_msg, crc_calc)

        frame = msg[8: -1 * (8 + padding)].replace(b'\x1B\x1B\x1B\x1B\x1B\x1B\x1B\x1B', b'\x1B\x1B\x1B\x1B')
        return SmlFrame(frame, msg_ctx=msg, build_ctx=self.build_ctx)
