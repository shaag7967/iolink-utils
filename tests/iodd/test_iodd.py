import pytest
from pathlib import Path
from iolink_utils.iodd.iodd import Iodd
from iolink_utils.utils.version import Version
from iolink_utils.exceptions import IoddFileNotFound, MSequenceCapabilityMissing


def test_iodd_BasicDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'IODDViewer1.4_Examples/IO-Link-01-BasicDevice-20211215-IODD1.1.xml')))

    assert my_iodd.fileInfo.fileExists
    assert my_iodd.fileInfo.sizeInBytes > 0

    assert my_iodd.fileInfo.date.year == 2021
    assert my_iodd.fileInfo.date.month == 12
    assert my_iodd.fileInfo.date.day == 15
    assert my_iodd.fileInfo.date == my_iodd.documentInfo.releaseDate

    assert my_iodd.fileInfo.schemaVersion == Version('1.1')

    assert my_iodd.isSafetyDevice() == False

    assert my_iodd.features.blockParameter
    assert my_iodd.features.dataStorage

    assert len(my_iodd.processDataDefinition.keys()) == 1
    assert None in my_iodd.processDataDefinition.keys()
    assert None in my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDin == 1
    assert len(my_iodd.processDataDefinition[None]['pdIn']['dataFormat']) == 1
    assert my_iodd.processDataDefinition[None]['pdIn']['bitLength'] == 8

    assert my_iodd.size_PDout == 1
    assert len(my_iodd.processDataDefinition[None]['pdOut']['dataFormat']) == 1
    assert my_iodd.processDataDefinition[None]['pdOut']['bitLength'] == 8


def test_iodd_ComplexProcessDataDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'IODDViewer1.4_Examples/IO-Link-17-ComplexProcessDataDevice-20211215-IODD1.1.xml')))

    assert len(my_iodd.processDataDefinition.keys()) == 1
    assert None in my_iodd.processDataDefinition.keys()
    assert None in my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDin == 4
    assert len(my_iodd.processDataDefinition[None]['pdIn']['dataFormat']) == 4
    assert my_iodd.processDataDefinition[None]['pdIn']['bitLength'] == 32

    assert my_iodd.size_PDout == 2
    assert len(my_iodd.processDataDefinition[None]['pdOut']['dataFormat']) == 3
    assert my_iodd.processDataDefinition[None]['pdOut']['bitLength'] == 16


def test_iodd_ConditionalProcessDataDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'IODDViewer1.4_Examples/IO-Link-22-ConditionalProcessDataDevice-20211215-IODD1.1.xml')))

    assert len(my_iodd.processDataDefinition.keys()) == 3
    assert [0, 1, 2] == list(my_iodd.processDataDefinition.keys())
    assert [0, 1, 2] == my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDin == 4
    assert my_iodd.size_PDout == 2

    # condition 0
    assert len(my_iodd.processDataDefinition[0]['pdIn']['dataFormat']) == 2
    assert my_iodd.processDataDefinition[0]['pdIn']['bitLength'] == 32

    assert len(my_iodd.processDataDefinition[0]['pdOut']['dataFormat']) == 1
    assert my_iodd.processDataDefinition[0]['pdOut']['bitLength'] == 16

    # condition 1
    assert len(my_iodd.processDataDefinition[1]['pdIn']['dataFormat']) == 4
    assert my_iodd.processDataDefinition[1]['pdIn']['bitLength'] == 32

    assert len(my_iodd.processDataDefinition[1]['pdOut']['dataFormat']) == 1
    assert my_iodd.processDataDefinition[1]['pdOut']['bitLength'] == 16

    # condition 2
    assert len(my_iodd.processDataDefinition[2]['pdIn']['dataFormat']) == 4
    assert my_iodd.processDataDefinition[2]['pdIn']['bitLength'] == 32

    assert len(my_iodd.processDataDefinition[2]['pdOut']['dataFormat']) == 3
    assert my_iodd.processDataDefinition[2]['pdOut']['bitLength'] == 16


def test_iodd_DeviceVariants():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'IODDViewer1.4_Examples/IO-Link-02-DeviceVariants-20211215-IODD1.1.xml')))

    assert my_iodd.identity.vendorId == 65535
    assert my_iodd.identity.deviceId == 2
    assert my_iodd.identity.vendorName == "IO-Link Community"
    assert len(my_iodd.identity.deviceVariants) == 3


def test_iodd_fileDoesNotExist():
    test_dir = Path(__file__).parent

    with pytest.raises(IoddFileNotFound):
        my_iodd = Iodd(str(test_dir.joinpath(
            'IODDViewer1.4_Examples/nonExistent-20211215-IODD1.1.xml')))


def test_iodd_noPDIn_noPDOut():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'IODDViewer1.4_Examples/IO-Link-01-BasicDevice-20211215-IODD1.1.xml')))

    assert my_iodd.fileInfo.fileExists

    assert len(my_iodd.processDataDefinition.keys()) == 1
    assert None in my_iodd.processDataDefinition.keys()
    assert None in my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)
    assert my_iodd.size_PDin == 1
    assert my_iodd.size_PDout == 1

    del my_iodd.processDataDefinition[None]['pdIn']
    assert my_iodd.size_PDin == 0

    del my_iodd.processDataDefinition[None]['pdOut']
    assert my_iodd.size_PDout == 0

    my_iodd.physicalLayer.m_sequence_capability = None  # like in IODD V1.0.1
    with pytest.raises(MSequenceCapabilityMissing):
        size_OnRequestData = my_iodd.size_OnRequestData
