import pytest
from pathlib import Path
from pprint import pprint
from iolink_utils.iodd.iodd import Iodd


def test_iodd_BasicDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-01-BasicDevice-20211215-IODD1.1.xml')))

    assert my_iodd.filename.date.year == 2021
    assert my_iodd.filename.date.month == 12
    assert my_iodd.filename.date.day == 15
    assert my_iodd.filename.date == my_iodd.document_info.releaseDate

    assert len(my_iodd.process_data_definition.keys()) == 1
    assert None in my_iodd.process_data_definition.keys()
    assert None in my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDIn == 1
    assert len(my_iodd.process_data_definition[None]['pdIn']['dataFormat']) == 1
    assert my_iodd.process_data_definition[None]['pdIn']['bitLength'] == 8

    assert my_iodd.size_PDOut == 1
    assert len(my_iodd.process_data_definition[None]['pdOut']['dataFormat']) == 1
    assert my_iodd.process_data_definition[None]['pdOut']['bitLength'] == 8

def test_iodd_ComplexProcessDataDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-17-ComplexProcessDataDevice-20211215-IODD1.1.xml')))

    assert len(my_iodd.process_data_definition.keys()) == 1
    assert None in my_iodd.process_data_definition.keys()
    assert None in my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDIn == 4
    assert len(my_iodd.process_data_definition[None]['pdIn']['dataFormat']) == 4
    assert my_iodd.process_data_definition[None]['pdIn']['bitLength'] == 32

    assert my_iodd.size_PDOut == 2
    assert len(my_iodd.process_data_definition[None]['pdOut']['dataFormat']) == 3
    assert my_iodd.process_data_definition[None]['pdOut']['bitLength'] == 16

def test_iodd_ConditionalProcessDataDevice():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-22-ConditionalProcessDataDevice-20211215-IODD1.1.xml')))

    assert len(my_iodd.process_data_definition.keys()) == 3
    assert [0, 1, 2] == list(my_iodd.process_data_definition.keys())
    assert [0, 1, 2] == my_iodd.processDataConditionValues

    assert my_iodd.size_OnRequestData == (2, 2)

    assert my_iodd.size_PDIn == 4
    assert my_iodd.size_PDOut == 2

    # condition 0
    assert len(my_iodd.process_data_definition[0]['pdIn']['dataFormat']) == 2
    assert my_iodd.process_data_definition[0]['pdIn']['bitLength'] == 32

    assert len(my_iodd.process_data_definition[0]['pdOut']['dataFormat']) == 1
    assert my_iodd.process_data_definition[0]['pdOut']['bitLength'] == 16

    # condition 1
    assert len(my_iodd.process_data_definition[1]['pdIn']['dataFormat']) == 4
    assert my_iodd.process_data_definition[1]['pdIn']['bitLength'] == 32

    assert len(my_iodd.process_data_definition[1]['pdOut']['dataFormat']) == 1
    assert my_iodd.process_data_definition[1]['pdOut']['bitLength'] == 16

    # condition 2
    assert len(my_iodd.process_data_definition[2]['pdIn']['dataFormat']) == 4
    assert my_iodd.process_data_definition[2]['pdIn']['bitLength'] == 32

    assert len(my_iodd.process_data_definition[2]['pdOut']['dataFormat']) == 3
    assert my_iodd.process_data_definition[2]['pdOut']['bitLength'] == 16

def test_iodd_DeviceVariants():
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-02-DeviceVariants-20211215-IODD1.1.xml')))

    assert my_iodd.identity.vendorId == 65535
    assert my_iodd.identity.deviceId == 2
    assert my_iodd.identity.vendorName == "IO-Link Community"
    assert len(my_iodd.identity.deviceVariants) == 3
