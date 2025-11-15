from enum import IntEnum
from datetime import datetime as dt

from iolink_utils.octetDecoder.octetDecoder import MC, CKT, CKS
from .octetStreamDecoderSettings import DecoderSettings
from .octetStreamDecoderMessages import MasterMessage, DeviceMessage


class MessageState(IntEnum):
    Incomplete = 0,
    Finished = 1

class DecodingState(IntEnum):
    Idle = 0,
    MasterMessage = 1,
    DeviceResponseDelay = 2,
    DeviceMessage = 3


class MasterMessageDecoder:
    def __init__(self, settings: DecoderSettings):
        self.settings: DecoderSettings = settings
        self.octetCount: int = 0
        self.pdOutLen: int = 0
        self.odLen: int = 0

        self.msg: MasterMessage = MasterMessage()

    def processOctet(self, octet, start_time: dt, end_time: dt) -> MessageState:
        if not self._isComplete():
            if self.octetCount == 0:
                self.msg.start_time = start_time
                self.msg.mc = MC.from_buffer_copy(bytes([octet]), 0)
            elif self.octetCount == 1:
                self.msg.ckt = CKT.from_buffer_copy(bytes([octet]), 0)

                payloadLength = self.settings.getPayloadLength(self.msg.ckt.mSeqType)
                self.pdOutLen = payloadLength.pdOut
                self.odLen = payloadLength.od if self.msg.mc.read == 0 else 0
            elif len(self.msg.pdOut) < self.pdOutLen:
                self.msg.pdOut.append(octet)
            elif len(self.msg.od) < self.odLen:
                self.msg.od.append(octet)

            self.octetCount += 1
            self.msg.end_time = end_time
        return MessageState.Finished if self._isComplete() else MessageState.Incomplete

    def _isComplete(self):
        return ((self.octetCount >= 2) and
                len(self.msg.pdOut) == self.pdOutLen and
                len(self.msg.od) == self.odLen)


class DeviceMessageDecoder:
    def __init__(self, settings: DecoderSettings, read: int, mSeqType: int):
        self.settings: DecoderSettings = settings
        self.octetCount: int = 0

        self.msg: DeviceMessage = DeviceMessage()

        payloadLength = self.settings.getPayloadLength(mSeqType)
        self.odLen: int = payloadLength.od if read == 1 else 0
        self.pdInLen: int = payloadLength.pdIn

    def processOctet(self, octet, start_time: dt, end_time: dt) -> MessageState:
        if not self._isComplete():
            if self.octetCount == 0:
                self.msg.start_time = start_time

            if len(self.msg.pdIn) < self.pdInLen:
                self.msg.pdIn.append(octet)
            elif len(self.msg.od) < self.odLen:
                self.msg.od.append(octet)
            else:
                self.msg.cks = CKS.from_buffer_copy(bytes([octet]), 0)

            self.octetCount += 1
            self.msg.end_time = end_time

        return MessageState.Finished if self._isComplete() else MessageState.Incomplete

    def _isComplete(self):
        return (self.octetCount == (self.pdInLen + self.odLen + 1) and
                len(self.msg.pdIn) == self.pdInLen and
                len(self.msg.od) == self.odLen)
