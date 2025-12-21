from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import MasterMessage, DeviceMessage


def test_octetStreamDecoderMessages_dispatch():
    class MasterMessageHandler:
        def handleMasterMessage(self, message: MasterMessage):
            assert isinstance(message, MasterMessage)
            return True

        def handleDeviceMessage(self, message: DeviceMessage):
            assert isinstance(message, DeviceMessage)
            return False

    mstHandler = MasterMessageHandler()

    assert MasterMessage().dispatch(mstHandler) == True
    assert DeviceMessage().dispatch(mstHandler) == False
