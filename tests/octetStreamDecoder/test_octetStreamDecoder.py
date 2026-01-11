from iolink_utils.octetStreamDecoder.octetStreamDecoder import OctetStreamDecoder, DecoderSettings, DecodingState
from iolink_utils.octetStreamDecoder.octetStreamDecoderSettings import MSeqPayloadLength
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import Message, MasterMessage, DeviceMessage
from iolink_utils.definitions.bitRate import BitRate
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.definitions.communicationChannel import CommChannel
from iolink_utils.definitions.mSequenceType import MSeqType
from iolink_utils.definitions.masterCommand import MasterCommand

from .testDataHelper import convertToTestDataList


def test_octetStreamDecoder_ctor():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    decoder = OctetStreamDecoder(settings)
    assert decoder.settings is not settings

    settings.transmissionRate = BitRate.COM3  # change source
    assert decoder.settings.transmissionRate == BitRate.COM2  # -> decoder has a copy
    assert decoder.settings != settings  # we changed transmissionRate

    assert decoder._state == DecodingState.Idle


def test_octetStreamDecoder_setSettings():
    initialSettings = DecoderSettings(
        transmissionRate=BitRate("COM3"),
        startup=MSeqPayloadLength(pdOut=1),
    )
    decoder = OctetStreamDecoder(initialSettings)

    settings = DecoderSettings(
        transmissionRate=BitRate("COM1"),
        startup=MSeqPayloadLength(pdOut=5),
    )

    decoder.setSettings(settings)
    assert decoder.settings is not settings  # we make a copy in setSettings
    assert decoder.settings.startup is not settings.startup
    assert decoder.settings != initialSettings
    assert decoder.settings == settings

    settings.startup = MSeqPayloadLength(pdOut=123)
    assert decoder.settings.startup.pdOut == 5  # nothing changed (copy)


def test_octetStreamDecoder_MSequence_startup():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    testData = convertToTestDataList(
        """
        162, , 2050-01-01 00:01:02.128865+00:00, 2050-01-01 00:01:02.129138+00:00, data
        0, , 2050-01-01 00:01:02.129152+00:00, 2050-01-01 00:01:02.129425+00:00, data
        73, , 2050-01-01 00:01:02.129520+00:00, 2050-01-01 00:01:02.129793+00:00, data
        6, , 2050-01-01 00:01:02.129806+00:00, 2050-01-01 00:01:02.130080+00:00, data
        """)

    decoder = OctetStreamDecoder(settings)
    assert decoder._state == DecodingState.Idle

    num = 0
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert issubclass(type(message), Message)
    assert isinstance(message, MasterMessage)
    assert decoder._state == DecodingState.DeviceResponseDelay

    assert TransmissionDirection(message.mc.read) == TransmissionDirection.Read
    assert CommChannel(message.mc.channel) == CommChannel.Page
    assert message.channel() == CommChannel.Page
    assert MSeqType(message.ckt.mSeqType) == MSeqType.Type_0_STARTUP
    assert message.isValid

    assert len(message.pdOut) == 0
    assert len(message.od) == 0

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.DeviceMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert issubclass(type(message), Message)
    assert isinstance(message, DeviceMessage)
    assert decoder._state == DecodingState.Idle

    assert message.channel() is None  # DeviceMessage has no channel info (only MasterMessage has it)
    assert message.isValid

    assert len(message.pdIn) == 0
    assert len(message.od) == 1
    assert message.od[0] == 73


def test_octetStreamDecoder_reset():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    testData = convertToTestDataList(
        """
        162, , 2050-01-01 00:01:02.128865+00:00, 2050-01-01 00:01:02.129138+00:00, data
        0, , 2050-01-01 00:01:02.129152+00:00, 2050-01-01 00:01:02.129425+00:00, data
        73, , 2050-01-01 00:01:02.129520+00:00, 2050-01-01 00:01:02.129793+00:00, data
        6, , 2050-01-01 00:01:02.129806+00:00, 2050-01-01 00:01:02.130080+00:00, data
        """)

    decoder = OctetStreamDecoder(settings)
    assert decoder._state == DecodingState.Idle

    num = 0
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage
    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, MasterMessage)
    assert decoder._state == DecodingState.DeviceResponseDelay

    decoder.reset()
    assert decoder._state == DecodingState.Idle

    num = 0
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage


