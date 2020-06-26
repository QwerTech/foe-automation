import logging

import pyautogui

from foe_pics import findLandscape, findButtonsPanel
from foe_scroll import scroll
from foe_utils import randSleepSec, checkIfPaused, lock, randDur, randSleepMs


def zoomOut():
    if findLandscape() is not None:
        randSleepSec(60, 120)
        return
    panel = findButtonsPanel()
    if panel is None:
        randSleepSec(5, 10)
        return
    with lock:
        checkIfPaused()
        logging.info("Zooming out")
        pyautogui.moveTo(panel[0], panel[1], duration=randDur())
        pyautogui.moveRel(50, -50, duration=randDur())
        pyautogui.click()
        randSleepMs()
        scroll(-1, 1)
        randSleepMs()
        scroll(-1, 1)
        randSleepSec(60, 120)
        logging.info("Zoomed out")
