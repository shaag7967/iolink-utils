from iolink_utils.iodd.iodd_version import Version

def test_iodd_version():
    ver = Version()

    assert str(ver) == "Version(V0.0.0.0)"
    assert ver < Version("1.0")
    assert ver < Version("V0.1.2.3")

    assert str(Version("1.2.1")) == "Version(V1.2.1)"

    assert Version("1.2.0") == Version("1.2")
    assert Version("1.2.0.0") == Version("1.2")
    assert Version("1.2") < Version("1.2.1")
    assert Version("1.2.1") > Version('1.2')
    assert Version("1.2.3") > Version("1.2.0")
