import pytest
import csv
import os
import re
from datetime import datetime, timezone
import logging

from iolink_utils.iodd.iodd import Iodd
from pprint import pprint
from iolink_utils.octetDecoder.octetStreamDecoder import OctetStreamDecoder, DecoderSettings, MSeqPayloadLength, MasterMessage, DeviceMessage, BitRate


_iso_z_re = re.compile(r'^(?P<date>\d{4}-\d{2}-\d{2})T'
                      r'(?P<time>\d{2}:\d{2}:\d{2})'
                      r'(?:\.(?P<frac>\d+))?Z$')

def parse_iso8601_z(s, keep_frac_as_int=False):
    s = s.strip()
    m = _iso_z_re.match(s)
    if not m:
        raise ValueError(f"Invalid Format: {s!r}")
    date = m.group('date')
    time = m.group('time')
    frac = m.group('frac') or '0'

    micros = (frac + '000000')[:6]
    dt_for_strptime = f"{date}T{time}.{micros}Z"
    dt = datetime.strptime(dt_for_strptime, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)

    if keep_frac_as_int:
        return dt, int(frac)
    return dt

def getTestData(filename: str):
    rows = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            value_str, error, start_str, end_str, type_str = [col.strip() for col in row]

            value = int(value_str)
            error = error if error else None
            start = parse_iso8601_z(start_str)
            end = parse_iso8601_z(end_str)

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

    # test_data = getTestData(os.path.join(os.path.dirname(__file__), 'serialdata_short.csv'))
    test_data = getTestData(os.path.join(os.path.dirname(__file__), 'serialdata_pre_operate.csv'))
    for data in test_data:
        if data['error'] is not None:
            continue

        message = decoder.processOctet(data['value'], data['start'], data['end'])
        if isinstance(message, MasterMessage):
            print(message)
        elif isinstance(message, DeviceMessage):
            print(message)

