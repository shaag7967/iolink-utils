from enum import IntEnum
from iolink_utils.exceptions import InvalidFlowControlValue


class FlowControl:
    class State(IntEnum):
        Invalid = 0
        Count = 1
        Start = 2
        Idle = 3
        Abort = 4

    def __init__(self, value: int = 0x11):
        self.state = FlowControl.State.Invalid

        # See Table 52 – FlowCTRL definitions
        mappings = [
            (range(0x00, 0x10), FlowControl.State.Count),  # 0x00–0x0F
            ([0x10], FlowControl.State.Start),
            ([0x11, 0x12], FlowControl.State.Idle),
            ([0x1F], FlowControl.State.Abort),
        ]

        for key_range, state in mappings:
            if value in key_range:
                self.state = state
                self.value = value
                return

        raise InvalidFlowControlValue(f"Invalid ISDU FlowControl value: {hex(value)}")
