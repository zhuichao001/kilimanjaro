#!/usr/local/bin/python
# -*- coding: utf8 -*-  

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import pyutil.common.dict_util as dict_util
import logging
import time


if __name__ == '__main__':
    import pyconf.db.default as default
    pool = conn_pool(default.config)
    conn = pool.get_conn(autocommit=1)
    cursor = conn.cursor()
    rows = cursor.execute("select * from info_user limit 1")
    result = cursor.fetchall()
    rows = cursor.execute("update info_user set name='222' where user_id = 2")
    rows = cursor.execute("update info_user set name='333' where user_id = 3")
    #conn.commit()
    print rows
