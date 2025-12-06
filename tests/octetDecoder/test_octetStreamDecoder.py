import pytest
import csv
import os
from datetime import datetime
import logging

from iolink_utils.iodd.iodd import Iodd
from pprint import pprint
from iolink_utils.octetDecoder.octetStreamDecoder import OctetStreamDecoder, DecoderSettings, MasterMessage, DeviceMessage
from iolink_utils.octetDecoder.octetStreamDecoderSettings import MSeqPayloadLength
from iolink_utils.definitions.bitRate import BitRate

from iolink_utils.messageInterpreter.messageInterpreter import MessageInterpreter
from iolink_utils.messageInterpreter.commChannelPage import TransactionPage
from iolink_utils.messageInterpreter.commChannelDiagnosis import TransactionDiagEventMemory, TransactionDiagEventReset



def getTestData(filename: str):
    rows = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            value_str, error, start_str, end_str, type_str = [col.strip() for col in row]

            value = int(value_str)
            error = error if error else None
            start = datetime.fromisoformat(start_str)
            end = datetime.fromisoformat(end_str)

            rows.append({
                "value": value,
                "error": error,
                "start": start,
                "end": end,
                "type": type_str,
            })

    return rows


def test_octetStreamDecoder():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    decoder = OctetStreamDecoder(settings)
    interpreter = MessageInterpreter()

    # test_data = getTestData(os.path.join(os.path.dirname(__file__), 'serialdata_short.csv'))
    # test_data = getTestData(os.path.join(os.path.dirname(__file__), 'serialdata_preoperate.csv'))
    test_data = getTestData(os.path.join(os.path.dirname(__file__), 'serialdata_pre_operate.csv'))
    # test_data = getTestData(os.path.join(os.path.dirname(__file__), 'tmg_safetyCommunication.csv'))

    line = 0
    for data in test_data:
        line += 1
        if data['error'] is not None:
            continue

        message = decoder.processOctet(data['value'], data['start'], data['end'])

        commChannelMessages = interpreter.processMessage(message)
        for msg in commChannelMessages:
            assert msg.start_time < msg.end_time

            if isinstance(msg, TransactionPage):
                print(msg)
            elif isinstance(msg, TransactionDiagEventMemory):
                print(msg)
            elif isinstance(msg, TransactionDiagEventReset):
                print(msg)
