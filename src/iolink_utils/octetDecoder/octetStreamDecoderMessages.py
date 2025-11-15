from datetime import datetime as dt
from iolink_utils.octetDecoder.octetDecoder import MC, CKT, CKS


class MasterMessage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.mc: MC = MC()
        self.ckt: CKT = CKT()
        self.pdOut: bytearray = bytearray()
        self.od: bytearray = bytearray()

    def __repr__(self):
        elements = [f"mc={self.mc}", f"ckt={self.ckt}"]
        if self.pdOut:
            elements.append(f"pdOut={bytes(self.pdOut).hex()}")
        if self.od:
            elements.append(f"od={bytes(self.od).hex()}")
        return f"MasterMessage({', '.join(elements)})"


class DeviceMessage:
    def __init__(self):
        self.start_time: dt = dt(1970, 1, 1)
        self.end_time: dt = dt(1970, 1, 1)

        self.od: bytearray = bytearray()
        self.pdIn: bytearray = bytearray()
        self.cks: CKS = CKS()

    def __repr__(self):
        elements = []
        if self.od:
            elements.append(f"od={bytes(self.od).hex()}")
        if self.pdIn:
            elements.append(f"pdIn={bytes(self.pdIn).hex()}")
        elements.append(f"cks={self.cks}")
        return f"DeviceMessage({', '.join(elements)})"
