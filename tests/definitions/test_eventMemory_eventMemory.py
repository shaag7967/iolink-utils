import pytest
from iolink_utils.exceptions import InvalidEventMemoryAddress, InvalidEventStatusCode
from iolink_utils.definitions.eventMemory import Event, EventMemory, EventQualifier, StatusCodeType2


def test_eventMemory_initialState():
    mem = EventMemory()
    assert not mem.isComplete()  # no details
    for e in mem.events:
        assert not e.isComplete()  # events are not complete


def test_eventMemory_invalidAddress():
    mem = EventMemory()
    mem.setMemory(0x12, 0)

    with pytest.raises(InvalidEventMemoryAddress):
        mem.setMemory(0x13, 0)


def test_eventMemory_invalidStatusCode():
    mem = EventMemory()

    with pytest.raises(InvalidEventStatusCode):
        mem.setMemory(0, 0x00)


def test_eventMemory_setMemory():
    mem = EventMemory()

    statusCode = StatusCodeType2()
    statusCode.details = 1

    # Event 1
    statusCode.evt1 = 1
    mem.setMemory(0, int(statusCode))
    assert not mem.isComplete()

    mem.setMemory(1, 0x01)   # qualifier
    assert not mem.isComplete()
    mem.setMemory(2, 0x12)   # code MSB
    assert not mem.isComplete()
    mem.setMemory(3, 0x34)   # code LSB
    assert mem.isComplete()
    assert mem.events[0].isComplete()

    # Event 6
    statusCode.evt6 = 1
    mem.setMemory(0, int(statusCode))
    assert not mem.isComplete()

    mem.setMemory(16, 0x01)   # qualifier
    assert not mem.isComplete()
    mem.setMemory(17, 0x12)   # code MSB
    assert not mem.isComplete()
    mem.setMemory(18, 0x34)   # code LSB
    assert mem.events[5].code == 0x1234
    assert mem.isComplete()
    assert mem.events[5].isComplete()

    # all event slots
    assert mem.events[0].isComplete()
    assert not mem.events[1].isComplete()
    assert not mem.events[2].isComplete()
    assert not mem.events[3].isComplete()
    assert not mem.events[4].isComplete()
    assert mem.events[5].isComplete()


def test_eventMemory_clear():
    mem = EventMemory()
    assert not mem.isComplete()

    mem.setMemory(0, 0b10000001)
    assert not mem.isComplete()
    mem.setMemory(1, 1)
    mem.setMemory(2, 0x12)
    mem.setMemory(3, 0x34)
    assert mem.isComplete()

    mem.clear()

    assert not mem.isComplete()
    for e in mem.events:
        assert not e.isComplete()


def test_eventMemory_copyIsDeep():
    mem1 = EventMemory()
    mem1.setMemory(0, 0b10000010)

    mem1.setMemory(4, 1)
    mem1.setMemory(5, 0x12)
    mem1.setMemory(6, 0x34)

    mem2 = mem1.copy()

    assert mem2 is not mem1
    assert mem2.statusCode is not mem1.statusCode

    for e1, e2 in zip(mem1.events, mem2.events):
        assert e1 is not e2
        assert e1.code == e2.code
        assert int(e1.qualifier) == int(e2.qualifier)

    mem2.events[0].setCodeLSB(0xFF)
    assert mem1.events[0].code != mem2.events[0].code


def test_event_memory_eq():
    m1 = EventMemory()
    m2 = EventMemory()

    assert m1 == m2

    m1.setMemory(0, 0x81)
    assert m1 != m2

    m2.setMemory(0, 0x81)
    assert m1 == m2

    m1.setMemory(1, 0x01)
    assert m1 != m2

    m2.setMemory(1, 0x01)
    assert m1 == m2

    m1.setMemory(2, 0x12)
    assert m1 != m2

    m2.setMemory(2, 0x12)
    assert m1 == m2

    m1.setMemory(3, 0x34)
    assert m1 != m2

    m2.setMemory(3, 0x34)
    assert m1 == m2

    m3 = m1.copy()
    assert m3 == m1
    assert m3 is not m1

    m3.setMemory(1, 0x02)
    assert m3 != m1

    assert m1 != object()