def test_octetStreamDecoder_MSequence_startupToPreoperate():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    testData = convertToTestDataList(
        """
        32, , 2050-01-01 00:01:02.166137+00:00, 2050-01-01 00:01:02.166410+00:00, data
        54, , 2050-01-01 00:01:02.166424+00:00, 2050-01-01 00:01:02.166698+00:00, data
        154, , 2050-01-01 00:01:02.166711+00:00, 2050-01-01 00:01:02.166985+00:00, data
        45, , 2050-01-01 00:01:02.167081+00:00, 2050-01-01 00:01:02.167354+00:00, data
        241, , 2050-01-01 00:01:02.169004+00:00, 2050-01-01 00:01:02.169278+00:00, data
        100, , 2050-01-01 00:01:02.169291+00:00, 2050-01-01 00:01:02.169564+00:00, data
        0, , 2050-01-01 00:01:02.169667+00:00, 2050-01-01 00:01:02.169941+00:00, data
        0, , 2050-01-01 00:01:02.169954+00:00, 2050-01-01 00:01:02.170228+00:00, data
        0, , 2050-01-01 00:01:02.170240+00:00, 2050-01-01 00:01:02.170514+00:00, data
        0, , 2050-01-01 00:01:02.170527+00:00, 2050-01-01 00:01:02.170800+00:00, data
        0, , 2050-01-01 00:01:02.170814+00:00, 2050-01-01 00:01:02.171087+00:00, data
        0, , 2050-01-01 00:01:02.171100+00:00, 2050-01-01 00:01:02.171373+00:00, data
        0, , 2050-01-01 00:01:02.171386+00:00, 2050-01-01 00:01:02.171660+00:00, data
        0, , 2050-01-01 00:01:02.171673+00:00, 2050-01-01 00:01:02.171946+00:00, data
        133, , 2050-01-01 00:01:02.171959+00:00, 2050-01-01 00:01:02.172233+00:00, data
        """)

    decoder = OctetStreamDecoder(settings)
    assert decoder._state == DecodingState.Idle

    num = 0
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num = 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num = 2
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, MasterMessage)
    assert decoder._state == DecodingState.DeviceResponseDelay

    assert TransmissionDirection(message.mc.read) == TransmissionDirection.Write
    assert CommChannel(message.mc.channel) == CommChannel.Page
    assert MSeqType(message.ckt.mSeqType) == MSeqType.Type_0_STARTUP
    assert message.isValid

    assert len(message.pdOut) == 0
    assert len(message.od) == 1
    assert message.od[0] == MasterCommand.DevicePreoperate.value

    num = 3
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, DeviceMessage)
    assert decoder._state == DecodingState.Idle
    assert message.isValid

    # now we are in preoperate

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, MasterMessage)
    assert decoder._state == DecodingState.DeviceResponseDelay
    assert TransmissionDirection(message.mc.read) == TransmissionDirection.Read
    assert CommChannel(message.mc.channel) == CommChannel.ISDU
    assert MSeqType(message.ckt.mSeqType) == MSeqType.Type_1_PREOPERATE
    assert message.isValid

    assert len(message.pdOut) == 0
    assert len(message.od) == 0

    for i in range(decoder._settings.preoperate.od):
        num += 1
        message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
        assert message is None
        assert decoder._state == DecodingState.DeviceMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, DeviceMessage)
    assert message.cks.eventFlag == 1
    assert decoder._state == DecodingState.Idle

    assert len(message.pdIn) == 0
    assert len(message.od) == decoder._settings.preoperate.od


