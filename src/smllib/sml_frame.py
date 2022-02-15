from typing import List, Optional

from smllib.builder import create_context, CTX_HINT
from smllib.errors import InvalidBufferPos
from smllib.sml import EndOfSmlMsg, SmlListEntry, SmlMessage
from smllib.sml_frame_snippet import SmlFrameSnippet


class SmlFrame:
    def __init__(self, buffer: bytes, build_ctx: CTX_HINT = None, msg_ctx: Optional[bytes] = None):
        self.bytes = buffer
        self.buffer = memoryview(buffer)
        self.buf_len = len(buffer)

        self.next_pos = 0

        self.msg_ctx = msg_ctx  # This is the whole sml message
        self.build_ctx: CTX_HINT = build_ctx if build_ctx is not None else create_context()

    def get_value(self, pos: Optional[int] = None) -> SmlFrameSnippet:
        if pos is None:
            pos = self.next_pos
        snip_start = pos

        # check start pos
        if pos >= self.buf_len:
            raise InvalidBufferPos(f'Start pos bigger than buffer: {pos} > {self.buf_len}')

        # advance
        v = self.buffer[pos]
        start = pos + 1

        # ----------------------------------------
        # types with fixed size
        # ----------------------------------------

        # No value
        if v == 0x01:
            self.next_pos = start
            return SmlFrameSnippet(None, snip_start, start, self.buffer)

        # End of a SmlMSg
        if v == 0x00:
            self.next_pos = start
            return SmlFrameSnippet(EndOfSmlMsg, snip_start, start, self.buffer)

        # Bool
        if v == 0x42:
            self.next_pos = start + 1
            return SmlFrameSnippet(bool(self.buffer[start]), snip_start, self.next_pos, self.buffer)

        # ----------------------------------------
        # types with dynamic size
        # ----------------------------------------
        is_long = bool(v & 0x80)
        _type = v & 0x70  # type
        _size = v & 0x0F  # size including the 1-byte tag
        while is_long:
            v = self.buffer[start]
            _size = _size << 4 | v & 0x0F
            is_long = bool(v & 0x80)
            start += 1

        # type is a list
        if _type == 0x70:
            self.next_pos = start   # Must be s_pos because we can have lists with a long length
            return SmlFrameSnippet([None for _ in range(_size)], snip_start)

        # End position
        end = pos + _size
        if end > self.buf_len:
            raise InvalidBufferPos(f'Pos bigger than buffer: {end} > {self.buf_len}')
        self.next_pos = end

        # 0x50: signed integer, 0x60 unsigned integer
        if _type == 0x50 or _type == 0x60:
            return SmlFrameSnippet(
                int.from_bytes(self.buffer[start:end], byteorder='big', signed=_type == 0x50),
                snip_start, end, self.buffer
            )

        # 0x00: octet str
        if _type == 0x00:
            return SmlFrameSnippet(self.buffer[start:end].hex(), snip_start, end, self.buffer)

        raise ValueError(f'Unknown data type: {_type:02x}!')

    def parse_frame(self) -> List[SmlMessage]:
        ret = []
        self.next_pos = 0
        while self.next_pos < self.buf_len:

            if not self.buffer[self.next_pos] == 0x76:
                raise ValueError(
                    f'No start of SML Message found at {self.next_pos}: 0x{self.buffer[self.next_pos]:x}\n'
                    f'{self.buffer.hex()}'
                )

            # This will always return a list
            val = self._parse_msg(self.get_value())
            ret.append(self.build_ctx[SmlMessage].build(val, self.build_ctx))
        return ret

    def _parse_msg(self, parent_obj: SmlFrameSnippet) -> SmlFrameSnippet:
        # it's always a list now
        _lst = parent_obj.get_value(list)
        for i, _ in enumerate(_lst):
            _lst[i] = v = self.get_value()
            if isinstance(v.value, list):
                self._parse_msg(v)
        parent_obj.stop_pos(self.next_pos, self.buffer)
        return parent_obj

    def get_obis(self) -> List[SmlListEntry]:
        """Returns all obis values in the frame without parsing the frame"""
        ret = []
        pos = 0
        while (pos := self.bytes.find(b'\x77\x07\x01', pos)) != -1:
            data = self.get_value(pos)
            if not isinstance(data.value, list):
                continue

            self._parse_msg(data)
            ret.append(self.build_ctx[SmlListEntry].build(data, self.build_ctx))

            # Don't search in the frame again since the payload might contain '770701'
            pos = self.next_pos
        return ret
