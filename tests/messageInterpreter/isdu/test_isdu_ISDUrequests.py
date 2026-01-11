import pytest

from iolink_utils.messageInterpreter.isdu.ISDUrequests import (
    createISDURequest,
    ISDURequest_Write8bitIdx,
    ISDURequest_Write8bitIdxSub,
    ISDURequest_Write16bitIdxSub,
    ISDURequest_Read8bitIdx,
    ISDURequest_Read8bitIdxSub,
    ISDURequest_Read16bitIdxSub
)
from iolink_utils.exceptions import InvalidISDUService
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.iServiceNibble import IServiceNibble


def test_ISDURequest_createISDURequest():
    _map_serviceValueToClass = {
        0b0001: ISDURequest_Write8bitIdx,
        0b0010: ISDURequest_Write8bitIdxSub,
        0b0011: ISDURequest_Write16bitIdxSub,
        0b1001: ISDURequest_Read8bitIdx,
        0b1010: ISDURequest_Read8bitIdxSub,
        0b1011: ISDURequest_Read16bitIdxSub
    }
    for serviceValue in _map_serviceValueToClass:
        req = createISDURequest(IService(service=serviceValue))
        assert type(req) is _map_serviceValueToClass[serviceValue]
        assert req.__class__.__name__.endswith(req.name())
        assert req._SERVICE_NIBBLE == IServiceNibble(serviceValue)


def test_ISDURequest_createISDURequest_InvalidISDUService():
    service = IService()
    service.service = IServiceNibble.NoService
    service.length = 4

    with pytest.raises(InvalidISDUService):
        createISDURequest(service)


def test_ISDURequest_Write8bitIdx_ctor():
    req = ISDURequest_Write8bitIdx()
    assert not req.isValid
    assert not req.isComplete
    assert req._service.length == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'
    assert len(d['data']) == 0


def test_ISDURequest_Write8bitIdx():
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdx, length=5)
    req = ISDURequest_Write8bitIdx()
    req.appendOctets(bytearray([int(service), 0x01, 0x02, 0x03, 21]))
    assert req.isComplete
    assert req.index == 1
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '1 / 0x0001'
    assert d['data'] == bytearray([0x02, 0x03])

    # extended length
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdx, length=1)
    req = ISDURequest_Write8bitIdx()
    req.appendOctets(bytearray([int(service), 0x06, 0x01, 0x02, 0x03, 23]))
    assert req.isComplete
    assert req.index == 1
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '1 / 0x0001'
    assert d['data'] == bytearray([0x02, 0x03])

    # invalid crc
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdx, length=1)
    req = ISDURequest_Write8bitIdx()
    req.appendOctets(bytearray([int(service), 0x06, 0x01, 0x02, 0x03, 111]))
    assert req.isComplete
    assert req.index == 1
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '1 / 0x0001'
    assert d['data'] == bytearray([0x02, 0x03])


def test_ISDURequest_Write8bitIdxSub():
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdxSub, length=6)
    req = ISDURequest_Write8bitIdxSub()
    req.appendOctets(bytearray([int(service), 0x01, 0x02, 0x03, 0x04, 34]))
    assert req.isComplete
    assert req.index == 1
    assert req.subIndex == 2
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '1 / 0x0001'
    assert d['subIndex'] == '2'
    assert d['data'] == bytearray([0x03, 0x04])

    # extended length
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdxSub, length=1)
    req = ISDURequest_Write8bitIdxSub()
    req.appendOctets(bytearray([int(service), 0x07, 0x01, 0x02, 0x03, 0x04, 34]))
    assert req.isComplete
    assert req.index == 1
    assert req.subIndex == 2
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '1 / 0x0001'
    assert d['subIndex'] == '2'
    assert d['data'] == bytearray([0x03, 0x04])

    # invalid crc
    service = IService(service=IServiceNibble.M_WriteReq_8bitIdxSub, length=1)
    req = ISDURequest_Write8bitIdxSub()
    req.appendOctets(bytearray([int(service), 0x07, 0x01, 0x02, 0x03, 0x04, 111]))
    assert req.isComplete
    assert req.index == 1
    assert req.subIndex == 2
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '1 / 0x0001'
    assert d['subIndex'] == '2'
    assert d['data'] == bytearray([0x03, 0x04])


