import pytest
from iolink_utils.octetDecoder.octetDecoder import MinCycleTimeOctet, MasterCycleTimeOctet
from iolink_utils.exceptions import InvalidOctetValue, InvalidCycleTime


def test_minCycleTime():
    cycleTime = MinCycleTimeOctet()
    assert cycleTime.getTimeInMs() == 0.0

    for value in range(4, 64, 1):
        ms = round(value/10, 1)
        cycleTime.setTimeInMs(ms)
        assert cycleTime.getTimeInMs() == ms
        assert cycleTime.timeBaseCode == 0

    for value in range(64, 320, 4):
        ms = round(value/10, 1)
        cycleTime.setTimeInMs(ms)
        assert cycleTime.getTimeInMs() == ms
        assert cycleTime.timeBaseCode == 1

    for value in range(320, 1344, 16):
        ms = round(value/10, 1)
        cycleTime.setTimeInMs(ms)
        assert cycleTime.getTimeInMs() == ms
        assert cycleTime.timeBaseCode == 2

    cycleTime.setTimeInMs(0.0)
    assert cycleTime.timeBaseCode == 0
    assert cycleTime.multiplier == 0
    assert cycleTime.getTimeInMs() == 0.0

    cycleTime.setTimeInMs(10)
    assert cycleTime.timeBaseCode == 1
    assert cycleTime.multiplier == 9
    assert cycleTime.getTimeInMs() == 10.0

    cycleTime.setTimeInMs(132.8)
    assert cycleTime.getTimeInMs() == 132.8


def test_cycleTime_inbetweenValues():
    cycleTime = MasterCycleTimeOctet()

    cycleTime.setTimeInMs(6.9) #  6.8 would be ok
    assert cycleTime.getTimeInMs() == 7.2 #  use next larger possible value
    cycleTime.setTimeInMs(7.2)
    assert cycleTime.getTimeInMs() == 7.2

    cycleTime.setTimeInMs(33.0) #  nok -> take next larger value
    assert cycleTime.getTimeInMs() == 33.6
    cycleTime.setTimeInMs(33.6)
    assert cycleTime.getTimeInMs() == 33.6


def test_cycleTime_invalidTime():
    with pytest.raises(InvalidOctetValue):
        cycleTime = MasterCycleTimeOctet(10000)  #  invalid octet value

    cycleTime = MinCycleTimeOctet(255)  #  invalid octet value
    with pytest.raises(InvalidOctetValue):
        cycleTime.getTimeInMs() #  3 is not a valid time base code

    cycleTime = MasterCycleTimeOctet()
    with pytest.raises(InvalidCycleTime):
        cycleTime.setTimeInMs(0.3)
    with pytest.raises(InvalidCycleTime):
        cycleTime.setTimeInMs(133.0)
    with pytest.raises(InvalidCycleTime):
        cycleTime.setTimeInMs(-10.0)
