from datetime import datetime as dt

from iolink_utils.messageInterpreter.process.commChannelProcess import CommChannelProcess, TransactionProcess
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage


def test_commChannelProcess_reset():
    channel = CommChannelProcess()
    channel._direction = TransmissionDirection.Write

    channel.reset()

    assert channel._direction == TransmissionDirection.Read


def test_commChannelProcess_handleMasterMessage():
    channel = CommChannelProcess()

    masterMsg = MasterMessage()
    masterMsg.startTime = dt(1999, 1, 2)
    masterMsg.endTime = dt(2000, 3, 4)
    masterMsg.mc.read = 0  # write

    transaction: TransactionProcess = channel.handleMasterMessage(masterMsg)

    assert transaction.startTime == dt(1999, 1, 2)
    assert transaction.endTime == dt(2000, 3, 4)
    assert transaction.direction == TransmissionDirection.Write


def test_commChannelProcess_handleDeviceMessage():
    channel = CommChannelProcess()

    deviceMsg = DeviceMessage()
    deviceMsg.startTime = dt(2000, 5, 6)
    deviceMsg.endTime = dt(2001, 7, 8)

    transaction: TransactionProcess = channel.handleDeviceMessage(deviceMsg)

    assert transaction.startTime == dt(2000, 5, 6)
    assert transaction.endTime == dt(2001, 7, 8)
