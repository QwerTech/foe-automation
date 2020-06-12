import math
import operator
from functools import reduce

from PIL import ImageChops
from comtypes.safearray import numpy


def same(img1, img2, error=10):
    return getRms(img1, img2) < error


def getRms(img1, img2):
    h1 = img1.histogram()
    h2 = img2.histogram()
    return math.sqrt(reduce(operator.add, map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))


def rmsdiff_1997(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
                            map(lambda h, i: h * (i ** 2), h, range(256))
                            ) / (float(im1.size[0]) * im1.size[1]))


def compare(img1, img2):
    if img1.size != img2.size or img1.getbands() != img2.getbands():
        return -1

    s = 0
    for band_index, band in enumerate(img1.getbands()):
        m1 = numpy.array([p[band_index] for p in img1.getdata()]).reshape(*img1.size)
        m2 = numpy.array([p[band_index] for p in img2.getdata()]).reshape(*img2.size)
        s += numpy.sum(numpy.abs(m1 - m2))
    return s


def images_are_similar(img1, img2, error=90):
    diff = ImageChops.difference(img1, img2).histogram()
    sq = (value * (i % 256) ** 2 for i, value in enumerate(diff))
    sum_squares = sum(sq)
    rms = math.sqrt(sum_squares / float(img1.size[0] * img1.size[1]))

    # Error is an arbitrary value, based on values when
    # comparing 2 rotated images & 2 different images.
    return rms
