from ._octetDecoderBase import OctetDecoderBase, ctypes
from iolink_utils.definitions.communicationChannel import CommChannel
from iolink_utils.definitions.transmissionDirection import TransmissionDirection


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


class CycleTimeOctet(OctetDecoderBase):
    _fields_ = [
        ("timeBaseCode", ctypes.c_uint8, 2),
        ("multiplier", ctypes.c_uint8, 6),
    ]


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
