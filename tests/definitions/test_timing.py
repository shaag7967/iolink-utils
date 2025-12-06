import pytest
from iolink_utils.definitions.timing import (getBitTimeInUs, getMaxResponseTime, getMaxMSequenceTime,
                                             getMaxFrameTransmissionDelay_device, getMaxFrameTransmissionDelay_master)
from iolink_utils.definitions.bitRate import BitRate
from iolink_utils.exceptions import InvalidBitRate, InvalidOctetCount


# See Table 9 – Dynamic characteristics of the transmission
def test_timing_getBitTimeInUs():
    assert getBitTimeInUs(BitRate.COM1) == 208.33
    assert getBitTimeInUs(BitRate.COM2) == 26.04
    assert getBitTimeInUs(BitRate.COM3) == 4.34

    with pytest.raises(InvalidBitRate):
        getBitTimeInUs(BitRate.Undefined)


def test_timing_getMaxMSequenceTime():
    assert (pytest.approx(getMaxMSequenceTime(BitRate.COM1, 2, 1), 0.1) ==
            (2+1)*11 * 208.33 + 10 * 208.33 + 1 * 208.33)
    assert (pytest.approx(getMaxMSequenceTime(BitRate.COM3, 3, 2), 0.1) ==
            (3+2)*11 * 4.34 + 10 * 4.34 + 2 * 4.34 + 1 * 4.34)

    with pytest.raises(InvalidOctetCount):
        getMaxMSequenceTime(BitRate.COM2, 1, 1)
    with pytest.raises(InvalidOctetCount):
        getMaxMSequenceTime(BitRate.COM3, 2, 0)


