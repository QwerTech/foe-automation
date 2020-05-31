import logging
import random
import threading
import time
from random import randint
from time import sleep

import pyautogui
import win32api
import win32con

# opencv-python is required! (pip install opencv-python).

# functions to be run, you can change these!
collectGold = True  # collect gold from buildings.
collectArmy = True  # collect gold from buildings.
collectSupplies = True  # collect supplies from buildings.
restartIdleBuildings = True  # restart any idle building.
collectGoods = True  # collect goods from buildings other than supplies and gold.
collectSocial = True  # automatically aid other people and accept friend requests.
doZoomOut = True  # automatically zoom out

# One might need to change these based on screen resolution
ydiff1 = 25
ydiff2 = 50

pyautogui.FAILSAFE = True
lock = threading.Lock()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def processOutput(output):
    # get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    # goto coordinates and click there
    lock.acquire()
    pyautogui.moveTo(xcoord, ycoord, duration=randDur())
    randSleepMs()
    pyautogui.moveRel(0, ydiff1, duration=randint(5, 15) / 20)
    randSleepMs()
    pyautogui.click()
    print("Bot has collected something from a building.")
    randSleepMs()
    pressEsc()
    pressEsc()
    pressEsc()
    lock.release()


def randSleepMs(fromMs=120, toMs=250):  sleep(randint(fromMs, toMs) / 1000)


def randSleepSec(fromSec=1, toSec=3):
    secs = randint(fromSec, toSec)
    logging.debug("Seeping for %s secs.", secs)
    sleep(secs)


def randDur(): return randint(5, 15) / 10


def processIdleOutput(output):
    # get coordinates to click from output
    xcoord = int(output[0])
    ycoord = int(output[1])
    ycoord += ydiff1
    # goto coordinates and click there
    lock.acquire()
    pyautogui.moveTo(xcoord, ycoord, duration=randint(5, 15) / 10)
    sleep(randint(12, 25) / 100)
    pyautogui.click()
    sleep(randint(70, 90) / 100)
    pyautogui.typewrite(['1', '2', '3', '4', '5'])
    print("Bot has restarted a production building.")
    sleep(randint(80, 100) / 100)
    pressEsc()
    lock.release()


def processButtonOutput(output, suppressESC):
    if output is None:
        logging.warning("There is no button")
        return
    lock.acquire()
    # get coordinates to click from output
    xcoord, ycoord, xcoord2, ycoord2 = output
    # goto coordinates and click there
    pyautogui.moveTo(randint(xcoord + 1, xcoord + xcoord2 - 1),
                     randint(ycoord + 1, ycoord + ycoord2 - 1),
                     duration=randint(2, 7) / 10)
    # sleep(randint(12, 25) / 100)
    pyautogui.click()
    logging.info("Bot has clicked a button.")
    if not suppressESC:
        pressEsc()
    lock.release()


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
    sleep(randint(80, 100) / 100)
    pyautogui.typewrite(['esc'])


def goldCollector():  # gold icons
    while True:
        output = findButton('gold1', confidence=0.905) \
                 or findButton('gold2', confidence=0.895)

        if output is not None:
            processOutput(output)
        else:
            randSleepSec(1, 3)


def processArmy():
    while True:
        output = findButton("army", confidence=0.905)
        if output is not None:
            processOutput(output)
        randSleepSec(5, 10)


def processSupplies():  # supplies icons
    while True:
        output = findButton('supplies1', confidence=0.805) \
                 or findButton('supplies2', confidence=0.820)
        if output is not None:
            processOutput(output)
        else:
            randSleepSec(3, 7)


def processIdleBuildings():  # idle building icons
    while True:
        output = findButton('idle1', confidence=0.545)
        if output is not None:
            processIdleOutput(output)
        else:
            randSleepSec(3, 7)


def processGoods():  # goods boxes icons
    while True:
        output = findButton('goods1', confidence=0.885)
        if output is not None:
            processIdleOutput(output)
        else:
            randSleepSec(3, 7)


def processSocial():
    while True:
        processes = [processFriends, processNeighbours, processSoguildians]
        random.shuffle(processes)
        for process in processes:
            process()


def processSoguildians():
    processButtonOutput(findSoguildians(), True)
    processAllSocialPages()


def processNeighbours():
    processButtonOutput(findNeighbours(), True)
    processAllSocialPages()


def processFriends():
    processButtonOutput(findFriends(), True)
    processAllSocialPages()


def processAllSocialPages():
    pages = 16
    processButtonOutput(findFullFf(), True)
    while pages >= 0:
        pages = pages - 1
        processSocialPage()
        nextPage()


def nextPage():
    output = findButton('next', confidence=0.800)
    processButtonOutput(output, True)


def findTavern(): return findButton('tavern')


def processSocialPage():
    output = True
    while output is not None:
        output = findAnySocialButton()
        if output is not None:
            processButtonOutput(output, True)


def findAnySocialButton():
    return findHelp() or findAccept() or findTavern()


def findFullFf(): return findButton('full-ff')


def findAccept(): return findButton('accept')


def findFriends(): return findButton('friends') \
                          or findButton('friendsActive')


def findSoguildians(): return findButton('soguildians') \
                              or findButton('soguldiansActive')


def findNeighbours(): return findButton('neighbors') \
                             or findButton('neighborsActive')


def findHelp(): return findButton('help')


def findButtonsPanel(): return findButton('buttonsPanel')


def findLandscape(): return findButton('landscape')


def findButton(picture, confidence=0.800):
    button = pyautogui.locateOnScreen("resources/" + picture + ".png", confidence=confidence,
                                      grayscale=True)
    logging.info("Button %s found: %s", picture, button is not None)
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
        lock.acquire()
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
        lock.release()


# multithreading
if collectGold:
    threading.Thread(name="golder", target=goldCollector).start()

if collectSupplies:
    threading.Thread(name="supplier", target=processSupplies).start()

if restartIdleBuildings:
    threading.Thread(name="idler", target=processIdleBuildings).start()

if collectGoods:
    threading.Thread(name="gooder", target=processGoods).start()

if collectSocial:
    threading.Thread(name="socialer", target=processSocial).start()

if collectArmy:
    threading.Thread(name="armer", target=processArmy).start()

if doZoomOut:
    threading.Thread(name="zoomer", target=zoomOut()).start()
