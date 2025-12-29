from datetime import datetime as dt

from iolink_utils.messageInterpreter.page.transactionPage import TransactionPage, TransmissionDirection


def test_transactionPage_data():
    tp = TransactionPage(TransmissionDirection.Write, 1, 10)

    tp.setTime(dt(1999, 1, 1), dt(2000, 1, 1))
    assert tp.startTime == dt(1999, 1, 1)
    assert tp.endTime == dt(2000, 1, 1)

    data = tp.data()
    assert data['pageDir'] == "Write"
    assert data['pageIndex'] == "1"
    assert data['pageValue'] == "0x0A"
    assert type(data['pageInfo']) is str  # tests see translateDirectParameter
    assert type(data['pageError']) is str  # tests see translateDirectParameter


def test_transactionPage_dispatch(mocker):
    handler = mocker.Mock()
    tp = TransactionPage(TransmissionDirection.Read, 1, 2)
    tp.dispatch(handler)
    handler.handlePage.assert_called_once_with(tp)
