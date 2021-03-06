from time import sleep

import pyautogui
import pygetwindow as gw

from foe_utils import lock, checkIfPaused, randSleepMs

currentDesktop = 1
numberOfDesktops = 2  # number of virtual desktop screens


def _leftDesktop():
    global currentDesktop
    currentDesktop = currentDesktop - 1
    pyautogui.hotkey('ctrl', 'win', 'left')
    sleep(0.5)


def _rightDesktop():
    global currentDesktop
    currentDesktop = currentDesktop + 1
    pyautogui.hotkey('ctrl', 'win', 'right')
    sleep(0.5)


def _moveToFirstDesktop():
    global currentDesktop
    for i in range(0, numberOfDesktops - 1):
        leftDesktop()
    rightDesktop()
    currentDesktop = 1


def leftDesktop():
    with lock:
        checkIfPaused()
        _leftDesktop()


def rightDesktop():
    with lock:
        checkIfPaused()
        _rightDesktop()


def moveToFirstDesktop():
    with lock:
        checkIfPaused()
        _moveToFirstDesktop()


def trySkip(func):
    try:
        func()
    except Exception as e:
        print(e)
        pass


def hideAll():
    pyautogui.hotkey('win', 'd')
    randSleepMs()
    for window in getGameWindows():
        hide(window)


def show(window):
    if not window.isMaximized:
        window.maximize()
        randSleepMs()
    if not window.isActive:
        trySkip(lambda: activate(window))


def activate(window):
    window.activate()
    randSleepMs()


def hide(window):
    if not window.isMinimized:
        window.minimize()
        randSleepMs()


def getGameWindows():
    return gw.getWindowsWithTitle('forge of empires')


if __name__ == '__main__':
    pass
