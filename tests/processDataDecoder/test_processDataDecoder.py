import pytest
from pathlib import Path
from iolink_utils.iodd.iodd import Iodd
from iolink_utils.processDataDecoder.processDataDecoder import createDecoderClass_PDIn, createDecoderClass_PDOut


def test_ConditionalProcessDataDevice():
    """
    {0: {'id': 'P_ProcessData0',
     'pdIn': {'bitLength': 32,
              'dataFormat': [{'bitOffset': 16,
                              'data': {'bitLength': 16, 'type': <class 'int'>},
                              'name': ('TN_PI_X_PDin_DetectionValue',
                                       'Detection Value')},
                             {'bitOffset': 8,
                              'data': {'bitLength': 8, 'type': <class 'int'>},
                              'name': ('TN_PI_X_PDin_TemperatureValue',
                                       'Temperature Value')}],
              'id': 'PI_PDin0',
              'name': ('TN_PI_PDin0', 'PD Input - Std')},
     'pdOut': {'bitLength': 16,
               'dataFormat': [{'bitOffset': 8,
                               'data': {'bitLength': 8, 'type': <class 'int'>},
                               'name': ('TN_PO_X_PDout_ControlValue',
                                        'Control Value')}],
               'id': 'PO_PDout0',
               'name': ('TN_PO_PDout0', 'PD Output - Std')}},
 1: {'id': 'P_ProcessData1',
     'pdIn': {'bitLength': 32,
              'dataFormat': [{'bitOffset': 16,
                              'data': {'bitLength': 16, 'type': <class 'int'>},
                              'name': ('TN_PI_X_PDin_DetectionValue',
                                       'Detection Value')},
                             {'bitOffset': 8,
                              'data': {'bitLength': 8, 'type': <class 'int'>},
                              'name': ('TN_PI_X_PDin_TemperatureValue',
                                       'Temperature Value')},
                             {'bitOffset': 0,
                              'data': {'bitLength': 1, 'type': <class 'bool'>},
                              'name': ('TN_PI_X_PDin_StatusSig1',
                                       'Status Signal 1')},
                             {'bitOffset': 1,
                              'data': {'bitLength': 1, 'type': <class 'bool'>},
                              'name': ('TN_PI_X_PDin_StatusSig2',
                                       'Status Signal 2')}],
              'id': 'PI_PDin1',
              'name': ('TN_PI_PDin1', 'PD Input - Set1')},
     'pdOut': {'bitLength': 16,
               'dataFormat': [{'bitOffset': 8,
                               'data': {'bitLength': 8, 'type': <class 'int'>},
                               'name': ('TN_PO_X_PDout_ControlValue',
                                        'Control Value')}],
               'id': 'PO_PDout1',
               'name': ('TN_PO_PDout1', 'PD Output - Set 1')}},
 2: {'id': 'P_ProcessData2',
     'pdIn': {'bitLength': 32,
              'dataFormat': [{'bitOffset': 16,
                              'data': {'bitLength': 16, 'type': <class 'int'>},
                              'name': ('TN_PI_X_PDin_DetectionValue',
                                       'Detection Value')},
                             {'bitOffset': 8,
                              'data': {'bitLength': 8, 'type': <class 'int'>},
                              'name': ('TN_V_PD_CounterValue',
                                       'Counter Value')},
                             {'bitOffset': 0,
                              'data': {'bitLength': 1, 'type': <class 'bool'>},
                              'name': ('TN_PI_X_PDin_StatusSig1',
                                       'Status Signal 1')},
                             {'bitOffset': 1,
                              'data': {'bitLength': 1, 'type': <class 'bool'>},
                              'name': ('TN_PI_X_PDin_StatusSig2',
                                       'Status Signal 2')}],
              'id': 'PI_PDin2',
              'name': ('TN_PI_PDin2', 'PD Input - Set 2')},
     'pdOut': {'bitLength': 16,
               'dataFormat': [{'bitOffset': 8,
                               'data': {'bitLength': 8, 'type': <class 'int'>},
                               'name': ('TN_PO_X_PDout_ControlValue',
                                        'Control Value')},
                              {'bitOffset': 0,
                               'data': {'bitLength': 1, 'type': <class 'bool'>},
                               'name': ('TN_PO_X_PDout_ControlFunction',
                                        'Control Function')},
                              {'bitOffset': 1,
                               'data': {'bitLength': 1, 'type': <class 'bool'>},
                               'name': ('TN_PO_X_PDout_ControlSig',
                                        'Control Signal')}],
               'id': 'PO_PDout2',
               'name': ('TN_PO_PDout2', 'PD Output - Set 2')}}}
    """
    test_dir = Path(__file__).parent.parent
    my_iodd = Iodd(str(test_dir.joinpath(
        'iodd/IODDViewer1.4_Examples/IO-Link-22-ConditionalProcessDataDevice-20211215-IODD1.1.xml')))

    ###
    # condition 0
    ###
    PDInDecoder_0 = createDecoderClass_PDIn(my_iodd.processDataDefinition, 0)
    decoder = PDInDecoder_0()

    assert ['TN_PI_X_PDin_DetectionValue', 'TN_PI_X_PDin_TemperatureValue'] == list(
        decoder.field_names)  # checks attributes
    assert decoder.TN_PI_X_PDin_DetectionValue == 0
    assert decoder.TN_PI_X_PDin_TemperatureValue == 0

    decoder = PDInDecoder_0.from_buffer_copy(b'\x00\x02\x01\xFF')
    assert decoder.TN_PI_X_PDin_DetectionValue == 2
    assert decoder.TN_PI_X_PDin_TemperatureValue == 1

    PDOutDecoder_0 = createDecoderClass_PDOut(my_iodd.processDataDefinition, 0)
    decoder = PDOutDecoder_0()

    assert ['TN_PO_X_PDout_ControlValue'] == list(decoder.field_names)  # checks attributes
    assert decoder.TN_PO_X_PDout_ControlValue == 0

    decoder = PDOutDecoder_0.from_buffer_copy(b'\xFF\x11')
    assert decoder.TN_PO_X_PDout_ControlValue == 255

    decoder = PDOutDecoder_0.from_buffer_copy(b'\x00\x22')
    assert decoder.TN_PO_X_PDout_ControlValue == 0

    ###
    # condition 2
    ###
    PDInDecoder_2 = createDecoderClass_PDIn(my_iodd.processDataDefinition, 2)
    decoder = PDInDecoder_2()

    assert ['TN_PI_X_PDin_DetectionValue',
            'TN_V_PD_CounterValue',
            'TN_PI_X_PDin_StatusSig2',
            'TN_PI_X_PDin_StatusSig1'] == list(decoder.field_names)  # checks attributes
    assert decoder.TN_PI_X_PDin_DetectionValue == 0
    assert decoder.TN_V_PD_CounterValue == 0
    assert decoder.TN_PI_X_PDin_StatusSig2 == 0
    assert decoder.TN_PI_X_PDin_StatusSig1 == 0

    decoder = PDInDecoder_2.from_buffer_copy(b'\x00\x01\x05\x01')
    assert decoder.TN_PI_X_PDin_DetectionValue == 1
    assert decoder.TN_V_PD_CounterValue == 5
    assert decoder.TN_PI_X_PDin_StatusSig2 == 0
    assert decoder.TN_PI_X_PDin_StatusSig1 == 1

    decoder = PDInDecoder_2.from_buffer_copy(b'\x00\x03\x02\x02')
    assert decoder.TN_PI_X_PDin_DetectionValue == 3
    assert decoder.TN_V_PD_CounterValue == 2
    assert decoder.TN_PI_X_PDin_StatusSig2 == 1
    assert decoder.TN_PI_X_PDin_StatusSig1 == 0


