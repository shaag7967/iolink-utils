import pytest
from iolink_utils.definitions.eventMemory import Event, EventMemory, EventQualifier


def test_event_initialState():
    e = Event()

    assert int(e.qualifier) == 0
    assert e.code == 0
    assert not e.isComplete()


def test_event_eq():
    e1 = Event()
    e2 = Event()
    assert e1 == e2

    e1.setCode(5)
    assert e1 != e2

    assert e1 != object()

    e1 = Event()
    e1.setQualifier(EventQualifier(0x05))
    e1.setCode(0xABCD)

    e2 = e1.copy()

    assert e1 == e2
    assert e1 is not e2

    e1 = Event()
    e2 = Event()

    e1.setQualifier(EventQualifier(0x03))
    e1.setCodeMSB(0x12)
    e1.setCodeLSB(0x34)

    e2.setCode(0x1234)
    e2.setQualifier(EventQualifier(0x03))

    assert e1 == e2


def test_event_checkQualifierCopy():
    e = Event()
    q = EventQualifier(0b10101010)

    e.setQualifier(q)

    assert int(e.qualifier) == int(q)
    assert e.qualifier is not q


def test_event_setCodeMsbAndLsb():
    e = Event()

    e.setCodeMSB(0x12)
    assert e.code == 0x1200
    assert not e.isComplete()

    e.setCodeLSB(0x34)
    assert e.code == 0x1234


def test_event_complete():
    e = Event()

    e.setQualifier(EventQualifier(1))
    assert not e.isComplete()
    e.setCodeMSB(0x12)
    assert not e.isComplete()
    e.setCodeLSB(0x34)
    assert e.isComplete()


def test_event_clear():
    e = Event()
    e.setQualifier(EventQualifier(1))
    e.setCode(0x1234)
    assert e.isComplete()

    e.clear()

    assert int(e.qualifier) == 0
    assert e.code == 0
    assert not e.isComplete()


def test_event_copyIsDeep():
    e1 = Event()
    e1.setQualifier(EventQualifier(5))
    e1.setCodeMSB(0x12)
    assert not e1.isComplete()

    e2 = e1.copy()

    assert not e2.isComplete()
    assert e2 is not e1
    assert e2.code == e1.code
    assert int(e2.qualifier) == int(e1.qualifier)
    assert e2._state == e1._state

    e2.setCodeLSB(0x34)
    assert e2.isComplete()
    assert not e1.isComplete()

