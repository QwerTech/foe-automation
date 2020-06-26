import logging
from random import randint

import pyautogui

from foe_utils import checkIfPaused, randDur, lock, randSleepMs

# One might need to change these based on screen resolution
ydiff1 = 60
ydiff2 = -25


def pressEsc():
    checkIfPaused()
    randSleepMs()
    pyautogui.typewrite(['esc'])


def processOutput(output):
    with lock:
        checkIfPaused()
        # get coordinates to click from output
        pressCollect1(output)
        pressEsc()
        pressCollect2(output)
        logging.debug("Bot has collected something from a building.")
        pressEsc()


def pressCollect1(output):
    # goto coordinates and click there
    moveAndClick(output.left, output.top + ydiff1)


def pressCollect2(output):
    # goto coordinates and click there
    moveAndClick(output.left, output.top + ydiff1 + ydiff2)


def moveAndClick(left, top):
    with lock:
        checkIfPaused()
        pyautogui.moveTo(left, top, duration=randDur())
        pyautogui.click()


def pressButton(output, suppressESC):
    if output is None:
        logging.warning("There is no button")
        return
    with lock:
        checkIfPaused()
        # get coordinates to click from output
        xcoord, ycoord, xcoord2, ycoord2 = output
        # goto coordinates and click there
        pyautogui.moveTo(randint(xcoord + 1, xcoord + xcoord2 - 1),
                         randint(ycoord + 1, ycoord + ycoord2 - 1),
                         duration=randDur())
        # sleep(randint(12, 25) / 100)
        pyautogui.click()
        logging.debug("Bot has clicked a button.")
        if not suppressESC:
            pressEsc()