def test_octetStreamDecoder_MSequence_operate():
    settings: DecoderSettings = DecoderSettings()
    settings.transmissionRate = BitRate.COM2
    settings.startup = MSeqPayloadLength(pdOut=0, od=1, pdIn=0)
    settings.preoperate = MSeqPayloadLength(pdOut=0, od=8, pdIn=0)
    settings.operate = MSeqPayloadLength(pdOut=7, od=2, pdIn=10)

    testData = convertToTestDataList(
        """
        32, , 2050-01-01 00:01:02.532318+00:00, 2050-01-01 00:01:02.532592+00:00, data
        191, , 2050-01-01 00:01:02.532605+00:00, 2050-01-01 00:01:02.532878+00:00, data
        0, , 2050-01-01 00:01:02.532891+00:00, 2050-01-01 00:01:02.533165+00:00, data
        0, , 2050-01-01 00:01:02.533178+00:00, 2050-01-01 00:01:02.533451+00:00, data
        0, , 2050-01-01 00:01:02.533464+00:00, 2050-01-01 00:01:02.533738+00:00, data
        0, , 2050-01-01 00:01:02.533751+00:00, 2050-01-01 00:01:02.534024+00:00, data
        0, , 2050-01-01 00:01:02.534037+00:00, 2050-01-01 00:01:02.534310+00:00, data
        0, , 2050-01-01 00:01:02.534323+00:00, 2050-01-01 00:01:02.534597+00:00, data
        0, , 2050-01-01 00:01:02.534610+00:00, 2050-01-01 00:01:02.534883+00:00, data
        152, , 2050-01-01 00:01:02.534896+00:00, 2050-01-01 00:01:02.535170+00:00, data
        0, , 2050-01-01 00:01:02.535183+00:00, 2050-01-01 00:01:02.535456+00:00, data
        0, , 2050-01-01 00:01:02.535586+00:00, 2050-01-01 00:01:02.535859+00:00, data
        0, , 2050-01-01 00:01:02.535872+00:00, 2050-01-01 00:01:02.536146+00:00, data
        0, , 2050-01-01 00:01:02.536159+00:00, 2050-01-01 00:01:02.536432+00:00, data
        0, , 2050-01-01 00:01:02.536445+00:00, 2050-01-01 00:01:02.536719+00:00, data
        0, , 2050-01-01 00:01:02.536732+00:00, 2050-01-01 00:01:02.537005+00:00, data
        0, , 2050-01-01 00:01:02.537018+00:00, 2050-01-01 00:01:02.537292+00:00, data
        0, , 2050-01-01 00:01:02.537305+00:00, 2050-01-01 00:01:02.537578+00:00, data
        0, , 2050-01-01 00:01:02.537591+00:00, 2050-01-01 00:01:02.537864+00:00, data
        0, , 2050-01-01 00:01:02.537878+00:00, 2050-01-01 00:01:02.538151+00:00, data
        0, , 2050-01-01 00:01:02.538164+00:00, 2050-01-01 00:01:02.538438+00:00, data
        45, , 2050-01-01 00:01:02.538451+00:00, 2050-01-01 00:01:02.538724+00:00, data
        """)

    decoder = OctetStreamDecoder(settings)
    assert decoder._state == DecodingState.Idle

    # MASTER message
    num = 0
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    # pd out
    for i in range(decoder._settings.operate.pdOut):
        num += 1
        message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
        assert message is None
        assert decoder._state == DecodingState.MasterMessage

    # od
    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert message is None
    assert decoder._state == DecodingState.MasterMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, MasterMessage)
    assert decoder._state == DecodingState.DeviceResponseDelay

    assert TransmissionDirection(message.mc.read) == TransmissionDirection.Write
    assert MSeqType(message.ckt.mSeqType) == MSeqType.Type_2_OPERATE

    assert len(message.pdOut) == decoder._settings.operate.pdOut
    assert len(message.od) == decoder._settings.operate.od

    # DEVICE message
    for i in range(decoder._settings.operate.pdIn):
        num += 1
        message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
        assert message is None
        assert decoder._state == DecodingState.DeviceMessage

    num += 1
    message = decoder.processOctet(testData[num]['value'], testData[num]['start'], testData[num]['end'])
    assert isinstance(message, DeviceMessage)
    assert decoder._state == DecodingState.Idle

    assert len(message.pdIn) == decoder._settings.operate.pdIn
    assert len(message.od) == 0 # when writing
