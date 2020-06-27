import logging

from foe_pics import findToCollect, findSomethingSleeps


def isThereSomethingToCollect():
    result = findToCollect() is not None
    logging.debug("isThereSomethingToCollect: %s", result)
    return result


def isThereSomethingSleeps():
    result = findSomethingSleeps() is not None
    logging.debug("findSomethingSleeps: %s", result)
    return result
