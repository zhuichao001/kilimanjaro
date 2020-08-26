# -*- coding: utf-8 -*- 

import pyutil.common.sys_utf8 as sys_utf8
import pyutil.common.util as common_util
import pyutil.common.http_util as http_util
import pyutil.common.type_util as type_util
import pyutil.db.util as db_util

import time
import json
import sys
import random
from urllib import quote


def test():
    m = mirror("127.0.0.1:9397", "default")
    result = m.Find("info_building", [], {"building_id":5257})
    print sys_utf8.Utf8(result)
    print "-----------------"
    result =  m.Update("info_building", {"building_name":"未名办公楼"}, {"building_id":5257})
    print sys_utf8.Utf8(result)

    print "-----------------"
    result =  m.Delete("info_building",  {"building_id":1})
    print sys_utf8.Utf8(result)

    print "====================="
    result =  m.Insert("info_building", {"building_name":"未名办公楼", "enum_building_type":1})
    print sys_utf8.Utf8(result)

    print "+++++++++++++++++++++++++++++"
    result =  m.Search("info_building", [], {"building_name":("like", '办公楼')})
    print sys_utf8.Utf8(result)


def test2():
    m = mirror("127.0.0.1:9397", "default")
    result = m.Find("info_user", [], {"joined_time": ("<>", ("2016-01-01 00:00:00", "2016-08-01 00:00:00"))}, out=dict)
    print "--------------------------------------------"
    print sys_utf8.Utf8(result)


if __name__ == '__main__':
    test()
