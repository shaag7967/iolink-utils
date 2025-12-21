import csv
import os
from datetime import datetime


from iolink_utils.messageInterpreter.messageInterpreter import MessageInterpreter
from iolink_utils.messageInterpreter.isdu.ISDU import ISDU


def test_interpreterISDU():
    interpreter = MessageInterpreter()
