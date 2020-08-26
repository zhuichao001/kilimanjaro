#!/usr/local/bin/python
# -*- coding: utf8 -*-  
  

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import pyutil.common.dict_util as dict_util
import logging
import time


class conn_pool(object):
    def __init__(self, config):
        _c = dict_util.BaseDict(config)
        self._pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20, maxconnections=200,
                          host=_c.host , port=_c.port , user=_c.user , passwd=_c.password,
                          db=_c.database, use_unicode=False, charset=_c.charset)

    def get_conn(self, is_tran=False):
        sharable = not is_tran
        conn = self._pool.connection(sharable)
        autocommit = 1 if not is_tran else 0
        cursor = conn.cursor()
        cursor.execute("set session transaction isolation level read committed; set autocommit=%d" % (autocommit))
        cursor.close()
        return conn

