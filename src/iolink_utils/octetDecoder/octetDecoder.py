from ._octetDecoderBase import OctetDecoderBase, ctypes
from iolink_utils.exceptions import InvalidCycleTime, InvalidOctetValue
from iolink_utils.definitions.communicationChannel import CommChannel
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from math import ceil


class MC(OctetDecoderBase):
    """M-sequence control (MC)"""
    _fields_ = [
        ("read", ctypes.c_uint8, 1),
        ("channel", ctypes.c_uint8, 2),
        ("address", ctypes.c_uint8, 5)
    ]

    def __repr__(self):
        return f"MC({TransmissionDirection(self.read).name}, channel={CommChannel(self.channel).name}, address={self.address})"


class CKT(OctetDecoderBase):
    _fields_ = [
        ("mSeqType", ctypes.c_uint8, 2),
        ("checksum", ctypes.c_uint8, 6)
    ]


class CKS(OctetDecoderBase):
    _fields_ = [
        ("eventFlag", ctypes.c_uint8, 1),
        ("pdValid", ctypes.c_uint8, 1),
        ("checksum", ctypes.c_uint8, 6)
    ]


class IService(OctetDecoderBase):
    _fields_ = [
        ("service", ctypes.c_uint8, 4),
        ("length", ctypes.c_uint8, 4)
    ]


class StatusCodeType1(OctetDecoderBase):
    _fields_ = [
        ("details", ctypes.c_uint8, 1),
        ("pdValid", ctypes.c_uint8, 1),
        ("unused", ctypes.c_uint8, 1),
        ("eventCode", ctypes.c_uint8, 5)
    ]


class StatusCodeType2(OctetDecoderBase):
    _fields_ = [
        ("details", ctypes.c_uint8, 1),
        ("unused", ctypes.c_uint8, 1),
        ("activatedEvents", ctypes.c_uint8, 6)
    ]


class EventQualifier(OctetDecoderBase):
    _fields_ = [
        ("mode", ctypes.c_uint8, 2),
        ("type", ctypes.c_uint8, 2),
        ("source", ctypes.c_uint8, 1),
        ("instance", ctypes.c_uint8, 3)
    ]

# TODO make class CycleTime
# with conversion functions
# move all ms calculation code into other class
class CycleTimeOctet(OctetDecoderBase):
    """
    Decodes or encodes a cycle time field.

    timeBaseCode (2 bits) and multiplier (6 bits) together encode
    a time in milliseconds according to predefined base tables.
    """
    _fields_ = [
        ("timeBaseCode", ctypes.c_uint8, 2),
        ("multiplier", ctypes.c_uint8, 6),
    ]

    _PARAMS = {
        0: {"offset": 0.0, "base": 0.1, "range": (0.4, 6.3)},
        1: {"offset": 6.4, "base": 0.4, "range": (6.4, 31.6)},
        2: {"offset": 32.0, "base": 1.6, "range": (32.0, 132.8)},
    }

    def getTimeInMs(self) -> float:
        """Return the decoded time value in milliseconds."""
        params = self._PARAMS.get(self.timeBaseCode)
        if not params:
            raise InvalidOctetValue(f"Invalid timeBaseCode: {self.timeBaseCode}")
        return round(params["offset"] + params["base"] * self.multiplier, 1)

    def setTimeInMs(self, value: float) -> None:
        """Set the encoded time fields for the given millisecond value."""
        if value < 0:
            raise InvalidCycleTime("Time value must be non-negative")

        if value == 0:
            self.timeBaseCode = 0
            self.multiplier = 0
            return

        for code, params in self._PARAMS.items():
            min_v, max_v = params["range"]
            if min_v <= value <= max_v:
                self.timeBaseCode = code
                self.multiplier = ceil(round((value - params["offset"]) / params["base"], 1))
                return

        raise InvalidCycleTime(f"Value {value} ms out of supported range")

MasterCycleTimeOctet = CycleTimeOctet
MinCycleTimeOctet = CycleTimeOctet


class MSequenceCapability(OctetDecoderBase):
    _fields_ = [
        ("unused", ctypes.c_uint8, 2),
        ("preoperateCode", ctypes.c_uint8, 2),
        ("operateCode", ctypes.c_uint8, 3),
        ("isduSupport", ctypes.c_uint8, 1)
    ]


class RevisionId(OctetDecoderBase):
    _fields_ = [
        ("majorRev", ctypes.c_uint8, 4),
        ("minorRev", ctypes.c_uint8, 4)
    ]


class ProcessDataIn(OctetDecoderBase):
    _fields_ = [
        ("byte", ctypes.c_uint8, 1),
        ("sio", ctypes.c_uint8, 1),
        ("unused", ctypes.c_uint8, 1),
        ("length", ctypes.c_uint8, 5)
    ]


class ProcessDataOut(OctetDecoderBase):
    _fields_ = [
        ("byte", ctypes.c_uint8, 1),
        ("unused", ctypes.c_uint8, 2),
        ("length", ctypes.c_uint8, 5)
    ]
