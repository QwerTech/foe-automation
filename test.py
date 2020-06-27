import unittest

import foe_desktops
from foe_pics import *

root = 'testresources/'


def f(x):
    return x * x


def findPic(o):
    return pyautogui.locate(o.picture, o.screenshot, confidence=0.8, grayscale=True)


class Task():

    def __init__(self, picture, screenshot):
        self.picture = picture
        self.screenshot = screenshot


class MyTestCase(unittest.TestCase):

    def test_something(self):
        windows = foe_desktops.getGameWindows()
        for window in windows:
            pass


if __name__ == '__main__':
    unittest.main()
