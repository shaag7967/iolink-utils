from typing import Dict
from datetime import datetime as dt

import pytest

from iolink_utils.exceptions import InvalidISDUService
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.iServiceNibble import IServiceNibble
from iolink_utils.definitions.ioLinkIndex import IOLinkIndex
from iolink_utils.messageInterpreter.isdu.ISDU import ISDU


# test implementation of abstract class ISDU
class MyISDU(ISDU):
    _SERVICE_NIBBLE: IServiceNibble = IServiceNibble.NoService

    def _onFinished(self):
        pass

    def data(self) -> Dict:
        raise AssertionError("data() not expected to be called in this test")


def test_ISDU_ctor():
    isdu = MyISDU()
    assert isdu._service.service == IServiceNibble.NoService
    assert isdu._service.length == 0
    assert not isdu._hasExtendedLength()
    assert not isdu.isComplete
    assert not isdu.isValid
    assert len(isdu._rawData) == 0
    assert isdu._chkpdu == 0


def test_ISDU_setEndTime():
    isdu = MyISDU()
    isdu.setTime(dt(2000, 1, 1), dt(2001, 2, 2))
    assert isdu.startTime == dt(2000, 1, 1)
    assert isdu.endTime == dt(2001, 2, 2)

    isdu.setEndTime(dt(3000, 3, 3))
    assert isdu.endTime == dt(3000, 3, 3)


def test_ISDU_length():
    isdu = MyISDU()
    assert not isdu._hasExtendedLength()

    service = IService()
    service.service = IServiceNibble.NoService
    service.length = 5

    assert not isdu.appendOctets(bytearray([int(service)]))
    assert isdu._service.length == 5
    assert isdu._getTotalLength() == 5


def test_ISDU_extendedLength():
    isdu = MyISDU()
    assert not isdu._hasExtendedLength()

    service = IService(service=IServiceNibble.NoService, length=1)  # ext length
    assert not isdu.appendOctets(bytearray([int(service), 25]))
    assert isdu._hasExtendedLength()
    assert isdu._getTotalLength() == 25


def test_ISDU_appendOctets():
    isdu = MyISDU()
    isdu.appendOctets(bytearray())
    assert len(isdu._rawData) == 0

    service = IService(service=IServiceNibble.NoService, length=5)
    isdu.appendOctets(bytearray([int(service), 0x0B]))
    assert not isdu._hasExtendedLength()
    assert isdu._getTotalLength() == 5
    assert len(isdu._rawData) == 2

    isdu.appendOctets(bytearray([0x0C, 0x0D, 0x0E]))
    assert len(isdu._rawData) == 5
    assert isdu.isComplete


def test_ISDU_appendOctets_invalidService():
    isdu = MyISDU()
    assert isdu._SERVICE_NIBBLE == IServiceNibble.NoService

    service = IService(service=IServiceNibble.M_ReadReq_8bitIdxSub, length=5)
    with pytest.raises(InvalidISDUService):
        isdu.appendOctets(bytearray([int(service), 0x11, 0x22]))


def test_ISDU_replaceTrailingOctets():
    isdu = MyISDU()
    isdu.replaceTrailingOctets(bytearray())
    assert len(isdu._rawData) == 0

    service = IService(service=IServiceNibble.NoService, length=5)
    isdu.appendOctets(bytearray([int(service), 0x0B]))
    assert isdu._getTotalLength() == 5
    assert len(isdu._rawData) == 2

    service = IService(service=IServiceNibble.NoService, length=10)
    isdu.replaceTrailingOctets(bytearray([int(service), 0xAA, 0xBB]))
    assert isdu._getTotalLength() == 10
    assert len(isdu._rawData) == 3
    assert isdu._rawData[1] == 0xAA
    assert isdu._rawData[2] == 0xBB


def test_ISDU_dispatch(mocker):
    handler = mocker.Mock()

    req = MyISDU()
    req.dispatch(handler)

    handler.handleISDU.assert_called_once_with(req)


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, "0 / 0x0000"),
        (4, "4 / 0x0004"),
        (IOLinkIndex.SystemCommand.value, "2 / 0x0002 (SystemCommand)"),
        (IOLinkIndex.ProductID.value, "19 / 0x0013 (ProductID)"),
        (IOLinkIndex.HW_ID_Key.value, "17342 / 0x43BE (HW_ID_Key)"),
    ],
)
def test_ISDU_getReadableIndexString(index, expected):
    isdu = MyISDU()
    assert isdu._getReadableIndexString(index) == expected
