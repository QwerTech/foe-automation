import logging

import pyautogui


def findAnySocialButton():
    return findHelp() or findAccept() or findTavern()


def findFullFf(): return findPic('full-ff', 0.9)


def findArmy():
    return findPic("army", confidence=0.905) or findPic("army2", confidence=0.805)


def findGold():
    return findPic('gold1', confidence=0.905) \
           or findPic('gold2', confidence=0.895) \
           or findPic('gold3', confidence=0.895) \
           or findPic('gold4', confidence=0.795)


def findGoods():
    return findPic('goods1', confidence=0.885) \
           or findPic('goods2', confidence=0.685) \
           or findPic('goods3', confidence=0.685)


def findIdle():
    return findPic('idle1', confidence=0.545) \
           or findPic('idle2', confidence=0.545) \
           or findPic('idle3', confidence=0.545)


def findSupplies():
    return findPic('supplies1', confidence=0.705) \
           or findPic('supplies2', confidence=0.720) \
           or findPic('supplies3', confidence=0.720) \
           or findPic('supplies4', confidence=0.720)


def findTavern(): return findPic('tavern')


def findAccept(): return findPic('accept')


def findToCollect(): return findPic('toCollect', 0.95)


def findFriends(): return findPic('friends', 0.9) \
                          or findPic('friendsActive', 0.9)


def findSoguildians(): return findPic('soguildians', 0.9) \
                              or findPic('soguldiansActive', 0.9)


def findNeighbours(): return findPic('neighbors', 0.9) \
                             or findPic('neighborsActive', 0.9)


def findHelp(): return findPic('help')


def findButtonsPanel(): return findPic('buttonsPanel', 0.9)


def findLandscape(): return findPic('landscape', 0.9)


def findGuild(): return findPic('guild')


def findPic(picture, confidence=0.800):
    button = pyautogui.locateOnScreen("resources/" + picture + ".png", confidence=confidence,
                                      grayscale=True)
    logging.debug("Button %s found: %s", picture, button is not None)
    return button


def findNext():
    return findPic('next')
