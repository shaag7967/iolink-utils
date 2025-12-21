from iolink_utils.octetDecoder.octetDecoder import MSequenceCapability


def test_mSequenceCapability_zeroInit():
    cap = MSequenceCapability()
    assert cap.isduSupport == 0
    assert cap.preoperateCode == 0
    assert cap.operateCode == 0

    assert cap.get() == 0
    assert int(cap) == 0


def test_mSequenceCapability_ctorInit():
    cap = MSequenceCapability(41) #  10 100 1
    assert cap.isduSupport == 1
    assert cap.preoperateCode == 2
    assert cap.operateCode == 4

    assert cap.get() == 41
    assert int(cap) == 41


def test_mSequenceCapability_setGet():
    cap = MSequenceCapability()
    assert cap.get() == 0

    cap.set(63) #  11 111 1
    assert cap.isduSupport == 1
    assert cap.preoperateCode == 3
    assert cap.operateCode == 7
    assert cap.get() == 63

    cap.operateCode = 0
    assert cap.get() == 49 #  11 000 1
    assert cap.isduSupport == 1
    assert cap.preoperateCode == 3

    cap.preoperateCode = 0
    assert cap.get() == 1 #  00 000 1
    assert cap.isduSupport == 1

    cap.isduSupport = 0
    assert cap.get() == 0 #  00 000 0

    cap.set(0)
    assert cap.get() == 0
