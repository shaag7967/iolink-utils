import sys, os
from dataclasses import dataclass
from typing import Union
from datetime import datetime as dt, timedelta
from enum import IntEnum

from iolink_utils.octetDecoder.octetDecoder import MC, CKT, CKS
from iolink_utils.definitions.bitRate import BitRate
from iolink_utils.definitions.timeing import getMaxFrameTransmissionDelay_master, getMaxResponseTime, \
    getMaxFrameTransmissionDelay_device

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))


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


class MessageState(IntEnum):
    Incomplete = 0,
    Finished = 1


class MasterMessage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.mc: MC = MC()
        self.ckt: CKT = CKT()
        self.pdOut: bytearray = bytearray()
        self.od: bytearray = bytearray()

    def __repr__(self):
        elements = [f"mc={self.mc}", f"ckt={self.ckt}"]
        if self.pdOut:
            elements.append(f"pdOut={bytes(self.pdOut).hex()}")
        if self.od:
            elements.append(f"od={bytes(self.od).hex()}")
        return f"MasterMessage({', '.join(elements)})"


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


class DeviceMessage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.od: bytearray = bytearray()
        self.pdIn: bytearray = bytearray()
        self.cks: CKS = CKS()

    def __repr__(self):
        elements = []
        if self.od:
            elements.append(f"od={bytes(self.od).hex()}")
        if self.pdIn:
            elements.append(f"pdIn={bytes(self.pdIn).hex()}")
        elements.append(f"cks={self.cks}")
        return f"DeviceMessage({', '.join(elements)})"


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


class OctetStreamDecoder:
    class DecodingState(IntEnum):
        Idle = 0,
        MasterMessage = 1,  # max 1 Tbit
        DeviceResponseDelay = 2,  # max 10 Tbit
        DeviceMessage = 3  # max 3 Tbit

    def __init__(self, settings: DecoderSettings):
        self.settings: DecoderSettings = settings

        State = OctetStreamDecoder.DecodingState
        self.state: State = State.Idle
        self.messageDecoder: Union[None, MasterMessage, DeviceMessage] = None
        self.lastMasterMessage: Union[None, MasterMessage] = None
        self.lastDeviceMessage: Union[None, DeviceMessage] = None

        self.lastProcessedOctetEndTime: dt = dt(1970, 1, 1)

        self.timingConstraints = {
            State.Idle: 0,
            State.MasterMessage: getMaxFrameTransmissionDelay_master(self.settings.transmissionRate),
            State.DeviceResponseDelay: getMaxResponseTime(self.settings.transmissionRate),
            State.DeviceMessage: getMaxFrameTransmissionDelay_device(self.settings.transmissionRate),
        }
        self.maxFrameTransmissionDelay: float = self.timingConstraints[State.Idle]

    def _updateTimingConstraint(self, state: DecodingState):
        self.maxFrameTransmissionDelay = self.timingConstraints[state]

    def _isWithinTimingConstraints(self, octetStartTime: dt) -> bool:
        return (octetStartTime - self.lastProcessedOctetEndTime) < timedelta(
            microseconds=self.maxFrameTransmissionDelay)

    def _gotoState(self, state: DecodingState):
        self.state = state
        self._updateTimingConstraint(self.state)

    def processOctet(self, octet, start_time: dt, end_time: dt) -> Union[None, MasterMessage, DeviceMessage]:
        State = OctetStreamDecoder.DecodingState

        if self.state == State.Idle or not self._isWithinTimingConstraints(start_time):
            self.messageDecoder = MasterMessageDecoder(self.settings)
            self._gotoState(State.MasterMessage)
            self.lastMasterMessage = None
            self.lastDeviceMessage = None
        self.lastProcessedOctetEndTime = end_time

        if self.state == State.MasterMessage:
            if self.messageDecoder.processOctet(octet, start_time, end_time) == MessageState.Finished:
                self._gotoState(State.DeviceResponseDelay)
                self.lastMasterMessage = self.messageDecoder.msg
                return self.lastMasterMessage

        if self.state == State.DeviceResponseDelay:
            self.messageDecoder = DeviceMessageDecoder(self.settings, self.lastMasterMessage.mc.read,
                                                       self.lastMasterMessage.ckt.mSeqType)
            self._gotoState(State.DeviceMessage)

        if self.state == State.DeviceMessage:
            if self.messageDecoder.processOctet(octet, start_time, end_time) == MessageState.Finished:
                self._gotoState(State.Idle)
                self.lastDeviceMessage = self.messageDecoder.msg
                return self.lastDeviceMessage

        return None
