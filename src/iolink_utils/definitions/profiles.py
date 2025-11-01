from enum import IntEnum


class ProfileID(IntEnum):
    Undefined               = 0
    MeasuringSensorHighRes  = 11     # 0x000B
    AdjustableSwitchingSensorTwoChannel  = 14     # 0x000E
    BlobTransfer            = 48     # 0x0030
    FirmwareUpdate          = 49     # 0x0031
    IdentificationDiagnosis = 16384  # 0x4000
    SafetyDevice            = 16385  # 0x4001
    WirelessDevice          = 16386  # 0x4002
    ProcessDataVariable     = 32770  # 0x8002
    AdjustableSwitchingSignalChannel     = 32774  # 0x
    MultipleAdjustableSwitchingSignalChannel     = 32781  # 0x
    ExtendedIdentification  = 33024  # 0x8100
