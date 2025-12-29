import pytest

from iolink_utils.messageInterpreter.isdu.ISDUerrors import IsduError


def test_isduError():
    e = IsduError((0x80, 0x00))
    assert e == IsduError.APP_DEV


def test_isduError_vendorSpecific():
    e = IsduError((0x81, 0x01))
    assert e == IsduError.VENDOR_SPECIFIC
    e = IsduError.fromCodes(0x81, 0x11)
    assert e == IsduError.VENDOR_SPECIFIC
    e = IsduError.fromCodes(0x81, 0xFF)
    assert e == IsduError.VENDOR_SPECIFIC


def test_isduError_unknown():
    with pytest.raises(ValueError):
        IsduError((0x88, 0x01))
