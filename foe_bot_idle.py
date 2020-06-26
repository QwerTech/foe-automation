import logging

import pyautogui

from foe_control import pressCollect1, pressCollect2, pressEsc
from foe_pics import findIdle
from foe_utils import lock, randSleepMs, randSleepSec


def processIdleOutput(output):
    with lock:
        pressCollect1(output)
        randSleepMs()
        pyautogui.typewrite(['1', '2', '3', '4', '5'])
        pressCollect2(output)
        randSleepMs()
        pyautogui.typewrite(['1', '2', '3', '4', '5'])
        logging.debug("Bot has restarted a production building.")
        pressEsc()


def processIdleBuildings():  # idle building icons
    output = findIdle()
    if output is not None:
        logging.info("Found idle %s", output)
        processIdleOutput(output)
    else:
        randSleepSec(3, 7)
