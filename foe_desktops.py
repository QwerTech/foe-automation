from time import sleep

import pyautogui
import pygetwindow as gw

currentDesktop = 1
numberOfDesktops = 2  # number of virtual desktop screens


def leftDesktop():
    global currentDesktop
    currentDesktop = currentDesktop - 1
    pyautogui.hotkey('ctrl', 'win', 'left')
    sleep(0.5)


def rightDesktop():
    global currentDesktop
    currentDesktop = currentDesktop + 1
    pyautogui.hotkey('ctrl', 'win', 'right')
    sleep(0.5)


def moveToFirstDesktop():
    global currentDesktop
    for i in range(0, numberOfDesktops - 1):
        leftDesktop()
    rightDesktop()
    currentDesktop = 1


def trySkip(func):
    try:
        func()
    except Exception as e:
        print(e)
        pass


def hideAll():
    pyautogui.hotkey('win', 'd')
    for window in getGameWindows():
        hide(window)


def show(window):
    if not window.isMaximized:
        window.maximize()
    if not window.isActive:
        trySkip(lambda: window.activate())


def hide(window):
    window.minimize()


def getGameWindows():
    return gw.getWindowsWithTitle('forge of empires')


if __name__ == '__main__':
    pass
