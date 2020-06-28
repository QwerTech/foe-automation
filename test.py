import unittest
from time import sleep

from foe_pics import *
from foe_utils import lock

root = 'testresources/'


def f(x):
    return x * x


def findPic(o):
    return pyautogui.locate(o.picture, o.screenshot, confidence=0.8, grayscale=True)


class Task():

    def __init__(self, picture, screenshot):
        self.picture = picture
        self.screenshot = screenshot


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)s:%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
class MyTestCase(unittest.TestCase):

    def test_something(self):
        with lock:
            sleep(2)


if __name__ == '__main__':
    unittest.main()
