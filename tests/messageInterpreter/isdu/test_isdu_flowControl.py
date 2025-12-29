import pytest

from iolink_utils.messageInterpreter.isdu.ISDUflowControl import FlowControl, InvalidFlowControlValue


def test_flowControl_init():
    flowControl = FlowControl()

    assert flowControl.state == FlowControl.State.Idle


def test_flowControl_values():
    for value in range(0x00, 0x10):
        assert FlowControl(value).state == FlowControl.State.Count
    assert FlowControl(0x10).state == FlowControl.State.Start
    assert FlowControl(0x11).state == FlowControl.State.Idle
    assert FlowControl(0x12).state == FlowControl.State.Idle
    assert FlowControl(0x1F).state == FlowControl.State.Abort


def test_flowControl_invalidValues():
    for value in range(0x13, 0x1F):
        with pytest.raises(InvalidFlowControlValue):
            FlowControl(value)
    for value in range(0x20, 0x100):  # we stop at 255...
        with pytest.raises(InvalidFlowControlValue):
            FlowControl(value)
