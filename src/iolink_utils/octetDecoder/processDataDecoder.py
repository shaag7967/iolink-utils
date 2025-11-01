
from ._processDataDecoderInternal import _createPDDecoderClass
import ctypes


class SafetyCodeIn(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("portNum", ctypes.c_uint8),
        ("DCNT", ctypes.c_uint8, 3),
        ("unused", ctypes.c_uint8, 2),
        ("SDset", ctypes.c_uint8, 1),
        ("DCommError", ctypes.c_uint8, 1),
        ("DTimeout", ctypes.c_uint8, 1),
        ("CRC", ctypes.c_uint32)
    ]

class SafetyCodeOut(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("portNum", ctypes.c_uint8),
        ("MCNT", ctypes.c_uint8, 3),
        ("unused", ctypes.c_uint8, 3),
        ("SetSD", ctypes.c_uint8, 1),
        ("ChFAckReq", ctypes.c_uint8, 1),
        ("CRC", ctypes.c_uint32)
    ]

def createDecoderClass_PDIn(json_process_data_def, condition=None):
    return _createPDDecoderClass(json_process_data_def[condition]['pdIn']['dataFormat'], SafetyCodeIn)

def createDecoderClass_PDOut(json_process_data_def, condition=None):
    return _createPDDecoderClass(json_process_data_def[condition]['pdOut']['dataFormat'], SafetyCodeOut)
