from enum import IntEnum, EnumMeta
from iolink_utils.octetDecoder.mSequenceCapability import MSequenceCapability


class AutoNameConvertMeta(EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, str):
            # resolve by name
            try:
                return cls[value]
            except KeyError:
                pass
            # resolve by int string
            try:
                value = int(value)
            except ValueError:
                raise ValueError(f"Cannot convert '{value}' to {cls.__name__}")
        return super().__call__(value, *args, **kwargs)

class BitRate(IntEnum, metaclass=AutoNameConvertMeta):
    Undefined = 0
    COM1 = 4800
    COM2 = 38400
    COM3 = 230400


class PhysicalLayer:
    def __init__(self):
        self.bitrate: BitRate = BitRate.Undefined
        self.min_cycle_time = 0
        self.sio_supported = False
        self.m_sequence_capability: MSequenceCapability = MSequenceCapability(0)

    def __str__(self):
        return (
            f"PhysicalLayer("
            f"bitrate={self.bitrate.name} ({self.bitrate.value}), "
            f"min_cycle_time={self.min_cycle_time}, "
            f"sio_supported={self.sio_supported}, "
            f"m_sequence_capability={self.m_sequence_capability})"
        )