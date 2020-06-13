from __future__ import annotations

import glob
import random
import threading
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from time import sleep

import keyboard as kb
import win32api
import win32con
# functions to be run, you can change these!
from waiting import wait, TimeoutExpired

from foe_images import *
from foe_pics import *

collectGold = True  # collect gold from buildings.
collectArmy = True  # collect gold from buildings.
collectSupplies = True  # collect supplies from buildings.
restartIdleBuildings = True  # restart any idle building.
collectGoods = True  # collect goods from buildings other than supplies and gold.
collectSocial = True  # automatically aid other people and accept friend requests.
doZoomOut = True  # automatically zoom out
collectGuild = True  # collect guild if full
doUnstuck = True  # reboot if session expired
doSwitchScreens = False  # switch virtual screens to another accounts
rebootSomeTime = True  # reboot game some times
doCollectLoot = True  # collect in-game loot

numberOfDesktops = 5  # number of virtual desktop screens
minimumTimeOnDesktop = 60  # minimum amount of time to spend on one desktop, sec

# One might need to change these based on screen resolution
ydiff1 = 60
ydiff2 = -25

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
lock = threading.RLock()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class GameState:
    games = []

    def __init__(self):
        self.lastRebooted = datetime.now()

    @classmethod
    def needToReboot(cls) -> bool:
        game_state = cls.getCurrentGameState()
        if game_state is None:
            return False
        return game_state.lastRebooted + timedelta(hours=1) < datetime.now()

    @classmethod
    def getCurrentGameState(cls) -> GameState:
        global currentDesktop
        if currentDesktop == 0 or currentDesktop > len(cls.games) - 1:
            return None
        return cls.games[currentDesktop]

    @classmethod
    def rebooted(cls):
        game_state = cls.getCurrentGameState()
        if game_state is None:
            return
        game_state.lastRebooted = datetime.now()


def initGamesState():
    for i in range(1, numberOfDesktops):
        GameState.games.append(GameState())


initGamesState()


def processOutput(output):
    lockControl()
    # get coordinates to click from output
    pressCollect1(output)
    pressEsc()
    pressCollect2(output)
    logging.debug("Bot has collected something from a building.")
    pressEsc()
    unlockControl()


def pressCollect1(output):
    # goto coordinates and click there
    moveAndClick(output.left, output.top + ydiff1)


def pressCollect2(output):
    # goto coordinates and click there
    moveAndClick(output.left, output.top + ydiff1 + ydiff2)


def moveAndClick(left, top):
    pyautogui.moveTo(left, top, duration=randDur())
    pyautogui.click()


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
    lockControl()
    pressCollect1(output)
    randSleepMs()
    pyautogui.typewrite(['1', '2', '3', '4', '5'])
    pressCollect2(output)
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
    while kb.is_pressed("ctrl"):  # or GetKeyState(VK_SCROLL) == 1:
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
    output = findGold()

    if output is not None:
        logging.info("Found gold %s", output)
        lockControl()
        # get coordinates to click from output
        pressCollect1(output)
        if waitGoldCollected(output.left, output.top + ydiff1):
            return

        pressEsc()
        pressCollect2(output)
        if waitGoldCollected(output.left, output.top + ydiff1 + ydiff2):
            return

        pressEsc()
        unlockControl()
    else:
        randSleepSec(5, 15)


def waitGoldCollected(left, top):
    region = [left - 10, top - 70, 50, 80]
    if waitCollected(lambda: findGoldCollected(region)):
        logging.debug("Bot has collected gold something from a building.")
        return True
    else:
        return False


def waitSuppliesCollected(left, top):
    region = [left - 20, top - 70, 70, 80]
    if waitCollected(lambda: findSuppliesCollected(region)):
        logging.debug("Bot has collected supplies something from a building.")
        return True
    else:
        return False


def waitCollected(findPicFunc):
    try:
        wait(lambda: findPicFunc() is not None, timeout_seconds=0.5, sleep_seconds=0)

        return True
    except TimeoutExpired:
        return False


def processArmy():
    output = findArmy()
    if output is not None:
        logging.info("Found army %s", output)
        processOutput(output)
    randSleepSec(5, 10)


def processSupplies():  # supplies icons
    output = findSupplies()
    if output is not None:
        logging.info("Found supplies %s", output)
        lockControl()
        # get coordinates to click from output
        pressCollect1(output)
        if waitSuppliesCollected(output.left, output.top + ydiff1):
            return

        pressEsc()
        pressCollect2(output)
        if waitSuppliesCollected(output.left, output.top + ydiff1 + ydiff2):
            return

        pressEsc()
        unlockControl()
    else:
        randSleepSec(3, 7)


