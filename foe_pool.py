import multiprocessing

pool = None


def initPool():
    global pool
    pool = multiprocessing.Pool(int(multiprocessing.cpu_count()))


def execInPool(func, params):
    return pool.map(func, params)
