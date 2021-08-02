import time
import os
import pickle
from datetime import datetime


def clamp(n, low, high):
    '''
    clamp a number to between low and high, inclusive. Also accepts None for either low or high to
    ignore that bound

    :param n: number to clamp
    :param low: lower bound or None
    :param high: upper bound or None
    :return: clamped value
    '''
    return min(max(n, low if low is not None else n), high if high is not None else n)


def make_path(path):
    os.makedirs(path, exist_ok=True)


def save(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def timer(func):
    '''
    Not for profiling. Time execution of a function in walltime that is substantial enough
    to neglect variation from sleep/switching times.

    :return: wrapped function that prints time elapsed on function return
    '''
    def wrapped(*args, **kwargs):
        start = time.time_ns()
        retval = func(*args, **kwargs)
        end = time.time_ns()
        print(f"elapsed time: {(end-start)*10E-9:.3f}s")
        return retval

    return wrapped


def get_timestamp():
    return datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
