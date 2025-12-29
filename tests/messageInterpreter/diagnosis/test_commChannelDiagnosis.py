import pytest
from datetime import datetime as dt

from iolink_utils.messageInterpreter.diagnosis.commChannelDiagnosis import (
    CommChannelDiagnosis,
    TransactionDiagEventMemory,
    TransactionDiagEventReset
)
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.exceptions import UnexpectedMasterMessageReceived


def _createMasterMessage(read: int, address: int, day: int) -> MasterMessage:
    msg = MasterMessage()
    msg.startTime = dt(2000, 1, day)
    msg.endTime = dt(2000, 1, day)
    msg.mc.read = read
    msg.mc.address = address
    return msg


def _createDeviceMessage(data: int, month: int) -> DeviceMessage:
    msg = DeviceMessage()
    msg.startTime = dt(2000, month, 1)
    msg.endTime = dt(2000, month, 1)
    msg.od.append(data)
    return msg


def test_commChannelDiagnosis_reset():
    channel = CommChannelDiagnosis()

    channel._state = CommChannelDiagnosis.State.ResetEventFlag
    channel.reset()

    assert channel._state == CommChannelDiagnosis.State.Idle


def test_commChannelDiagnosis_readEventMemory():
    channel = CommChannelDiagnosis()
    assert channel._state == CommChannelDiagnosis.State.Idle

    # read octet 1 of 4
    msg = _createMasterMessage(1, 0, 1)
    assert channel.handleMasterMessage(msg) is None
    assert channel._eventMemoryIndex == 0
    assert channel._startTime == dt(2000, 1, 1)
    assert channel._state == CommChannelDiagnosis.State.ReadEventMemory

    msg = _createDeviceMessage(0x82, 2)  # details + evt2
    assert channel.handleDeviceMessage(msg) is None
    assert channel._endTime == dt(2000, 2, 1)

    # read octet 2 of 4
    msg = _createMasterMessage(1, 4, 2)
    assert channel.handleMasterMessage(msg) is None
    assert channel._eventMemoryIndex == 4
    assert channel._startTime == dt(2000, 1, 1)
    assert channel._state == CommChannelDiagnosis.State.ReadEventMemory

    msg = _createDeviceMessage(0xF4, 2)  # status code
    assert channel.handleDeviceMessage(msg) is None
    assert channel._endTime == dt(2000, 2, 1)

    # read octet 3 of 4
    msg = _createMasterMessage(1, 5, 3)
    assert channel.handleMasterMessage(msg) is None
    assert channel._eventMemoryIndex == 5
    assert channel._startTime == dt(2000, 1, 1)
    assert channel._state == CommChannelDiagnosis.State.ReadEventMemory

    msg = _createDeviceMessage(0xAA, 3)  # code MSB
    assert channel.handleDeviceMessage(msg) is None
    assert channel._endTime == dt(2000, 3, 1)

    # read octet 4 of 4
    msg = _createMasterMessage(1, 6, 4)
    assert channel.handleMasterMessage(msg) is None
    assert channel._eventMemoryIndex == 6
    assert channel._startTime == dt(2000, 1, 1)
    assert channel._state == CommChannelDiagnosis.State.ReadEventMemory

    msg = _createDeviceMessage(0xBB, 4)  # code LSB
    transaction = channel.handleDeviceMessage(msg)
    assert channel._eventMemory.isComplete()
    assert channel._state == CommChannelDiagnosis.State.Idle
    assert type(transaction) == TransactionDiagEventMemory
    assert transaction.startTime == dt(2000, 1, 1)
    assert transaction.endTime == dt(2000, 4, 1)
    assert transaction.eventMemory.isComplete()
    assert int(transaction.eventMemory.statusCode) == 0x82
    assert transaction.eventMemory.events[1].qualifier.get() == 0xF4
    assert transaction.eventMemory.events[1].code == 0xAABB


def test_commChannelDiagnosis_resetEventFlag():
    channel = CommChannelDiagnosis()
    assert channel._state == CommChannelDiagnosis.State.Idle

    msg = _createMasterMessage(0, 0, 1)  # write address 0
    msg.od.append(123)
    assert channel.handleMasterMessage(msg) is None
    assert channel._eventMemoryIndex == 0
    assert channel._startTime == dt(2000, 1, 1)
    assert channel._state == CommChannelDiagnosis.State.ResetEventFlag

    msg = _createDeviceMessage(0x00, 2)
    msg.od = bytearray()  # remove data
    transaction = channel.handleDeviceMessage(msg)
    assert not channel._eventMemory.isComplete()
    assert channel._state == CommChannelDiagnosis.State.Idle
    assert type(transaction) == TransactionDiagEventReset
    assert transaction.startTime == dt(2000, 1, 1)
    assert transaction.endTime == dt(2000, 2, 1)


def test_commChannelDiagnosis_invalidMasterMessage():
    channel = CommChannelDiagnosis()
    assert channel._state == CommChannelDiagnosis.State.Idle

    msg = MasterMessage()
    msg.startTime = dt(2000, 1, 1)
    msg.endTime = dt(2000, 1, 2)
    msg.mc.read = 0  # write
    msg.mc.address = 1  # INVALID

    with pytest.raises(UnexpectedMasterMessageReceived):
        channel.handleMasterMessage(msg)
