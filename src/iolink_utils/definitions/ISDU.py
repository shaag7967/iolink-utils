from enum import IntEnum


# See Table A.12 – Definition of the nibble "I-Service"
class IServiceNibble(IntEnum):
    NoService = 0b0000,
    M_WriteReq_8bitIdx = 0b0001,
    M_WriteReq_8bitIdxSub = 0b0010,
    M_WriteReq_16bitIdxSub = 0b0011,
    D_WriteResp_M = 0b0100,
    D_WriteResp_P = 0b0101,
    M_ReadReq_8bitIdx = 0b1001,
    M_ReadReq_8bitIdxSub = 0b1010,
    M_ReadReq_16bitIdxSub = 0b1011,
    D_ReadResp_M = 0b1100,
    D_ReadResp_P = 0b1101


# See Table 52 – FlowCTRL definitions
class FlowCtrl:
    class State(IntEnum):
        Count = 0
        Start = 1
        Idle = 2
        Reserved = 3
        Abort = 4

    def __init__(self, value: int = 0x11):
        mappings = [
            (range(0x00, 0x10), FlowCtrl.State.Count),  # 0x00–0x0F
            ([0x10], FlowCtrl.State.Start),
            ([0x11, 0x12], FlowCtrl.State.Idle),
            (range(0x13, 0x1F), FlowCtrl.State.Reserved),  # 0x13–0x1E
            ([0x1F], FlowCtrl.State.Abort),
        ]

        for key_range, state in mappings:
            if value in key_range:
                self.state = state
                self.value = value
                return

        raise ValueError(f"Invalid FlowCtrl value: {value}")
