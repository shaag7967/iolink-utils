import pytest
from datetime import datetime as dt
from typing import List

from iolink_utils.messageInterpreter.isdu.commChannelISDU import CommChannelISDU
from iolink_utils.octetStreamDecoder.octetStreamDecoderMessages import MasterMessage, DeviceMessage
from iolink_utils.octetDecoder.octetDecoder import MC, CKT, CKS


def test_commChannelDiagnosis_reset():
    channel = CommChannelISDU()

    channel._state = CommChannelISDU.State.Response
    channel.reset()

    assert channel._state == CommChannelISDU.State.Idle


def createMasterMessage(mc: int, ckt: int, pdOutSize: int, od: List[int]):
    masterMsg = MasterMessage()
    masterMsg.mc = MC(mc)
    masterMsg.ckt = CKT(ckt)
    masterMsg.pdOut = bytearray(pdOutSize)
    masterMsg.od = bytearray(od)
    masterMsg.isValid = True
    return masterMsg


def createDeviceMessage(od: List[int], pdInSize: int, cks: int):
    deviceMsg = DeviceMessage()
    deviceMsg.od = bytearray(od)
    deviceMsg.pdIn = bytearray(pdInSize)
    deviceMsg.cks = CKS(cks)
    deviceMsg.isValid = True
    return deviceMsg


def test_commChannelDiagnosis_read():
    messages = [
        (createMasterMessage(0x70, 0x83, 7, [0xA4, 0x03]), createDeviceMessage([], 10, 0x2D)),
        (createMasterMessage(0x61, 0x86, 7, [0x01, 0xA6]), createDeviceMessage([], 10, 0x2D)),
        (createMasterMessage(0xF0, 0x85, 7, []), createDeviceMessage([0xD3, 0x00], 10, 0x39)),
        (createMasterMessage(0xE1, 0x80, 7, []), createDeviceMessage([0xD3, 0x00], 10, 0x39))
    ]

    channel = CommChannelISDU()

    channel.handleMasterMessage(messages[0][0])
    transaction = channel.handleDeviceMessage(messages[0][1])
    print(transaction)

    channel.handleMasterMessage(messages[1][0])
    transaction = channel.handleDeviceMessage(messages[1][1])
    print(transaction)

    channel.handleMasterMessage(messages[2][0])
    transaction = channel.handleDeviceMessage(messages[2][1])
    print(transaction)

    channel.handleMasterMessage(messages[3][0])
    transaction = channel.handleDeviceMessage(messages[3][1])
    print(transaction)
