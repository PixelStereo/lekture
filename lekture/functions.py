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

def unicode2_list(data):
    if isinstance(data,list):
        if len(data) == 1:
            rv = data[0]
            rv = checkType(rv)
        else:
            rv = []
            for item in data:
                item = checkType(item)
                rv.append(item)
    return rv

def checkType(data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    if isinstance(data,str):
        if data.isdigit():
            data = int(data)
        elif isFloat(data):
            data = float(data)
    elif isFloat(data):
        data = float(data)
    elif isInt(data):
        data = int(data)
    else:
        print 'no type' , data , type(data)
    return data

def isString(value):
  try:
    str(value)
    return True
  except:
    return False
def isList(value):
  try:
    list(value)
    return True
  except:
    return False

def isUnicode(value):
  try:
    unicode(value)
    return True
  except:
    return False

def isFloat(value):
  try:
    float(value)
    return True
  except:
    return False

def isInt(value):
  try:
    int(value)
    return True
  except:
    return False

"""a_string = u'popo2'
a_float = u'122.2'
an_int = u'122'
print 'a_string' , checkType(a_string)
print 'a_float' , checkType(a_float)
print 'an_int' , checkType(an_int)"""