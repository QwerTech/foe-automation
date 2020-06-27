import logging

import pyautogui


def findAnySocialButton():
    return findHelp() or findAccept() or findTavern()


def findFullFf(): return findPic('full-ff', 0.9)


def findArmy():
    return findPic("army", confidence=0.905) or findPic("army2", confidence=0.805)


def findGold():
    return findPic('gold1', confidence=0.905) \
           or findPic('goldStar', confidence=0.805) \
           or findPic('gold2', confidence=0.895) \
           or findPic('gold3', confidence=0.895) \
           or findPic('gold4', confidence=0.795)


def findGoldCollected(region):
    return findPic('goldCollected', confidence=0.905, region=region)


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


def findSuppliesCollected(region):
    return findPic('suppliesCollected', confidence=0.805, region=region)


def findTavern(): return findPic('tavern')


def findAccept(): return findPic('accept')


def findToCollect(): return findPic('toCollect', 0.95)


def findSomethingSleeps(): return findPic('somethingSleeps', 0.95)


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


def findUpLeftCorner(): return findPic('upLeftCorner')


def findCoastOnTheRight(): return findPic('coastOnTheRight')


def findUpRightCorner(): return findPic('rightUp')


def findDownLeftCorner(): return findPic('downLeft')


def findDownRightCorner(): return findPic('downRight')


def findPic(picture, confidence=0.800, region=None):
    if region is None:
        button = pyautogui.locateOnScreen("resources/" + picture + ".png", confidence=confidence, grayscale=True)
    else:
        # pyautogui.screenshot(region=region, imageFilename="screenshot.png")
        button = pyautogui.locateOnScreen("resources/" + picture + ".png", confidence=confidence, grayscale=True,
                                          region=region)
    logging.debug("Button %s found: %s", picture, button is not None)
    return button


def findNext():
    return findPic('next')


def findRewardReceived():
    return findPic("rewardReceived")
