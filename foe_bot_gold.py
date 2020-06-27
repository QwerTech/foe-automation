import logging

from foe_common import isThereSomethingToCollect
from foe_control import pressCollect1, ydiff1, ydiff2, pressCollect2, pressEsc
from foe_pics import findGold, findGoldCollected
from foe_utils import lock, checkIfPaused, waitFor, randSleepSec


def goldCollector():  # gold icons
    if not isThereSomethingToCollect():
        randSleepSec(5, 15)
        return

    output = findGold()

    if output is not None:
        logging.info("Found gold %s", output)
        with lock:
            checkIfPaused()
            # get coordinates to click from output
            pressCollect1(output)
            if waitGoldCollected(output.left, output.top + ydiff1):
                return

            pressEsc()
            pressCollect2(output)
            if waitGoldCollected(output.left, output.top + ydiff1 + ydiff2):
                return

            pressEsc()
    else:
        randSleepSec(5, 15)


def waitGoldCollected(left, top):
    region = [left - 10, top - 70, 50, 80]
    if waitFor(lambda: findGoldCollected(region)):
        logging.debug("Bot has collected gold something from a building.")
        return True
    else:
        return False
