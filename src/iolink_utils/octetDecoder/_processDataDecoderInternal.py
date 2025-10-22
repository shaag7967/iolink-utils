from iolink_utils.exceptions import InvalidProcessDataSize


def _init(self):
    # init with zero
    if getattr(self, 'pdin_length', None) is not None:
        _decodePDIn(self, bytes(int(self.pdin_length / 8)))
    if getattr(self, 'pdout_length', None) is not None:
        _decodePDOut(self, bytes(int(self.pdout_length / 8)))

def __decodeBinaryProcessData(self, data_format, raw_bytes):
    for element in data_format:
        name = element['name'][0] # using textId as name
        offset = element['bitOffset']
        value_type = element['data']['type']
        length = element['data']['bitLength']

        if value_type == bytearray:
            start_pos = int(offset / 8)
            end_pos = int(start_pos + (length / 8))
            setattr(self, name, raw_bytes[start_pos:end_pos])
        else:
            value = int.from_bytes(raw_bytes, byteorder="big")
            mask = 2 ** length - 1
            setattr(self, name, value_type((value >> offset) & mask))

def _decodePDIn(self, raw_bytes):
    if self.pdin_length != (len(raw_bytes)*8):
        raise InvalidProcessDataSize(f"Raw data size ({len(raw_bytes)*8} bits) does not match PDIn size ({self.pdin_length} bits).")
    __decodeBinaryProcessData(self, self.pdin_format, raw_bytes)

def _decodePDOut(self, raw_bytes):
    if self.pdout_length != (len(raw_bytes)*8):
        raise InvalidProcessDataSize(f"Raw data size ({len(raw_bytes)*8} bits) does not match PDOut size ({self.pdout_length} bits).")
    __decodeBinaryProcessData(self, self.pdout_format, raw_bytes)
