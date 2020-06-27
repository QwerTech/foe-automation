import glob
from pathlib import Path

from foe_control import pressButton, pressEsc, right, up, left, down
from foe_pics import findRewardReceived, findUpRightCorner, findDownRightCorner, \
    findDownLeftCorner, findUpLeftCorner, findCoastOnTheRight, findPic
from foe_pool import execInPool
from foe_utils import waitFor, lock, randSleepSec, checkIfPaused


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
    randSleepSec(90, 180)
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


def moveTo(move, findFunc):
    maxIterations = 26

    while findFunc() is None and maxIterations > 0:
        checkIfPaused()
        move()
        maxIterations = maxIterations - 1


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
