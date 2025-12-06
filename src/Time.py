import time

def current_time_hms():
    """
    Returns the current time as a formatted string HH:MM:SS.
    """
    return time.strftime("%H_%M_%S", time.localtime())

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