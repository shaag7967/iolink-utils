import ctypes
from iolink_utils.exceptions import InvalidOctetValue


class OctetDecoderBase(ctypes.BigEndianStructure):
    """Basisklasse für Bitfeld-Strukturen mit gemeinsamen Methoden."""
    _pack_ = 1

    def __init__(self, value: int = 0):
        super().__init__()
        self.set(value)

    def __int__(self):
        """Gibt den Bytewert zurück, der die Bitfelder repräsentiert."""
        return int.from_bytes(bytes(self), "big")

    def get(self) -> int:
        """Alias für __int__()."""
        return int(self)

    def set(self, value: int):
        """Setzt die Struktur basierend auf einem Bytewert."""
        _MAX_OCTET_VALUE = 255
        if 0 <= value <= _MAX_OCTET_VALUE:
            ctypes.memmove(ctypes.addressof(self), ctypes.byref(ctypes.c_uint8(value)), 1)
        else:
            raise InvalidOctetValue()

    def __repr__(self):
        """Dynamische Darstellung aller Felder basierend auf _fields_."""
        fields_repr = ", ".join(
            f"{name}={getattr(self, name)}" for name, *_ in self._fields_
        )
        return f"{self.__class__.__name__}({fields_repr})"