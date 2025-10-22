from iolink_utils.exceptions import InvalidProcessDataDefinition
from ._processDataDecoderInternal import _init, _decodePDIn, _decodePDOut


def createPDInDecoderClass(json_process_data_def, condition=None):
    attributes = {
        "__init__": _init
    }

    pd_def = json_process_data_def[condition]
    if 'pdIn' in pd_def:
        cls_name = f"PDInDecoder_{pd_def['pdIn']['id']}"
        attributes["pdin_format"] = pd_def['pdIn']['dataFormat']
        attributes["pdin_length"] = pd_def['pdIn']['bitLength']
        attributes["decodePDIn"] = _decodePDIn
    else:
        raise InvalidProcessDataDefinition(f"ProcessDataIn: key 'pdIn' not found (for condition {condition}).", json_process_data_def)

    cls = type(
        cls_name,
        (object,),
        attributes
    )
    return cls

def createPDOutDecoderClass(json_process_data_def, condition=None):
    attributes = {
        "__init__": _init
    }

    pd_def = json_process_data_def[condition]
    if 'pdOut' in pd_def:
        cls_name = f"PDOutDecoder_{pd_def['pdOut']['id']}"
        attributes["pdout_format"] = pd_def['pdOut']['dataFormat']
        attributes["pdout_length"] = pd_def['pdOut']['bitLength']
        attributes["decodePDOut"] = _decodePDOut
    else:
        raise InvalidProcessDataDefinition(f"ProcessDataOut: key 'pdOut' not found (for condition {condition}).", json_process_data_def)

    cls = type(
        cls_name,
        (object,),
        attributes
    )
    return cls