def processIdleBuildings():  # idle building icons
    output = findIdle()
    if output is not None:
        logging.info("Found idle %s", output)
        processIdleOutput(output)
    else:
        randSleepSec(3, 7)


def processGoods():  # goods boxes icons
    output = findGoods()
    if output is not None:
        logging.info("Found good %s", output)
        processIdleOutput(output)
    else:
        randSleepSec(3, 7)


socialProcesses = []


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


def isThereSomethingToCollect():
    result = findToCollect() is not None
    logging.debug("isThereSomethingToCollect: %s", result)
    return result


def zoomOut():
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
    found = pyautogui.locate(leftScreen, rightScreen, confidence=0.8)
    unlockControl()
    if found:
        lockControl()
        logging.info("Found full guild")
        pyautogui.moveTo(guild.left, guild.top + guild.height + ydiff1,
                         duration=randDur())
        pyautogui.click()
        guildGet = findPic('guildGet')
        tries = 10
        while guildGet is None and tries > 0:
            tries = tries - 1
            randSleepSec(1, 3)
            guildGet = findPic('guildGet')
        pressButton(guildGet, False)
        unlockControl()
    else:
        logging.debug("Guild is not full")
        pressEsc()
    randSleepSec(60, 180)


def reboot():
    lockControl()
    activateWindow()
    pyautogui.press('f5')
    GameState.rebooted()
    sleep(1)
    unlockControl()


def activateWindow():
    pyautogui.moveTo(pyautogui.size().width / 2, 15)
    pyautogui.click()


def unstuck():
    if findPic('sessionExpired') is not None:
        pressButton(findPic('rebootNow'), True)
        randSleepSec(5, 10)

    playBtn = findPic('play')
    if playBtn is not None:
        pressButton(playBtn, True)

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

    returnToCity = findPic('returnToCity')
    if returnToCity is not None:
        pressButton(returnToCity, False)

    if findPic('cannotHelp') is not None:
        reboot()

    randSleepSec(5, 15)


currentDesktop = 1


def leftDesktop():
    global currentDesktop
    lockControl()
    currentDesktop = currentDesktop - 1
    pyautogui.hotkey('ctrl', 'win', 'left')
    randSleepMs(500, 500)
    unlockControl()


def rightDesktop():
    global currentDesktop
    lockControl()
    currentDesktop = currentDesktop + 1
    pyautogui.hotkey('ctrl', 'win', 'right')
    randSleepMs(500, 500)
    unlockControl()


def moveToFirstDesktop():
    global currentDesktop
    lockControl()
    for i in range(0, numberOfDesktops - 1):
        leftDesktop()
    rightDesktop()
    currentDesktop = 1
    unlockControl()


if doSwitchScreens:
    moveToFirstDesktop()

start = time.time()


def switchScreens():
    global start
    if time.time() - start > minimumTimeOnDesktop:
        lockControl()
        start = time.time()
        initSocialProcesses()
        if currentDesktop == numberOfDesktops - 1:
            moveToFirstDesktop()
        else:
            rightDesktop()
        unlockControl()


def startBot(botFunction, toggle):
    if toggle:
        botName = botFunction.__name__
        logging.info("Starting bot " + botName)
        threading.Thread(name=botName, target=safeInfiniteLoopFactory(botFunction)).start()


def rebooter():
    wait(GameState.needToReboot)
    reboot()


def lootCollector():
    loot = findLoot()
    if loot is None:
        randSleepSec(300, 600)
        # randSleepMs()
        return
    pressButton(loot, False)
    try:
        wait(lambda: findPic("rewardReceived") is not None, timeout_seconds=10, sleep_seconds=0.5)
    except TimeoutExpired:
        pass
    pressEsc()


def findLoot():
    # for i in range(0, 10):
    randSleepSec()
    for file in glob.glob("resources/loot/*.png"):
        name = Path(file).stem
        pic = findPic(f"loot/{name}")
        if pic is not None:
            return pic
        randSleepMs()


def safeInfiniteLoopFactory(func):
    return lambda: safeInfiniteLoop(func)


def safeInfiniteLoop(func):
    while True:
        try:
            logging.info("Bot iteration")
            checkIfPaused()
            func()
        except Exception as e:
            logging.error(traceback.format_exc())
            logging.error(e)


startBot(goldCollector, collectGold)
startBot(processSupplies, collectSupplies)
startBot(processIdleBuildings, restartIdleBuildings)
startBot(processGoods, collectGoods)
startBot(processSocial, collectSocial)
startBot(processArmy, collectArmy)
startBot(zoomOut, doZoomOut)
startBot(processGuild, collectGuild)
startBot(unstuck, doUnstuck)
startBot(switchScreens, doSwitchScreens)
startBot(rebooter, rebootSomeTime)

startBot(lootCollector, doCollectLoot)