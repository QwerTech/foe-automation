import logging
import random

import pyautogui

from foe_control import pressButton
from foe_images import same
from foe_pics import findSoguildians, findNeighbours, findFriends, findFullFf, \
    findNext, findAnySocialButton
from foe_utils import randSleepSec, randSleepMs


def processSocial():
    global socialProcesses
    initSocialProcesses()
    random.shuffle(socialProcesses)
    while socialProcesses:
        process = socialProcesses.pop()
        process()
    randSleepSec(300, 600)


def initSocialProcesses():
    global socialProcesses
    socialProcesses = [processFriends, processNeighbours, processSoguildians]
    # socialProcesses = [processSoguildians]


def processSoguildians():
    logging.info("Precessing soguildians")
    pressButton(findSoguildians(), True)
    processAllSocialPages()


def processNeighbours():
    logging.info("Precessing neighbours")
    pressButton(findNeighbours(), True)
    processAllSocialPages()


def processFriends():
    logging.info("Precessing friends")
    pressButton(findFriends(), True)
    processAllSocialPages()


def processAllSocialPages():
    pages = 16
    # pages = 3
    lastPage = False
    pressButton(findFullFf(), True)
    while pages >= 0 and not lastPage:
        pages = pages - 1
        processSocialPage()
        lastPage = nextPage()


def nextPage():
    nextBtn = findNext()
    friendsRegion = [nextBtn.left - 640, nextBtn.top - 50, 530, 80]
    before = pyautogui.screenshot(region=friendsRegion)
    pressButton(nextBtn, True)
    randSleepMs()
    after = pyautogui.screenshot(region=friendsRegion)
    return same(before, after)


def processSocialPage():
    output = True
    while output is not None:
        output = findAnySocialButton()
        if output is not None:
            logging.info("Precessing social button")
            pressButton(output, True)
            randSleepMs(500, 900)
