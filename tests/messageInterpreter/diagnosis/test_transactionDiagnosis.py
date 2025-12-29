from datetime import datetime as dt

from iolink_utils.octetDecoder.octetDecoder import StatusCodeType2, EventQualifier
from iolink_utils.definitions.eventInfo import EventType, EventMode, EventSource, EventInstance
from iolink_utils.definitions.eventMemory import EventMemory
from iolink_utils.messageInterpreter.diagnosis.transactionDiagnosis import (
    TransactionDiagEventMemory,
    TransactionDiagEventReset
)


def test_transactionDiagnosis_eventMemory():
    memory = EventMemory()
    transaction = TransactionDiagEventMemory(dt(1999, 1, 1), dt(2000, 1, 1), memory)

    assert transaction.eventMemory is not memory
    assert transaction.eventMemory == memory

    assert transaction.startTime == dt(1999, 1, 1)
    assert transaction.endTime == dt(2000, 1, 1)

    # set event 3
    statusCode = StatusCodeType2()
    statusCode.details = 1
    statusCode.evt3 = 1
    transaction.eventMemory.setMemory(0, int(statusCode))

    qualifier = EventQualifier()
    qualifier.mode = EventMode.SingleShot.value
    qualifier.type = EventType.Notification.value
    qualifier.source = EventSource.Device.value
    qualifier.instance = EventInstance.Application.value

    transaction.eventMemory.setMemory(7, int(qualifier))
    transaction.eventMemory.setMemory(8, 0xFF)
    transaction.eventMemory.setMemory(9, 0x91)

    data = transaction.data()
    assert data['eventStatus'] == "details=1, evt6=0, evt5=0, evt4=0, evt3=1, evt2=0, evt1=0"
    assert data['events'] == "NotificationSingleShot(0xFF91)"


def test_transactionDiagnosis_reset():
    transaction = TransactionDiagEventReset(dt(1999, 1, 1), dt(2000, 1, 1))

    assert transaction.startTime == dt(1999, 1, 1)
    assert transaction.endTime == dt(2000, 1, 1)

    data = transaction.data()
    assert len(data) == 0


def test_transactionPage_EventMemory_dispatch(mocker):
    handler = mocker.Mock()

    transaction = TransactionDiagEventMemory(dt(1999, 1, 1), dt(2000, 1, 1), EventMemory())
    transaction.dispatch(handler)

    handler.handleDiagEventMemory.assert_called_once_with(transaction)


def test_transactionPage_EventReset_dispatch(mocker):
    handler = mocker.Mock()

    transaction = TransactionDiagEventReset(dt(1999, 1, 1), dt(2000, 1, 1))
    transaction.dispatch(handler)

    handler.handleDiagEventReset.assert_called_once_with(transaction)
