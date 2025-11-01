import pytest
from pathlib import Path
from pprint import pprint
from iolink_utils.iodd.iodd import Iodd
from iolink_utils.octetDecoder.processDataDecoder import createDecoderClass_PDIn, createDecoderClass_PDOut


def test_decoder_ConditionalProcessDataDevice():
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
    :return:
    """
    test_dir = Path(__file__).parent
    my_iodd = Iodd(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-22-ConditionalProcessDataDevice-20211215-IODD1.1.xml')))

    ###
    # condition 0
    ###
    PDInDecoder_0 = createDecoderClass_PDIn(my_iodd.process_data_definition, 0)
    decoder = PDInDecoder_0()

    assert ['TN_PI_X_PDin_DetectionValue', 'TN_PI_X_PDin_TemperatureValue'] == list(decoder.field_names) # checks attributes
    assert decoder.TN_PI_X_PDin_DetectionValue == 0
    assert decoder.TN_PI_X_PDin_TemperatureValue == 0

    decoder = PDInDecoder_0.from_buffer_copy(b'\xFF\xFF\x01\xFF')
    assert decoder.TN_PI_X_PDin_DetectionValue == 65535
    assert decoder.TN_PI_X_PDin_TemperatureValue == 1

    ###
    # condition 2
    ###
    PDInDecoder_2 = createDecoderClass_PDIn(my_iodd.process_data_definition, 2)
    decoder = PDInDecoder_2()

    assert ['TN_PI_X_PDin_DetectionValue', 'TN_V_PD_CounterValue', 'TN_PI_X_PDin_StatusSig2', 'TN_PI_X_PDin_StatusSig1'] == \
           list(decoder.field_names) # checks attributes
    assert decoder.TN_PI_X_PDin_DetectionValue == 0
    assert decoder.TN_V_PD_CounterValue == 0
    assert decoder.TN_PI_X_PDin_StatusSig2 == False
    assert decoder.TN_PI_X_PDin_StatusSig1 == False

    decoder = PDInDecoder_2.from_buffer_copy(b'\x00\x01\x05\x01')
    assert decoder.TN_PI_X_PDin_DetectionValue == 1
    assert decoder.TN_V_PD_CounterValue == 5
    assert decoder.TN_PI_X_PDin_StatusSig2 == False
    assert decoder.TN_PI_X_PDin_StatusSig1 == True

    decoder = PDInDecoder_2.from_buffer_copy(b'\x00\x03\x02\x02')
    assert decoder.TN_PI_X_PDin_DetectionValue == 3
    assert decoder.TN_V_PD_CounterValue == 2
    assert decoder.TN_PI_X_PDin_StatusSig2 == True
    assert decoder.TN_PI_X_PDin_StatusSig1 == False