def test_ISDURequest_Write16bitIdxSub():
    service = IService(service=IServiceNibble.M_WriteReq_16bitIdxSub, length=9)
    req = ISDURequest_Write16bitIdxSub()
    req.appendOctets(bytearray([int(service), 0xAA, 0xBB, 0xCC, 0x11, 0x22, 0x33, 0x44, 160]))
    assert req.isComplete
    assert req.index == 0xAABB
    assert req.subIndex == 0xCC
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '43707 / 0xAABB'
    assert d['subIndex'] == '204'
    assert d['data'] == bytearray([0x11, 0x22, 0x33, 0x44])

    # extended length
    service = IService(service=IServiceNibble.M_WriteReq_16bitIdxSub, length=1)
    req = ISDURequest_Write16bitIdxSub()
    req.appendOctets(bytearray([int(service), 10, 0xAA, 0xBB, 0xCC, 0x11, 0x22, 0x33, 0x44, 162]))
    assert req.isComplete
    assert req.index == 0xAABB
    assert req.subIndex == 0xCC
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '43707 / 0xAABB'
    assert d['subIndex'] == '204'
    assert d['data'] == bytearray([0x11, 0x22, 0x33, 0x44])

    # invalid crc
    service = IService(service=IServiceNibble.M_WriteReq_16bitIdxSub, length=1)
    req = ISDURequest_Write16bitIdxSub()
    req.appendOctets(bytearray([int(service), 10, 0xAA, 0xBB, 0xCC, 0x11, 0x22, 0x33, 0x44, 111]))
    assert req.isComplete
    assert req.index == 0xAABB
    assert req.subIndex == 0xCC
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '43707 / 0xAABB'
    assert d['subIndex'] == '204'
    assert d['data'] == bytearray([0x11, 0x22, 0x33, 0x44])


def test_ISDURequest_Read8bitIdx():
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdx, length=3)
    req = ISDURequest_Read8bitIdx()
    req.appendOctets(bytearray([int(service), 0xAA, 57]))
    assert req.isComplete
    assert req.index == 0xAA
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '170 / 0x00AA'

    # extended length
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdx, length=1)
    req = ISDURequest_Read8bitIdx()
    req.appendOctets(bytearray([int(service), 4, 0xAA, 63]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length
    assert req.index == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'

    # invalid crc
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdx, length=1)
    req = ISDURequest_Read8bitIdx()
    req.appendOctets(bytearray([int(service), 4, 0xAA, 111]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length and invalid crc
    assert req.index == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'


def test_ISDURequest_Read8bitIdxSub():
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdxSub, length=4)
    req = ISDURequest_Read8bitIdxSub()
    req.appendOctets(bytearray([int(service), 0xAA, 0xBB, 181]))
    assert req.isComplete
    assert req.index == 0xAA
    assert req.subIndex == 0xBB
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '170 / 0x00AA'
    assert d['subIndex'] == '187'

    # extended length
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdxSub, length=1)
    req = ISDURequest_Read8bitIdxSub()
    req.appendOctets(bytearray([int(service), 5, 0xAA, 0xBB, 181]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length
    assert req.index == 0
    assert req.subIndex == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'
    assert d['subIndex'] == '0'

    # invalid crc
    service = IService(service=IServiceNibble.M_ReadReq_8bitIdxSub, length=1)
    req = ISDURequest_Read8bitIdxSub()
    req.appendOctets(bytearray([int(service), 5, 0xAA, 0xBB, 111]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length and invalid crc
    assert req.index == 0
    assert req.subIndex == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'
    assert d['subIndex'] == '0'


def test_ISDURequest_Read16bitIdxSub():
    service = IService(service=IServiceNibble.M_ReadReq_16bitIdxSub, length=5)
    req = ISDURequest_Read16bitIdxSub()
    req.appendOctets(bytearray([int(service), 0xAA, 0xBB, 0xCC, 104]))
    assert req.isComplete
    assert req.index == 0xAABB
    assert req.subIndex == 0xCC
    d = req.data()
    assert d['valid'] == True
    assert d['index'] == '43707 / 0xAABB'
    assert d['subIndex'] == '204'

    # extended length
    service = IService(service=IServiceNibble.M_ReadReq_16bitIdxSub, length=1)
    req = ISDURequest_Read16bitIdxSub()
    req.appendOctets(bytearray([int(service), 6, 0xAA, 0xBB, 0xCC, 106]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length
    assert req.index == 0
    assert req.subIndex == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'
    assert d['subIndex'] == '0'

    # invalid crc
    service = IService(service=IServiceNibble.M_ReadReq_16bitIdxSub, length=1)
    req = ISDURequest_Read16bitIdxSub()
    req.appendOctets(bytearray([int(service), 6, 0xAA, 0xBB, 0xCC, 111]))
    assert req.isComplete
    assert not req.isValid  # reason: extended length and invalid crc
    assert req.index == 0
    assert req.subIndex == 0
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0 / 0x0000'
    assert d['subIndex'] == '0'
