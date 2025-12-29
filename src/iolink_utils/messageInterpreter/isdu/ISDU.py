from datetime import datetime as dt
from abc import abstractmethod

from iolink_utils.definitions.iServiceNibble import IServiceNibble
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.messageInterpreter.transaction import Transaction

from .ISDUflowControl import FlowControl


class ISDU(Transaction):
    def __init__(self, iService: IService):
        super().__init__()

        self._flowControl: FlowControl = FlowControl()

        self._service = IServiceNibble(iService.service)
        self._length = iService.length
        self._rawData: bytearray = bytearray()
        self._chkpdu: int = 0

        self._isValid: bool = False
        self._isComplete: bool = False

    @property
    def isValid(self) -> bool:
        return self._isValid

    @property
    def isComplete(self) -> bool:
        return self._isComplete

    def _hasExtendedLength(self):
        return self._length == 1

    def _getTotalLength(self):
        return int(self._rawData[1]) if self._hasExtendedLength() else self._length

    def _calculateCheckByte(self) -> int:
        chk = 0
        for b in self._rawData[:-1]:  # except chkpdu which is last byte
            chk ^= b
        return chk

    def setEndTime(self, endTime: dt):
        self.endTime = endTime

    def appendOctets(self, flowControl: FlowControl, requestData: bytearray) -> bool:
        if flowControl.state == FlowControl.State.Start or flowControl.state == FlowControl.State.Count:
            # TODO if same count value, replace last received data
            self._rawData.extend(requestData)

            targetLength = self._getTotalLength()
            if len(self._rawData) > targetLength:
                self._rawData = self._rawData[:targetLength]
        self._flowControl = flowControl

        if len(self._rawData) == self._getTotalLength():
            self._chkpdu = self._rawData[-1]
            self._isValid = self._chkpdu == self._calculateCheckByte()
            self._isComplete = True
        return self._isComplete

    @abstractmethod
    def name(self) -> str:  # pragma: no cover
        return 'ISDU'
