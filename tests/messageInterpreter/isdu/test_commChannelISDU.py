import pytest
from datetime import datetime as dt

from iolink_utils.messageInterpreter.isdu.commChannelISDU import CommChannelISDU


def test_commChannelDiagnosis_reset():
    channel = CommChannelISDU()

    channel._state = CommChannelISDU.State.Response
    channel.reset()

    assert channel._state == CommChannelISDU.State.Idle
