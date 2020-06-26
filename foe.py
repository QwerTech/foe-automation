from __future__ import annotations

import glob
import itertools
import threading
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

import keyboard as kb
# functions to be run, you can change these!
from waiting import wait

import foe_desktops
from foe_bot_army import processArmy
from foe_bot_gold import goldCollector
from foe_bot_goods import processGoods
from foe_bot_idle import processIdleBuildings
from foe_bot_social import initSocialProcesses, processSocial
from foe_bot_zoom import zoomOut
from foe_control import pressCollect1, pressCollect2, ydiff1, ydiff2, pressEsc, \
    pressButton
from foe_pics import *
from foe_pics import findRewardReceived
from foe_pool import execInPool, initPool
from foe_utils import waitFor, randDur, checkIfPaused, \
    randSleepSec, lock

collectGold = True  # collect gold from buildings.
collectArmy = True  # collect gold from buildings.
collectSupplies = True  # collect supplies from buildings.
restartIdleBuildings = True  # restart any idle building.
collectGoods = True  # collect goods from buildings other than supplies and gold.
collectSocial = True  # automatically aid other people and accept friend requests.
doZoomOut = True  # automatically zoom out
collectGuild = True  # collect guild if full
doUnstuck = True  # reboot if session expired
doSwitchBots = True  # switch virtual screens to another accounts
rebootSomeTime = True  # reboot game some times
doCollectLoot2 = True  # collect in-game loot

minimumTimeOnDesktop = 120  # minimum amount of time to spend on one desktop, sec

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


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
    for i in range(1, foe_desktops.numberOfDesktops):
        GameState.games.append(GameState())


initGamesState()


def waitSuppliesCollected(left, top):
    region = [left - 20, top - 70, 70, 80]
    if waitFor(lambda: findSuppliesCollected(region)):
        logging.debug("Bot has collected supplies something from a building.")
        return True
    else:
        return False


def waitIdleOpened(left, top):  # todo
    region = [left - 20, top - 70, 70, 80]
    if waitFor(lambda: findSuppliesCollected(region)):
        logging.debug("Bot has collected supplies something from a building.")
        return True
    else:
        return False


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


socialProcesses = []


def isThereSomethingToCollect():
    result = findToCollect() is not None
    logging.debug("isThereSomethingToCollect: %s", result)
    return result


def processGuild():
    guild = findGuild()
    if guild is None:
        randSleepSec(60, 120)
        return
    else:
        pressEsc()
    with lock:
        checkIfPaused()
        x = guild.left
        y = guild.top + guild.height + 1
        leftRegion = (x + 3, y, 8, 7)
        rightRegion = (x + guild.width / 2 + 2, y, 8, 7)
        leftScreen = pyautogui.screenshot(region=leftRegion)
        rightScreen = pyautogui.screenshot(region=rightRegion)
        found = pyautogui.locate(leftScreen, rightScreen, confidence=0.8)
        if found:
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
        else:
            logging.debug("Guild is not full")
            pressEsc()
    randSleepSec(60, 180)


def reboot():
    with lock:
        checkIfPaused()
        activateWindow()
        pyautogui.press('f5')
        GameState.rebooted()
        sleep(1)


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
    with lock:
        checkIfPaused()
        foe_desktops.leftDesktop()


def rightDesktop():
    with lock:
        checkIfPaused()
        foe_desktops.rightDesktop()


def moveToFirstDesktop():
    with lock:
        checkIfPaused()
        foe_desktops.moveToFirstDesktop()


def switchBots():
    windows = foe_desktops.getGameWindows()
    foe_desktops.hideAll()
    for window in itertools.cycle(windows):
        with lock:
            checkIfPaused()
            foe_desktops.show(window)
            initSocialProcesses()
        sleep(minimumTimeOnDesktop)
        with lock:
            foe_desktops.hide(window)


def startBot(botFunction, toggle):
    if toggle:
        botName = botFunction.__name__
        logging.info("Starting bot " + botName)
        thread = threading.Thread(name=botName, target=safeInfiniteLoop,
                                  args=(botFunction,))
        thread.setDaemon(True)
        thread.start()
        return thread


def rebooter():
    wait(GameState.needToReboot)
    reboot()


def collectLoot():
    loot = findLoot()
    while loot is not None:
        if loot is None:
            return
        pressButton(loot, False)
        waitFor(findRewardReceived, 10)
        pressEsc()
        loot = findLoot()


def lootCollector2():
    with lock:
        moveTo(lambda: right() or up(), findUpRightCorner)
        collectLoot()
        moveTo(lambda: right() or down(), findDownRightCorner)
        collectLoot()
        moveTo(lambda: left() or down(), findDownLeftCorner)
        collectLoot()
        moveTo(lambda: left() or up(), findUpLeftCorner)
        collectLoot()
        moveTo(lambda: right(), findCoastOnTheRight)
    randSleepSec(90, 180)


def moveTo(move, findFunc):
    maxIterations = 26

    while findFunc() is None and maxIterations > 0:
        checkIfPaused()
        move()
        maxIterations = maxIterations - 1


def left(): pressDelayed('left')


def down(): pressDelayed('down')


def up(): pressDelayed('up')


def right(): pressDelayed('right')


def pressDelayed(key: str, delay=0.1):
    pyautogui.keyDown(key)
    sleep(delay)
    pyautogui.keyUp(key)


def findLoot():
    pics = []
    for file in glob.glob("resources/loot/*.png"):
        name = Path(file).stem
        pic = f"loot/{name}"
        pics.append(pic)
    for i in range(0, 3):
        found = execInPool(findPic, pics)
        found = [pic for pic in found if pic is not None]
        if found:
            return found[0]
        randSleepSec()


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if doSwitchBots:
        moveToFirstDesktop()

    startBot(goldCollector, collectGold)
    startBot(processSupplies, collectSupplies)
    startBot(processIdleBuildings, restartIdleBuildings)
    startBot(processGoods, collectGoods)
    startBot(processSocial, collectSocial)
    startBot(processArmy, collectArmy)
    startBot(zoomOut, doZoomOut)
    startBot(processGuild, collectGuild)
    startBot(unstuck, doUnstuck)
    startBot(switchBots, doSwitchBots)
    startBot(rebooter, rebootSomeTime)
    initPool()
    startBot(lootCollector2, doCollectLoot2)
    while not kb.is_pressed('end'):
        sleep(1)

    logging.info("Bye!")
