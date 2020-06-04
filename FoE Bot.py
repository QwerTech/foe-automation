import logging
import random
import threading
import time
from random import randint
from time import sleep

import keyboard as kb
import pyautogui
import win32api
import win32con

# functions to be run, you can change these!
collectGold = True  # collect gold from buildings.
collectArmy = True  # collect gold from buildings.
collectSupplies = True  # collect supplies from buildings.
restartIdleBuildings = True  # restart any idle building.
collectGoods = True  # collect goods from buildings other than supplies and gold.
collectSocial = True  # automatically aid other people and accept friend requests.
doZoomOut = False  # automatically zoom out
collectGuild = True  # collect guild if full
rebootExpired = True  # reboot if session expired
doSwitchScreens = True  # switch virtual screens to another accounts
numberOfDesktops = 5  # number of virtual desktop screens
minimumTimeOnDesktop = 120  # minimum amount of time to spend on one desktop, sec

# One might need to change these based on screen resolution
ydiff1 = 55
ydiff2 = -20

pyautogui.FAILSAFE = True
lock = threading.RLock()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def processOutput(output):
    # get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    # goto coordinates and click there
    lockControl()
    pyautogui.moveTo(xcoord, ycoord + ydiff1, duration=randDur())
    pyautogui.click()
    pressEsc()
    pyautogui.moveRel(0, ydiff2, duration=randDur())
    pyautogui.click()
    logging.debug("Bot has collected something from a building.")
    pressEsc()
    unlockControl()


def randSleepMs(fromMs=220, toMs=550):
    checkIfPaused()
    sleep(randint(fromMs, toMs) / 1000)


def randSleepSec(fromSec=1, toSec=3):
    checkIfPaused()
    secs = randint(fromSec, toSec)
    logging.debug("Sleeping for %s secs.", secs)
    sleep(secs)


def randDur(): return randint(150, 750) / 1000


def processIdleOutput(output):
    # get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    ycoord += ydiff1
    # goto coordinates and click there
    lockControl()
    pyautogui.moveTo(xcoord, ycoord, duration=randDur())
    pyautogui.click()
    randSleepMs()
    pyautogui.typewrite(['1', '2', '3', '4', '5'])
    logging.debug("Bot has restarted a production building.")
    pressEsc()
    unlockControl()


def unlockControl():
    checkIfPaused()
    lock.release()


def lockControl():
    checkIfPaused()
    lock.acquire()


def checkIfPaused():
    while kb.is_pressed("ctrl"):
        sleep(1)


def pressButton(output, suppressESC):
    if output is None:
        logging.warning("There is no button")
        return
    lockControl()
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
    unlockControl()


def scroll(clicks=0, delta_x=0, delta_y=0, delay_between_ticks=0):
    """
    Source: https://docs.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-mouse_event?redirectedfrom=MSDN

    void mouse_event(
      DWORD     dwFlags,
      DWORD     dx,
      DWORD     dy,
      DWORD     dwData,
      ULONG_PTR dwExtraInfo
    );

    If dwFlags contains MOUSEEVENTF_WHEEL,
    then dwData specifies the amount of wheel movement.
    A positive value indicates that the wheel was rotated forward, away from the user;
    A negative value indicates that the wheel was rotated backward, toward the user.
    One wheel click is defined as WHEEL_DELTA, which is 120.

    :param delay_between_ticks:
    :param delta_y:
    :param delta_x:
    :param clicks:
    :return:
    """

    if clicks > 0:
        increment = win32con.WHEEL_DELTA
    else:
        increment = win32con.WHEEL_DELTA * -1

    for _ in range(abs(clicks)):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, delta_x, delta_y,
                             increment, 0)
        time.sleep(delay_between_ticks)


def pressEsc():
    checkIfPaused()
    randSleepMs()
    pyautogui.typewrite(['esc'])


def goldCollector():  # gold icons
    while True:
        output = findGold()

        if output is not None:
            logging.info("Found gold %s", output)
            processOutput(output)
        else:
            randSleepSec(1, 3)


def findGold():
    return findPic('gold1', confidence=0.905) \
           or findPic('gold2', confidence=0.895) \
           or findPic('gold3', confidence=0.895) \
           or findPic('gold4', confidence=0.795)


def processArmy():
    while True:
        output = findArmy()
        if output is not None:
            logging.info("Found army %s", output)
            processOutput(output)
        randSleepSec(5, 10)


def findArmy():
    return findPic("army", confidence=0.905) or findPic("army2", confidence=0.805)


def processSupplies():  # supplies icons
    while True:
        if not isThereSomethingToCollect():
            randSleepSec(3, 7)
            continue

        output = findSupplies()
        if output is not None:
            logging.info("Found supplies %s", output)
            processOutput(output)
        else:
            randSleepSec(3, 7)


def findSupplies():
    return findPic('supplies1', confidence=0.705) \
           or findPic('supplies2', confidence=0.720) \
           or findPic('supplies3', confidence=0.720) \
           or findPic('supplies4', confidence=0.720)


def processIdleBuildings():  # idle building icons
    while True:
        output = findIdle()
        if output is not None:
            logging.info("Found idle %s", output)
            processIdleOutput(output)
        else:
            randSleepSec(3, 7)


def findIdle():
    return findPic('idle1', confidence=0.545) \
           or findPic('idle2', confidence=0.545) \
           or findPic('idle3', confidence=0.545)


def processGoods():  # goods boxes icons
    while True:
        output = findGoods()
        if output is not None:
            logging.info("Found good %s", output)
            processIdleOutput(output)
        else:
            randSleepSec(3, 7)


