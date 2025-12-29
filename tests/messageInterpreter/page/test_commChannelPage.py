from datetime import datetime as dt

from iolink_utils.messageInterpreter.page.commChannelPage import CommChannelPage, TransactionPage
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage


def test_commChannelPage_reset():
    channel = CommChannelPage()
    channel._direction = TransmissionDirection.Write
    channel._pageIndex = 10
    channel._octet = 20

    channel.reset()

    assert channel._direction == TransmissionDirection.Read
    assert channel._pageIndex == 0
    assert channel._octet == 0


def test_commChannelPage_write():
    channel = CommChannelPage()

    masterMsg = MasterMessage()
    masterMsg.startTime = dt(1999, 1, 2)
    masterMsg.endTime = dt(2000, 3, 4)
    masterMsg.mc.read = 0  # write
    masterMsg.mc.address = 3
    masterMsg.od.append(4)

    assert channel.handleMasterMessage(masterMsg) is None

    deviceMsg = DeviceMessage()
    deviceMsg.startTime = dt(2000, 5, 6)
    deviceMsg.endTime = dt(2001, 7, 8)
    deviceMsg.od.append(5)

    transaction: TransactionPage = channel.handleDeviceMessage(deviceMsg)

    assert transaction.startTime == dt(1999, 1, 2)
    assert transaction.endTime == dt(2001, 7, 8)
    assert transaction.direction == TransmissionDirection.Write
    assert transaction.index == 3
    assert transaction.value == 4


def test_commChannelPage_read():
    channel = CommChannelPage()

    masterMsg = MasterMessage()
    masterMsg.startTime = dt(1999, 1, 2)
    masterMsg.endTime = dt(2000, 3, 4)
    masterMsg.mc.read = 1  # read
    masterMsg.mc.address = 5

    assert channel.handleMasterMessage(masterMsg) is None

    deviceMsg = DeviceMessage()
    deviceMsg.startTime = dt(2000, 5, 6)
    deviceMsg.endTime = dt(2001, 7, 8)
    deviceMsg.od.append(6)

    transaction: TransactionPage = channel.handleDeviceMessage(deviceMsg)

    assert transaction.startTime == dt(1999, 1, 2)
    assert transaction.endTime == dt(2001, 7, 8)
    assert transaction.direction == TransmissionDirection.Read
    assert transaction.index == 5
    assert transaction.value == 6
