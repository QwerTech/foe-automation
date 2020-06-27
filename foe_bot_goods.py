from __future__ import annotations

from foe_common import isThereSomethingToCollect
from foe_control import pressCollect1, pressCollect2, pressEsc
from foe_pics import *
from foe_utils import randSleepSec, lock, randSleepMs


# functions to be run, you can change these!


def processGoods():  # goods boxes icons
    if not isThereSomethingToCollect():
        randSleepSec(5, 15)
        return

    output = findGoods()
    if output is not None:
        logging.info("Found good %s", output)
        processGoodsOutput(output)
    else:
        randSleepSec(3, 7)


def processGoodsOutput(output):
    with lock:
        pressCollect1(output)
        randSleepMs()
        pressEsc()
        pressCollect2(output)
        randSleepMs()
        logging.debug("Bot has restarted a production building.")
        pressEsc()