def findGoods():
    return findPic('goods1', confidence=0.885) \
           or findPic('goods2', confidence=0.685) \
           or findPic('goods3', confidence=0.685)


socialProcesses = []


def processSocial():
    while True:
        global socialProcesses
        initSocialProcesses()
        random.shuffle(socialProcesses)
        while socialProcesses:
            process = socialProcesses.pop()
            process()
        randSleepSec(300, 600)


def initSocialProcesses():
    global socialProcesses
    # socialProcesses = [processFriends, processNeighbours, processSoguildians]
    socialProcesses = [processNeighbours, processSoguildians]


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
    pressButton(findFullFf(), True)
    while pages >= 0:
        pages = pages - 1
        processSocialPage()
        nextPage()


def nextPage():
    output = findPic('next', confidence=0.800)
    pressButton(output, True)
    randSleepMs()


def findTavern(): return findPic('tavern')


def processSocialPage():
    output = True
    while output is not None:
        output = findAnySocialButton()
        if output is not None:
            logging.info("Precessing social button")
            pressButton(output, True)


def findAnySocialButton():
    return findHelp() or findAccept() or findTavern()


def findFullFf(): return findPic('full-ff', 0.9)


def findAccept(): return findPic('accept', 0.9)


def findToCollect(): return findPic('toCollect', 0.95)


def isThereSomethingToCollect():
    result = findToCollect() is not None
    logging.debug("isThereSomethingToCollect: %s", result)
    return result


def findFriends(): return findPic('friends', 0.9) \
                          or findPic('friendsActive', 0.9)


def findSoguildians(): return findPic('soguildians', 0.9) \
                              or findPic('soguldiansActive', 0.9)


def findNeighbours(): return findPic('neighbors', 0.9) \
                             or findPic('neighborsActive', 0.9)


def findHelp(): return findPic('help', 0.9)


def findButtonsPanel(): return findPic('buttonsPanel', 0.9)


def findLandscape(): return findPic('landscape', 0.9)


def findGuild(): return findPic('guild')


def findPic(picture, confidence=0.800):
    checkIfPaused()
    button = pyautogui.locateOnScreen("resources/" + picture + ".png", confidence=confidence,
                                      grayscale=True)
    logging.debug("Button %s found: %s", picture, button is not None)
    return button


def zoomOut():
    while True:
        if findLandscape() is not None:
            randSleepSec(60, 120)
            return
        panel = findButtonsPanel()
        if panel is None:
            randSleepSec(5, 10)
            return
        lockControl()
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
        unlockControl()


def processGuild():
    while True:

        guild = findGuild()
        if guild is None:
            randSleepSec(60, 120)
            return
        else:
            pressEsc()
        lockControl()
        x = guild.left
        y = guild.top + guild.height + 1
        leftRegion = (x + 3, y, 8, 7)
        rightRegion = (x + guild.width / 2 + 2, y, 8, 7)
        leftScreen = pyautogui.screenshot(region=leftRegion)
        rightScreen = pyautogui.screenshot(region=rightRegion)
        found = pyautogui.locate(leftScreen, rightScreen, confidence=0.9)
        unlockControl()
        if found:
            lockControl()
            logging.info("Found full guild")
            pyautogui.moveTo(guild.left, guild.top + guild.height + ydiff1, duration=randDur())
            pyautogui.click()
            randSleepSec(1, 3)
            unlockControl()
            pressButton(findPic('guildGet'), False)
        else:
            logging.debug("Guild is not full")
            pressEsc()
        randSleepSec(60, 180)


def unstuck():
    while True:
        if findPic('sessionExpired') is not None:
            pressButton(findPic('rebootNow'), True)
            randSleepSec(5, 10)

        playBtn = findPic('play')
        if playBtn is not None:
            pressButton(playBtn, True)
            randSleepSec(5, 10)

        worldBtn = findPic('world')
        if worldBtn is not None:
            pressButton(worldBtn, True)
            randSleepSec(5, 10)

        eventsPanel = findPic('events')
        if eventsPanel is not None:
            pressEsc()
            randSleepSec(5, 10)

        if findPic('visitUnavailable') is not None:
            pressButton(findPic('ok'), True)

        randSleepSec(1, 3)


currentDesktop = 2


def leftDesktop():
    global currentDesktop
    currentDesktop = currentDesktop - 1
    pyautogui.hotkey('ctrl', 'win', 'left')
    randSleepMs()


def rightDesktop():
    global currentDesktop
    currentDesktop = currentDesktop + 1
    pyautogui.hotkey('ctrl', 'win', 'right')
    randSleepMs()


def moveToFirstDesktop():
    global currentDesktop
    lockControl()
    for i in range(0, numberOfDesktops):
        leftDesktop()
        randSleepMs()
    rightDesktop()
    currentDesktop = 2
    unlockControl()


moveToFirstDesktop()


def switchScreens():
    start = time.time()
    while True:
        if time.time() - start > minimumTimeOnDesktop:
            start = time.time()
            initSocialProcesses()
            if currentDesktop == numberOfDesktops:
                moveToFirstDesktop()
            else:
                lockControl()
                rightDesktop()
                unlockControl()


def startBot(botFunction, toggle):
    if toggle:
        threading.Thread(name=botFunction.__name__, target=botFunction).start()


startBot(goldCollector, collectGold)
startBot(processSupplies, collectSupplies)
startBot(processIdleBuildings, restartIdleBuildings)
startBot(processGoods, collectGoods)
startBot(processSocial, collectSocial)
startBot(processArmy, collectArmy)
startBot(zoomOut, doZoomOut)
startBot(processGuild, collectGuild)
startBot(unstuck, rebootExpired)
startBot(switchScreens, doSwitchScreens)
