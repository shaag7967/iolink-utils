import pytest
from iolink_utils.definitions._internal import MSeqPDSizeCombination, AutoNameConvertMeta
from enum import IntEnum


def test_internal_MSeqPDSizeCombination():
    combination = MSeqPDSizeCombination(0, 1, 2)
    assert combination.matches(0, 1, 2)
    assert not combination.matches(2, 1, 2)
    assert not combination.matches(0, 2, 2)
    assert not combination.matches(0, 1, 3)

    combination = MSeqPDSizeCombination(0, range(1, 5), 5)
    assert combination.matches(0, 2, 5)
    assert not combination.matches(0, 5, 5)

    combination = MSeqPDSizeCombination(0, 3, range(1, 5))
    assert combination.matches(0, 3, 2)
    assert not combination.matches(0, 3, 5)
    
    combination = MSeqPDSizeCombination(0, range(10, 11), range(0, 10))
    assert combination.matches(0, 10, 5)
    assert combination.matches(0, 10, 0)
    assert not combination.matches(0, 11, 0)
    assert not combination.matches(0, 11, 10)
    assert not combination.matches(0, 10, 20)
    assert not combination.matches(1, 10, 50)

def test_internal_autoNameConvertMeta():
    class MyIntEnum(IntEnum, metaclass=AutoNameConvertMeta):
        Undefined = 0
        EnumEntry1 = 11
        EnumEntry2 = 22
        EnumEntry3 = 333

    myEnum = MyIntEnum(0)
    assert myEnum.name == 'Undefined'
    assert myEnum.value == 0

    myEnum = MyIntEnum('11')
    assert myEnum.name == 'EnumEntry1'
    assert myEnum.value == 11

    myEnum = MyIntEnum('EnumEntry3')
    assert myEnum.name == 'EnumEntry3'
    assert myEnum.value == 333

    with pytest.raises(ValueError):
        MyIntEnum('abc')

    with pytest.raises(ValueError):
        MyIntEnum(4444)
