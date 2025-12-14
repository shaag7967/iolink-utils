from pathlib import Path
from datetime import date

from iolink_utils.iodd.iodd import IoddFileInfo
from iolink_utils.utils.version import Version


def test_iodd_IoddFileInfo():
    test_dir = Path(__file__).parent
    info = IoddFileInfo(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-01-BasicDevice-20211215-IODD1.1.xml')))

    assert info.fileExists
    assert info.filename == 'IO-Link-01-BasicDevice-20211215-IODD1.1.xml'
    assert info.sizeInBytes > 10000
    assert info.schemaVersion == Version('1.1')
    assert info.dirPath.endswith('IODDViewer1.4_Examples')
    assert info.date == date(2021, 12, 15)


def test_iodd_IoddFileInfo_noExist():
    info = IoddFileInfo('IO-Link-01-BasicDevice-20211215-IODD1.1.xml')

    assert info.fileExists is False
    assert info.filename == 'IO-Link-01-BasicDevice-20211215-IODD1.1.xml'
    assert info.sizeInBytes == 0
    assert info.schemaVersion == Version('1.1')
    assert info.dirPath == '.'
    assert info.date == date(2021, 12, 15)


def test_iodd_IoddFileInfo_invalidFilename():
    info = IoddFileInfo('abc-bca-111-aaaa.xml')

    assert info.fileExists is False
    assert info.filename == 'abc-bca-111-aaaa.xml'
    assert info.sizeInBytes == 0
    assert info.schemaVersion == Version('0.0')
    assert info.dirPath == '.'
    assert info.date is None
