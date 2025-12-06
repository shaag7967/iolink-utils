import pytest

from iolink_utils.octetDecoder.octetStreamDecoderSettings import MSeqPayloadLength, DecoderSettings
from iolink_utils.definitions.bitRate import BitRate


def test_octetDecoder_settings():
    settings = DecoderSettings()
    assert settings.transmissionRate == BitRate.Undefined
    assert settings.startup == MSeqPayloadLength(0, 0, 0)
    assert settings.preoperate == MSeqPayloadLength(0, 0, 0)
    assert settings.operate == MSeqPayloadLength(0, 0, 0)

    settings.startup = MSeqPayloadLength(1, 2, 3)
    assert settings.getPayloadLength(0).pdOut == 1
    assert settings.getPayloadLength(0).od == 2
    assert settings.getPayloadLength(0).pdIn == 3

    settings.preoperate = MSeqPayloadLength(4, 5, 6)
    assert settings.getPayloadLength(1).pdOut == 4
    assert settings.getPayloadLength(1).od == 5
    assert settings.getPayloadLength(1).pdIn == 6

    settings.operate = MSeqPayloadLength(7, 8, 9)
    assert settings.getPayloadLength(2).pdOut == 7
    assert settings.getPayloadLength(2).od == 8
    assert settings.getPayloadLength(2).pdIn == 9

    with pytest.raises(ValueError):
        settings.getPayloadLength(3)

def test_octetDecoder_settingsFromIodd():
    class PhysicalLayer:
        def __init__(self):
            self.bitrate: BitRate = BitRate.Undefined

    class Iodd:
        def __init__(self):
            self.physical_layer: PhysicalLayer = PhysicalLayer()
            self.size_PDIn = 0
            self.size_PDOut = 0

    iodd = Iodd()
    iodd.physical_layer.bitrate = BitRate.COM2
    iodd.size_PDOut = 2
    iodd.size_OnRequestData = [3, 4]
    iodd.size_PDIn = 5
    settings = DecoderSettings.fromIODD(iodd)

    assert settings.transmissionRate == BitRate.COM2
    assert settings.startup.pdOut == 0
    assert settings.startup.od == 1
    assert settings.startup.pdIn == 0
    assert settings.preoperate.pdOut == 0
    assert settings.preoperate.od == 3
    assert settings.preoperate.pdIn == 0
    assert settings.operate.pdOut == 2
    assert settings.operate.od == 4
    assert settings.operate.pdIn == 5
