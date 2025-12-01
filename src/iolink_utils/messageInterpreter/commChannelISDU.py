from typing import Union, Optional, List, Dict
from datetime import datetime as dt
from enum import IntEnum

from iolink_utils.octetDecoder.octetStreamDecoderMessages import DeviceMessage, MasterMessage
from iolink_utils.octetDecoder.octetDecoder import IService
from iolink_utils.definitions.transmissionDirection import TransmissionDirection
from iolink_utils.definitions.ISDU import IServiceNibble, FlowCtrl
from .ISDUrequests import createISDURequest
from .ISDUresponses import createISDUResponse


class TransactionISDU:
    def __init__(self, value: str):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.value: str = value

    def data(self) -> Dict:
        return {
            'isdu': ' '.join(filter(None, [self.value]))
        }

    def __str__(self):
        return f"ISDU: {' '.join(filter(None, [self.value]))}"



class CommChannelISDU:
    class State(IntEnum):
        Idle = 0,
        Request = 1,
        RequestFinished = 2,
        WaitForResponse = 3,
        Response = 4,
        ResponseFinished = 5

    def __init__(self):
        self.state: CommChannelISDU.State = CommChannelISDU.State.Idle

        self.direction: TransmissionDirection = TransmissionDirection.Read
        self.flowCtrl: FlowCtrl = FlowCtrl()

        self.isduRequest = None
        self.isduResponse = None

    def processMasterMessage(self, message: MasterMessage):
        self.direction = TransmissionDirection(message.mc.read)
        self.flowCtrl = FlowCtrl(message.mc.address)

        if self.flowCtrl.state != FlowCtrl.State.Idle:
            print(message)

        if self.state == CommChannelISDU.State.Idle:
            if self.flowCtrl.state == FlowCtrl.State.Start and self.direction == TransmissionDirection.Write:
                self.isduRequest = createISDURequest(IService(message.od[0]))

                self.isduRequest.setStartTime(message.start_time)
                self.isduRequest.setEndTime(message.end_time)
                self.isduRequest.appendOctets(self.flowCtrl, message.od)

                if self.isduRequest.isComplete:
                    self.state = CommChannelISDU.State.RequestFinished
                else:
                    self.state = CommChannelISDU.State.Request

        elif self.state == CommChannelISDU.State.Request:
            if self.flowCtrl.state == FlowCtrl.State.Count:
                self.isduRequest.setEndTime(message.end_time)
                self.isduRequest.appendOctets(self.flowCtrl, message.od)

                if self.isduRequest.isComplete:
                    self.state = CommChannelISDU.State.RequestFinished

            elif self.flowCtrl.state == FlowCtrl.State.Abort:
                self.state = CommChannelISDU.State.Idle

        elif self.state == CommChannelISDU.State.Response: # WaitForResponse
            if self.flowCtrl.state == FlowCtrl.State.Start and self.direction == TransmissionDirection.Read:
                pass

        return []

    def processDeviceMessage(self, message: DeviceMessage):
        isduTransactions = []

        if self.flowCtrl.state != FlowCtrl.State.Idle:
            print(message)

        if self.state == CommChannelISDU.State.RequestFinished:
            self.isduRequest.setEndTime(message.end_time)

            transaction = TransactionISDU(str(self.isduRequest))
            transaction.start_time = message.start_time
            transaction.end_time = message.end_time
            isduTransactions.append(transaction)
            self.state = CommChannelISDU.State.WaitForResponse

        elif self.state == CommChannelISDU.State.WaitForResponse:
            if self.flowCtrl.state == FlowCtrl.State.Start:
                if IService(message.od[0]).service != IServiceNibble.NoService:
                    self.isduResponse = createISDUResponse(IService(message.od[0]))

                    self.isduResponse.setStartTime(message.start_time)
                    self.isduResponse.setEndTime(message.end_time)
                    self.isduResponse.appendOctets(self.flowCtrl, message.od)

                    if self.isduResponse.isComplete:
                        transaction = TransactionISDU(str(self.isduResponse))
                        transaction.start_time = message.start_time
                        transaction.end_time = message.end_time
                        isduTransactions.append(transaction)
                        self.state = CommChannelISDU.State.Idle
                    else:
                        self.state = CommChannelISDU.State.Response

        elif self.state == CommChannelISDU.State.Response:
            if self.flowCtrl.state == FlowCtrl.State.Count:
                self.isduResponse.setEndTime(message.end_time)
                self.isduResponse.appendOctets(self.flowCtrl, message.od)

                if self.isduResponse.isComplete:
                    transaction = TransactionISDU(str(self.isduResponse))
                    transaction.start_time = message.start_time
                    transaction.end_time = message.end_time
                    isduTransactions.append(transaction)
                    self.state = CommChannelISDU.State.Idle

            elif self.flowCtrl.state == FlowCtrl.State.Abort:
                self.state = CommChannelISDU.State.Idle

        return isduTransactions
