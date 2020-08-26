# -*- coding: utf-8 -*- 

import MySQLdb
import logging
import threading
import pyutil.common.sys_utf8
import pyutil.db.mysqlpool as mysqlpool
import pyutil.db.conn_pool as conn_pool
import re


def test():
    import pyconf.db.default as default
    mysql = magic(default.config)
    rows = mysql.query_dict("SELECT * FROM info_user limit 1")
    for row in rows:
        print row

def test2():
    import pyconf.db.default_dev as default
    mysql = magic(default.config)
    
    mysql.start_transaction()
    ret = mysql.execute("insert into info_device_alarmer(alarmer_id, dtu_id, alarmer_no) values(1234561, 12343, 1234)")
    print ret

    ret = mysql.execute("insert into info_device_alarmer(alarmer_id, dtu_id, alarmer_no) values(1234562, 12343, 1234)")
    print ret
    mysql.commit()


if __name__ == '__main__':
    test()
    test2()