def test_safetyProcessData():
    process_data_definition = {
        None: {'id': 'P_FSP_ProcessData',
               'pdIn': {'bitLength': 80,
                        'dataFormat': [{'bitOffset': 72,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_FST_PDin_FI_MyValueA',
                                                 'FI_MyValueA'),
                                        'subIndex': 1},
                                       {'bitOffset': 56,
                                        'data': {'bitLength': 16,
                                                 'type': int},
                                        'name': ('TN_V_FST_PDin_FI_MyValueB',
                                                 'FI_MyValueB'),
                                        'subIndex': 2},
                                       {'bitOffset': 8,
                                        'data': {'bitLength': 48,
                                                 'type': bytearray},
                                        'name': ('TN_V_FSP_SafetyCode',
                                                 'FS Safety Code'),
                                        'subIndex': 127},
                                       {'bitOffset': 7,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_PDin_I_MyValueC',
                                                 'I_MyValueC'),
                                        'subIndex': 128},
                                       {'bitOffset': 6,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_PDin_I_MyValueD',
                                                 'I_MyValueD'),
                                        'subIndex': 129},
                                       {'bitOffset': 5,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_PDin_I_MyValueE',
                                                 'I_MyValueE'),
                                        'subIndex': 130},
                                       {'bitOffset': 4,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_PDin_I_MyValueF',
                                                 'I_MyValueF'),
                                        'subIndex': 131},
                                       {'bitOffset': 0,
                                        'data': {'bitLength': 1,
                                                 'type': bool},
                                        'name': ('TN_V_PDin_I_MyValueG',
                                                 'I_MyValueG'),
                                        'subIndex': 132}],
                        'id': 'PI_FSP_PDin',
                        'name': ('TN_PI_FSP_PDin', 'PD Input')},
               'pdOut': {'bitLength': 56,
                         'dataFormat': [{'bitOffset': 8,
                                         'data': {'bitLength': 48,
                                                  'type': bytearray},
                                         'name': ('TN_V_FSP_SafetyCode',
                                                  'FS Safety Code'),
                                         'subIndex': 127},
                                        {'bitOffset': 7,
                                         'data': {'bitLength': 1,
                                                  'type': bool},
                                         'name': ('TN_V_PDout_O_MyValueA',
                                                  'O_MyValueA'),
                                         'subIndex': 128}],
                         'id': 'PO_FSP_PDout',
                         'name': ('TN_PO_FSP_PDout', 'PD Output')}}}

    PDInDecoder = createDecoderClass_PDIn(process_data_definition)
    decoder = PDInDecoder.from_buffer_copy(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    assert ['TN_V_FST_PDin_FI_MyValueA', 'TN_V_FST_PDin_FI_MyValueB', 'FI_portNum', 'FI_DCNT', 'FI_SDset',
            'FI_DCommError',
            'FI_DTimeout', 'FI_CRC', 'TN_V_PDin_I_MyValueC', 'TN_V_PDin_I_MyValueD', 'TN_V_PDin_I_MyValueE',
            'TN_V_PDin_I_MyValueF', 'TN_V_PDin_I_MyValueG'] == list(decoder.field_names)


    PDOutDecoder = createDecoderClass_PDOut(process_data_definition)
    decoder = PDOutDecoder.from_buffer_copy(b'\x00\x01\x05\x01\x01\x05\x01')

    assert ['FO_portNum', 'FO_MCNT', 'FO_SetSD', 'FO_ChFAckReq', 'FO_CRC', 'TN_V_PDout_O_MyValueA'] == list(decoder.field_names)  # checks attributes
    assert decoder.FO_portNum == 0
    assert decoder.TN_V_PDout_O_MyValueA == 0


def test_processData_ArrayT():
    process_data_definition = {
        None: {'pdIn': {'bitLength': 32,
                        'dataFormat': [{'bitOffset': 0,
                                        'data': {'bitLength': 32,
                                                 'type': bytearray},
                                        'name': ('PD_Value',
                                                 'Value'),
                                        'subIndex': 1}]
                        }
               }
    }

    PDInDecoder = createDecoderClass_PDIn(process_data_definition)
    decoder = PDInDecoder.from_buffer_copy(b'\x01\x02\x03\x04')

    assert ['PD_Value'] == list(decoder.field_names)  # checks attributes
    assert len(decoder.PD_Value) == 4
    assert decoder.PD_Value[0] == 0x01
    assert decoder.PD_Value[1] == 0x02
    assert decoder.PD_Value[2] == 0x03
    assert decoder.PD_Value[3] == 0x04

    invalid_process_data_definition = {
        None: {'pdIn': {'bitLength': 31,
                        'dataFormat': [{'bitOffset': 0,
                                        'data': {'bitLength': 31,
                                                 'type': bytearray},
                                        'name': ('PD_Value',
                                                 'Value'),
                                        'subIndex': 1}]
                        }
               }
    }

    with pytest.raises(ValueError):
        createDecoderClass_PDIn(invalid_process_data_definition)


def test_processData_int32():
    process_data_definition = {
        None: {'pdIn': {'bitLength': 32,
                        'dataFormat': [{'bitOffset': 0,
                                        'data': {'bitLength': 32,
                                                 'type': int},
                                        'name': ('PD_Value',
                                                 'Value'),
                                        'subIndex': 1}]
                        }
               }
    }

    PDInDecoder = createDecoderClass_PDIn(process_data_definition)
    decoder = PDInDecoder.from_buffer_copy(b'\x00\x00\x00\x01')

    assert ['PD_Value'] == list(decoder.field_names)  # checks attributes
    assert decoder.PD_Value == 1


def test_processData_intSizeTooLarge():
    process_data_definition = {
        None: {'pdIn': {'bitLength': 33,
                        'dataFormat': [{'bitOffset': 0,
                                        'data': {'bitLength': 33,
                                                 'type': int},
                                        'name': ('PD_Value',
                                                 'Value'),
                                        'subIndex': 1}]
                        }
               }
    }

    with pytest.raises(ValueError):
        createDecoderClass_PDIn(process_data_definition)
