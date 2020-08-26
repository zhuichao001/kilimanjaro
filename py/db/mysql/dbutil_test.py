# -*- coding: utf-8 -*- 

import datetime
import functools
import time


def test():
    a= [{'a':123},{'b':'c'}]
    print ParseUtime(a)
    b =  [(103, u'12210', u'12210', u'12210', u'12210', 1, datetime.datetime(2017, 12, 6, 20, 22, 8))]
    print ParseUtime(b)


if __name__ == '__main__':
    test_escape()
