import logging
import threading
from random import randint
from time import sleep

import keyboard as kb
from waiting import wait, TimeoutExpired
from win32api import GetKeyState
from win32con import VK_SCROLL

lock = threading.RLock()


def waitFor(findPicFunc, timeout_seconds=0.5, sleep_seconds=0):
    try:
        wait(lambda: findPicFunc() is not None, timeout_seconds=timeout_seconds,
             sleep_seconds=sleep_seconds)
        return True
    except TimeoutExpired:
        return False


def randSleepSec(fromSec=1, toSec=3):
    checkIfPaused()
    secs = randint(fromSec, toSec)
    logging.debug("Sleeping for %s secs.", secs)
    sleep(secs)


def randSleepMs(fromMs=220, toMs=550):
    checkIfPaused()
    sleep(randint(fromMs, toMs) / 1000)


def randDur(): return randint(150, 750) / 1000


def checkIfPaused():
    while kb.is_pressed("ctrl") or GetKeyState(VK_SCROLL) == 1:
        logging.warning("PAUSED")
        sleep(1)
