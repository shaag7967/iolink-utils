from datetime import datetime as dt

from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.ISDU import IServiceNibble, FlowCtrl


class ISDURequest:
    def __init__(self, iService: IService):
        self.flowCtrl: FlowCtrl = FlowCtrl()

        self.service = IServiceNibble(iService.service)
        self.length = iService.length
        self.rawData: bytearray = bytearray()
        self.chkpdu: int = 0

        self.isValid = False
        self.isComplete = False

        self.start_time = dt(1970, 1, 1)
        self.end_time = dt(1970, 1, 1)

    def _hasExtendedLength(self):
        return self.length == 1

    def _getTotalLength(self):
        return int(self.rawData[1]) if self._hasExtendedLength() else self.length

    def _calculateCheckByte(self) -> int:
        chk = 0
        for b in self.rawData[:-1]:  # except chkpdu which is last byte
            chk ^= b
        return chk

    def setStartTime(self, start_time: dt):
        self.start_time = start_time

    def setEndTime(self, end_time: dt):
        self.end_time = end_time

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        if flowCtrl.state == FlowCtrl.State.Start or flowCtrl.state == FlowCtrl.State.Count:
            # TODO if same count value, replace last received data
            self.rawData.extend(requestData)

            targetLength = self._getTotalLength()
            if len(self.rawData) > targetLength:
                self.rawData = self.rawData[:targetLength]
        self.flowCtrl = flowCtrl

        if len(self.rawData) == self._getTotalLength():
            self.chkpdu = self.rawData[-1]
            self.isValid = self.chkpdu == self._calculateCheckByte()
            self.isComplete = True
        return self.isComplete


class ISDURequest_Write8bitIdx(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            pos = 2 if self._hasExtendedLength() else 1
            self.index = int(self.rawData[pos])
        return finished

    def __str__(self):
        return f"ISDURequest_Write8bitIdx(index={self.index} data={self.rawData.hex()})"


class ISDURequest_Write8bitIdxSub(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0
        self.subIndex: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            pos = 2 if self._hasExtendedLength() else 1
            self.index = int(self.rawData[pos])
            self.subIndex = int(self.rawData[pos+1])
        return finished

    def __str__(self):
        return f"ISDURequest_Write8bitIdxSub(index={self.index} subIndex={self.subIndex} data={self.rawData.hex()})"


class ISDURequest_Write16bitIdxSub(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0
        self.subIndex: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            pos = 2 if self._hasExtendedLength() else 1
            self.index = int.from_bytes(self.rawData[pos:pos+2], byteorder='big')
            self.subIndex = int(self.rawData[pos+2])
        return finished

    def __str__(self):
        return f"ISDURequest_Write16bitIdxSub(index={self.index} subIndex={self.subIndex} data={self.rawData.hex()})"


### READ ###

class ISDURequest_Read8bitIdx(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            self.index = int(self.rawData[1])
        return finished

    def __str__(self):
        return f"ISDURequest_Read8bitIdx(index={self.index} data={self.rawData.hex()})"


class ISDURequest_Read8bitIdxSub(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0
        self.subIndex: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            self.index = int(self.rawData[1])
            self.subIndex = int(self.rawData[2])
        return finished

    def __str__(self):
        return f"ISDURequest_Read8bitIdxSub(index={self.index} subIndex={self.subIndex} data={self.rawData.hex()})"


class ISDURequest_Read16bitIdxSub(ISDURequest):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.index: int = 0
        self.subIndex: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            self.index = int.from_bytes(self.rawData[1:2], byteorder='big')
            self.subIndex = int(self.rawData[3])
        return finished

    def __str__(self):
        return f"ISDURequest_Read16bitIdxSub(index={self.index} subIndex={self.subIndex} data={self.rawData.hex()})"


def createISDURequest(iService: IService):
    _req_map = {
        IServiceNibble.M_WriteReq_8bitIdx: ISDURequest_Write8bitIdx,
        IServiceNibble.M_WriteReq_8bitIdxSub: ISDURequest_Write8bitIdxSub,
        IServiceNibble.M_WriteReq_16bitIdxSub: ISDURequest_Write16bitIdxSub,
        IServiceNibble.M_ReadReq_8bitIdx: ISDURequest_Read8bitIdx,
        IServiceNibble.M_ReadReq_8bitIdxSub: ISDURequest_Read8bitIdxSub,
        IServiceNibble.M_ReadReq_16bitIdxSub: ISDURequest_Read16bitIdxSub,
    }

    if iService.service not in _req_map:
        raise ValueError(f"Invalid request nibble: {iService}")

    return _req_map[iService.service](iService)
