import time

debug = False

def timestamp():
    """return a time stamp"""
    if debug:print 'timestamp' , str(int(time.time() * 1000))
    return str(int(time.time() * 1000))

