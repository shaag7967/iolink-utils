from dataclasses import dataclass
from iolink_utils.definitions.bitRate import BitRate


@dataclass(frozen=True)
class MSeqPayloadLength:
    pdOut: int = 0
    od: int = 0
    pdIn: int = 0


class DecoderSettings:
    def __init__(self):
        self.transmissionRate: BitRate = BitRate('Undefined')
        self.startup: MSeqPayloadLength = MSeqPayloadLength()
        self.preoperate: MSeqPayloadLength = MSeqPayloadLength()
        self.operate: MSeqPayloadLength = MSeqPayloadLength()

    def getPayloadLength(self, mSeqType: int) -> MSeqPayloadLength:
        if mSeqType == 0:
            return self.startup
        elif mSeqType == 1:
            return self.preoperate
        elif mSeqType == 2:
            return self.operate
        else:
            raise ValueError(f"Invalid M-Sequence type: '{mSeqType}'")
