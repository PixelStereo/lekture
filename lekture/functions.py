import time

debug = False

def timestamp():
    """return a time stamp"""
    if debug:print 'timestamp' , str(int(time.time() * 1000))
    return str(int(time.time() * 1000))

def unicode2string_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = unicode2string_list(value)
        elif isinstance(value, dict):
            value = unicode2string_dict(value)
        rv[key] = value
    return rv

def unicode2string_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = unicode2string_list(item)
        elif isinstance(item, dict):
            item = unicode2string_dict(item)
        rv.append(item)
    return rv
