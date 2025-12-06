from iolink_utils.definitions.profiles import ProfileID


def test_profiles():
    profileID = ProfileID(16385)
    assert profileID.name == 'SafetyDevice'
    assert profileID.value == 16385

    # unknown profile ID will not raise an exception
    # (because they seem not to be documented completely)
    # See IOL_ProfileIDOverview_V11_Mar2023.pdf
    profileID = ProfileID(99999)
    assert profileID.name == 'Unknown'
    assert profileID.value == 0

    profileID = ProfileID(32789)
    assert profileID.name == 'NoName_32789'
    assert profileID.value == 32789
