from typing import List, Optional

from .sml_fields import EndofSmlMsg, SmlListEntry, SmlMessage


class InvalidBufferPos(Exception):
    pass


class SmlFrame:
    def __init__(self, buffer: bytes):
        self.bytes = buffer
        self.buffer = memoryview(buffer)
        self.buf_len = len(buffer)

        self.next_pos = 0

    def get_value(self, pos: Optional[int] = None):
        if pos is None:
            pos = self.next_pos

        # check start pos
        if pos >= self.buf_len:
            raise InvalidBufferPos(f'Start pos bigger than buffer: {pos} > {self.buf_len}')

        v = self.buffer[pos]

        # No value
        if v == 0x01:
            self.next_pos = pos + 1
            return None

        # Bool
        if v == 0x42:
            self.next_pos = pos + 2
            return bool(self.buffer[pos + 1])

        # End of a SmlMSg
        if v == 0x00:
            self.next_pos = pos + 1
            return EndofSmlMsg

        # types with dynamic size
        s_pos = pos
        is_long = bool(v & 0x80)
        _type = v & 0x70  # type
        _size = v & 0x0F  # size including the 1-byte tag
        while is_long:
            s_pos += 1
            v = self.buffer[s_pos]
            _size = _size << 4 | v & 0x0F
            is_long = bool(v & 0x80)

        # type is a list
        if _type == 0x70:
            self.next_pos = s_pos + 1   # Must be s_pos because we can have lists with a long length
            return [None for i in range(_size)]

        # End position
        e_pos = pos + _size
        if e_pos > self.buf_len:
            raise InvalidBufferPos(f'Pos bigger than buffer: {e_pos} > {self.buf_len}')
        self.next_pos = e_pos

        # 0x50: signed integer, 0x60 unsigned integer
        if _type in (0x50, 0x60):
            return int.from_bytes(
                self.buffer[s_pos + 1:e_pos], byteorder='big', signed=True if _type == 0x50 else False
            )

        # 0x00: octet str
        if _type == 0x00:
            return self.buffer[s_pos + 1:e_pos].hex()

        raise ValueError(f'Unknown data type: {_type:02x}!')

    def parse_frame(self) -> List[SmlMessage]:
        ret = []
        while self.next_pos < self.buf_len:

            if not self.buffer[self.next_pos] == 0x76:
                raise ValueError(
                    f'No start of SML Message found at {self.next_pos}: 0x{self.buffer[self.next_pos]:x}\n'
                    f'{self.buffer.hex()}'
                )

            # This will always return a list
            val = self.get_value()
            self._parse_msg(val)
            if val[-1] != EndofSmlMsg:
                raise ValueError(f'Last Entry is not {EndofSmlMsg}! Something went wrong!')

            ret.append(SmlMessage.from_list(val))
        return ret

    def _parse_msg(self, parent_obj=None):
        # it's always a list now
        for i, _ in enumerate(parent_obj):
            parent_obj[i] = v = self.get_value()
            if isinstance(v, list):
                self._parse_msg(v)

    def get_obis(self) -> List[SmlListEntry]:
        """Returns all obis values in the frame without parsing the frame"""
        ret = []
        start = -1
        while (start := self.bytes.find(b'\x77\x07\x01', start + 1)) != -1:
            data = self.get_value(start)
            if not isinstance(data, list):
                continue

            self._parse_msg(data)
            ret.append(SmlListEntry.from_list(data))
        return ret
