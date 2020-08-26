# -*- coding: utf-8 -*- 

import datetime
import functools
import time


def escape_string(value):
    if not isinstance(value, str) and not isinstance(value, unicode):
        return value
    value = value.replace('\\', '\\\\')
    value = value.replace('\0', '\\0')
    value = value.replace('\n', '\\n')
    value = value.replace('\r', '\\r')
    value = value.replace('\032', '\\Z')
    value = value.replace("'", "\'")
    value = value.replace('"', '\"')
    return value


def func_cache(func):

    cache = {}
    last = {}

    @functools.wraps(func)
    def _inner(*args):
        db_config = args[0].db_config
        key = func.__name__+"@"+db_config["database"]
        if len(args)>1:
            key +=":"+str(args[1])
        if key not in cache or last.get(key, 0)+120<time.time():
            last[key] = time.time()
            cache[key] = func(*args)
        return cache[key]
    return _inner


def ParseUtime(data):
    if isinstance(data, list) or isinstance(data, tuple):
        result = []
        for item in data:
            result.append(ParseUtime(item))
        return result
    elif isinstance(data, dict):
        result = {}
        for key in data:
            result[key]=ParseUtime(data[key])
        return result
    elif isinstance(data, datetime.datetime):
        try:
            return data.strftime('%Y-%m-%d %H:%M:%S')
        except Exception, e:
            return "0000-00-00 00:00:00"
    elif isinstance(data, datetime.date):
        try:
            return data.strftime('%Y-%m-%d')
        except Exception, e:
            return "0000-00-00"
    else:
        return data
