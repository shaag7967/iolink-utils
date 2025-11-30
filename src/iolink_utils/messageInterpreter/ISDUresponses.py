from datetime import datetime as dt

from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.ISDU import IServiceNibble, FlowCtrl


class ISDUResponse:
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

    def _getTotalLength(self):
        return self.length if self.length > 1 else int(self.rawData[1])  # extLength

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


class ISDUResponse_WriteResp_M(ISDUResponse):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.errorCode: int = 0
        self.additionalCode: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            self.errorCode = int(self.rawData[1])
            self.additionalCode = int(self.rawData[2])
        return finished

    def __str__(self):
        return f"ISDUResponse_WriteResp_M(errorCode={self.errorCode} additionalCode={self.additionalCode} data={self.rawData.hex()})"


class ISDUResponse_WriteResp_P(ISDUResponse):
    def __init__(self, iService: IService):
        super().__init__(iService)

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        return super().appendOctets(flowCtrl, requestData)

    def __str__(self):
        return f"ISDUResponse_WriteResp_P(data={self.rawData.hex()})"


class ISDUResponse_ReadResp_M(ISDUResponse):
    def __init__(self, iService: IService):
        super().__init__(iService)
        self.errorCode: int = 0
        self.additionalCode: int = 0

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        finished = super().appendOctets(flowCtrl, requestData)

        if finished:
            self.errorCode = int(self.rawData[1])
            self.additionalCode = int(self.rawData[2])
        return finished

    def __str__(self):
        return f"ISDUResponse_ReadResp_M(errorCode={self.errorCode} additionalCode={self.additionalCode} data={self.rawData.hex()})"


class ISDUResponse_ReadResp_P(ISDUResponse):
    def __init__(self, iService: IService):
        super().__init__(iService)

    def appendOctets(self, flowCtrl: FlowCtrl, requestData: bytearray) -> bool:
        return super().appendOctets(flowCtrl, requestData)

    def __str__(self):
        return f"ISDUResponse_ReadResp_P(data={self.rawData.hex()})"


def createISDUResponse(iService: IService):
    _req_map = {
        IServiceNibble.D_WriteResp_M: ISDUResponse_WriteResp_M,
        IServiceNibble.D_WriteResp_P: ISDUResponse_WriteResp_P,
        IServiceNibble.D_ReadResp_M: ISDUResponse_ReadResp_M,
        IServiceNibble.D_ReadResp_P: ISDUResponse_ReadResp_P,
    }

    if iService.service not in _req_map:
        raise ValueError(f"Invalid request nibble: {iService}")

    return _req_map[iService.service](iService)
