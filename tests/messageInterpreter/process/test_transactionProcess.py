from datetime import datetime as dt

from iolink_utils.messageInterpreter.process.transactionProcess import TransactionProcess, TransmissionDirection


def test_transactionProcess_data():
    tp = TransactionProcess("source", TransmissionDirection.Write)

    tp.setTime(dt(1999, 1, 1), dt(2000, 1, 1))
    assert tp.startTime == dt(1999, 1, 1)
    assert tp.endTime == dt(2000, 1, 1)

    data = tp.data()
    assert data['processDir'] == TransmissionDirection.Write
    assert data['processSource'] == "source"


def test_transactionPage_dispatch(mocker):
    handler = mocker.Mock()
    tp = TransactionProcess("abc", TransmissionDirection.Read)
    tp.dispatch(handler)
    handler.handleProcess.assert_called_once_with(tp)
