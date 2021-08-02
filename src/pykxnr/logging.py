from inspect import currentframe
import logging

def debug_print(arg):
    '''
    print function that tags the print with the
    line number and file from which it was called
    so that debug prints can be easily removed
    once they are not needed.

    params
    ------
    '''
    frameinfo = currentframe()
    print(frameinfo.f_back.f_lineno, ":", arg)


class logger(logging.Logger):
    pass