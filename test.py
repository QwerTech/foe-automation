import itertools
import unittest

from PIL import Image

from foe_images import *
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
        cycle = itertools.cycle([1, 2, 3, 4])
        print(cycle)

    @unittest.skip
    def test_image_compare(self):
        initial = Image.open(root + 'friends1.png')
        second = Image.open(root + 'friends2.png')
        sameAsInitial = Image.open(root + 'friends3.png')
        completelyDifferent = Image.open(root + 'landscape.png')

        rms = getRms(initial, initial)
        i = compare(initial, initial)
        rmsdiff__ = rmsdiff_1997(initial, initial)
        similar = images_are_similar(initial, initial)

        rms0 = getRms(initial, second)
        i0 = compare(initial, second)
        rmsdiff__0 = rmsdiff_1997(initial, second)
        similar0 = images_are_similar(initial, second)

        rms1 = getRms(initial, sameAsInitial)
        i1 = compare(initial, sameAsInitial)
        rmsdiff__1 = rmsdiff_1997(initial, sameAsInitial)
        similar1 = images_are_similar(initial, sameAsInitial)

        rms2 = getRms(second, sameAsInitial)
        i2 = compare(second, sameAsInitial)
        rmsdiff__2 = rmsdiff_1997(second, sameAsInitial)
        similar2 = images_are_similar(second, sameAsInitial)

        rms3 = getRms(initial, completelyDifferent)
        i3 = compare(initial, completelyDifferent)
        rmsdiff__3 = rmsdiff_1997(initial, completelyDifferent)
        similar3 = images_are_similar(initial, completelyDifferent)
        comparator = lambda img1, img2: getRms(img1, img2)
        self.assertTrue(same(initial, sameAsInitial))
        self.assertFalse(same(initial, second))
        self.assertFalse(same(initial, completelyDifferent))
        self.assertTrue(same(sameAsInitial, initial))
        self.assertFalse(same(second, completelyDifferent))


if __name__ == '__main__':
    unittest.main()
