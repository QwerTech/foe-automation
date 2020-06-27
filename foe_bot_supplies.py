import logging

from foe_control import pressCollect1, ydiff1, pressEsc, pressCollect2, ydiff2
from foe_pics import findSupplies, findSuppliesCollected
from foe_utils import lock, checkIfPaused, randSleepSec, waitFor


def processSupplies():  # supplies icons
    output = findSupplies()
    if output is not None:
        logging.info("Found supplies %s", output)
        with lock:
            checkIfPaused()
            # get coordinates to click from output
            pressCollect1(output)
            if waitSuppliesCollected(output.left, output.top + ydiff1):
                return

            pressEsc()
            pressCollect2(output)
            if waitSuppliesCollected(output.left, output.top + ydiff1 + ydiff2):
                return

            pressEsc()
    else:
        randSleepSec(3, 7)


def waitSuppliesCollected(left, top):
    region = [left - 20, top - 70, 70, 80]
    if waitFor(lambda: findSuppliesCollected(region)):
        logging.debug("Bot has collected supplies something from a building.")
        return True
    else:
        return False
