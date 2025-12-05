import time


def now():
    """
    Returns the current time in seconds since the epoch.
    """
    return time.time()


def elapsed(start_time):
    """
    Returns the elapsed time in seconds since start_time.
    """
    return now() - start_time