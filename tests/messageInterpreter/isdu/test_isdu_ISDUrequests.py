import pytest

from iolink_utils.messageInterpreter.isdu.ISDUrequests import (
    createISDURequest,
    ISDURequest_Write8bitIdx
)
from iolink_utils.exceptions import InvalidISDUService
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.messageInterpreter.isdu.ISDU import IServiceNibble, FlowControl, ISDU


def test_ISDURequest_createISDURequest_InvalidISDUService():
    service = IService()
    service.service = IServiceNibble.NoService
    service.length = 4

    with pytest.raises(InvalidISDUService):
        createISDURequest(service)


def test_ISDURequest_Write8bitIdx():
    service = IService()
    service.service = IServiceNibble.M_WriteReq_8bitIdx
    service.length = 4

    req = createISDURequest(service)
    assert type(req) is ISDURequest_Write8bitIdx
    assert req.name() == 'Write8bitIdx'
    assert not req.isValid
    assert not req.isComplete
    assert req._length == 4
    d = req.data()
    assert d['valid'] == False
    assert d['index'] == '0'
    assert len(d['data']) == 0


def test_ISDURequest_Write8bitIdx_dispatch(mocker):
    handler = mocker.Mock()

    service = IService()
    service.service = IServiceNibble.M_WriteReq_8bitIdx
    service.length = 4

    req = ISDURequest_Write8bitIdx(service)
    req.dispatch(handler)

    handler.handleISDU.assert_called_once_with(req)
