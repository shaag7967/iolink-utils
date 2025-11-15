import pytest

from iolink_utils.utils.cycleTime import CycleTime
from iolink_utils.octetDecoder.octetDecoder import CycleTimeOctet
from iolink_utils.exceptions import InvalidOctetValue, InvalidCycleTime


def test_zeroTimeValue():
    octet = CycleTime.encodeAsCycleTimeOctet(0)
    assert int(octet) == 0
    assert CycleTime.decodeToTimeInMs(octet) == 0.0

def test_allValidTimeValues():
    for value in range(4, 64, 1):
        ms = round(value/10, 1)
        octet = CycleTime.encodeAsCycleTimeOctet(ms)
        assert octet.timeBaseCode == 0
        assert CycleTime.decodeToTimeInMs(octet) == ms

    for value in range(64, 320, 4):
        ms = round(value/10, 1)
        octet = CycleTime.encodeAsCycleTimeOctet(ms)
        assert octet.timeBaseCode == 1
        assert CycleTime.decodeToTimeInMs(octet) == ms

    for value in range(320, 1344, 16):
        ms = round(value/10, 1)
        octet = CycleTime.encodeAsCycleTimeOctet(ms)
        assert octet.timeBaseCode == 2
        assert CycleTime.decodeToTimeInMs(octet) == ms


def test_cycleTime_inbetweenValues():
    octet = CycleTime.encodeAsCycleTimeOctet(6.9) #  6.8 would be ok
    assert CycleTime.decodeToTimeInMs(octet) == 7.2 #  use next larger possible value
    octet = CycleTime.encodeAsCycleTimeOctet(7.2)
    assert CycleTime.decodeToTimeInMs(octet) == 7.2

    octet = CycleTime.encodeAsCycleTimeOctet(33.0) #  nok -> take next larger value
    assert CycleTime.decodeToTimeInMs(octet) == 33.6
    octet = CycleTime.encodeAsCycleTimeOctet(33.6)
    assert CycleTime.decodeToTimeInMs(octet) == 33.6


def test_cycleTime_invalidTime():
    octet = CycleTimeOctet(255)
    assert octet.timeBaseCode == 3 #  3 is not a valid time base code
    with pytest.raises(InvalidOctetValue):
        CycleTime.decodeToTimeInMs(octet)

    with pytest.raises(InvalidCycleTime):
        CycleTime.encodeAsCycleTimeOctet(0.3)
    with pytest.raises(InvalidCycleTime):
        CycleTime.encodeAsCycleTimeOctet(133.0)
    with pytest.raises(InvalidCycleTime):
        CycleTime.encodeAsCycleTimeOctet(-10.0)
