import pytest
from iolink_utils.definitions.onRequestDataOctetCount import ODOctetCount
from iolink_utils.exceptions import InvalidMSeqCode, InvalidMSeqCodePDSizeCombination


# See Table A.8 – M-sequence types for the PREOPERATE mode
def test_ODOctetCount_preoperate():
    assert ODOctetCount.in_preoperate(0) == (1, 'TYPE_0')
    assert ODOctetCount.in_preoperate(1) == (2, 'TYPE_1_2')
    assert ODOctetCount.in_preoperate(2) == (8, 'TYPE_1_V')
    assert ODOctetCount.in_preoperate(3) == (32, 'TYPE_1_V')

    with pytest.raises(InvalidMSeqCode):
        ODOctetCount.in_preoperate(4)


# See Table A.10 – M-sequence types for the OPERATE mode
def test_ODOctetCount_operate():
    assert ODOctetCount.in_operate(0, 0, 0) == (1, 'TYPE_0')
    assert ODOctetCount.in_operate(1, 0, 0) == (2, 'TYPE_1_2')
    assert ODOctetCount.in_operate(6, 0, 0) == (8, 'TYPE_1_V')
    assert ODOctetCount.in_operate(7, 0, 0) == (32, 'TYPE_1_V')

    for pdInSize in range(3, 33):
        for pdOutSize in range(0, 33):
            assert ODOctetCount.in_operate(0, pdInSize, pdOutSize) == (2, 'TYPE_1_1')
    for pdInSize in range(0, 33):
        for pdOutSize in range(3, 33):
            assert ODOctetCount.in_operate(0, pdInSize, pdOutSize) == (2, 'TYPE_1_1')

    assert ODOctetCount.in_operate(0, 1, 0) == (1, 'TYPE_2_1')
    assert ODOctetCount.in_operate(0, 2, 0) == (1, 'TYPE_2_2')
    assert ODOctetCount.in_operate(0, 0, 1) == (1, 'TYPE_2_3')
    assert ODOctetCount.in_operate(0, 0, 2) == (1, 'TYPE_2_4')
    assert ODOctetCount.in_operate(0, 1, 1) == (1, 'TYPE_2_5')
    assert ODOctetCount.in_operate(0, 2, 1) == (1, 'TYPE_2_V')
    assert ODOctetCount.in_operate(0, 1, 2) == (1, 'TYPE_2_V')

    for pdInSize in range(0, 33):
        for pdOutSize in range(3, 33):
            assert ODOctetCount.in_operate(4, pdInSize, pdOutSize) == (1, 'TYPE_2_V')
    for pdInSize in range(3, 33):
        for pdOutSize in range(0, 33):
            assert ODOctetCount.in_operate(4, pdInSize, pdOutSize) == (1, 'TYPE_2_V')

    for pdInSize in range(1, 33):
        for pdOutSize in range(0, 33):
            assert ODOctetCount.in_operate(5, pdInSize, pdOutSize) == (2, 'TYPE_2_V')
    for pdInSize in range(0, 33):
        for pdOutSize in range(1, 33):
            assert ODOctetCount.in_operate(5, pdInSize, pdOutSize) == (2, 'TYPE_2_V')

    for pdInSize in range(1, 33):
        for pdOutSize in range(0, 33):
            assert ODOctetCount.in_operate(6, pdInSize, pdOutSize) == (8, 'TYPE_2_V')
    for pdInSize in range(0, 33):
        for pdOutSize in range(1, 33):
            assert ODOctetCount.in_operate(6, pdInSize, pdOutSize) == (8, 'TYPE_2_V')

    for pdInSize in range(1, 33):
        for pdOutSize in range(0, 33):
            assert ODOctetCount.in_operate(7, pdInSize, pdOutSize) == (32, 'TYPE_2_V')
    for pdInSize in range(0, 33):
        for pdOutSize in range(1, 33):
            assert ODOctetCount.in_operate(7, pdInSize, pdOutSize) == (32, 'TYPE_2_V')


def test_ODOctetCount_operate_error():
    with pytest.raises(InvalidMSeqCodePDSizeCombination):
        ODOctetCount.in_operate(1, 0, 1)

    with pytest.raises(InvalidMSeqCodePDSizeCombination):
        ODOctetCount.in_operate(4, 0, 0)

    with pytest.raises(InvalidMSeqCodePDSizeCombination):
        ODOctetCount.in_operate(4, 1, 1)

    with pytest.raises(InvalidMSeqCodePDSizeCombination):
        ODOctetCount.in_operate(5, 0, 0)
