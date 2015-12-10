import time

debug = True

def timestamp():
    """return a time stamp"""
    print 'timestamp' , str(int(time.time() * 1000))
    return str(int(time.time() * 1000))

