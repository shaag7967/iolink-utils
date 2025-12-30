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


def test_flowControl_eq():
    flow1 = FlowControl(0x10)
    flow2 = FlowControl(0x10)

    assert flow1 == flow2
    assert flow1.state == flow2.state
    assert flow1.value == flow2.value

    flow1 = FlowControl(0x1F)
    assert flow1 != flow2
    assert flow1.state != flow2.state
    assert flow1.value != flow2.value

    assert flow1 != object()


def test_flowControl_copyIsDeep():
    flow1 = FlowControl(0x10)
    flow2 = flow1.copy()

    assert flow1 is not flow2
    assert flow1.state == flow2.state
    assert flow1.value == flow2.value


def test_flowControl_nextCountValue():
    for octet in [0x11, 0x12, 0x1F]:
        flow = FlowControl(octet)
        assert flow.nextCountValue() == 1

    for octet in range(0x00, 0x10):
        flow = FlowControl(octet)
        if octet == 0x0F:
            assert flow.nextCountValue() == 0
        else:
            assert flow.nextCountValue() == octet + 1
