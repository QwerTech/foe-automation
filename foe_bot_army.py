from __future__ import annotations

from foe_pics import *
from foe_utils import randSleepSec


# functions to be run, you can change these!


def processArmy():
    output = findArmy()
    if output is not None:
        logging.info("Found army %s", output)
        processOutput(output)
    randSleepSec(5, 10)
