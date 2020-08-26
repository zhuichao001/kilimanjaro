# -*- coding: utf-8 -*- 

import MySQLdb
import logging
import threading
import pyutil.common.sys_utf8
import pyutil.db.mysqlpool as mysqlpool
import pyutil.db.conn_pool as conn_pool
import re

class magic:

    def __init__(self, dbconfig):
        if not dbconfig:
            raise Exception("when call magic.__init__(self, db_config), db_config must not be None")
        self.dbconfig = dbconfig

        self.pool = conn_pool.conn_pool(self.dbconfig)
        self.conn_tran = None


    def query_dict(self, lang):
        try:
            conn = self.conn_tran or self.pool.get_conn()
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cursor.execute(lang)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception, e:
            print "Error when query dict:",lang, "\n Exception:", e
            logging.error("Error when query dict: %s \n Exception: %s" %(lang, e))
        return []

    def query(self, lang):
        try:
            conn = self.conn_tran or self.pool.get_conn()
            cursor = conn.cursor()
            cursor.execute(lang)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception, e:
            print "Error when query:",lang, "\n Exception:", e
            logging.error("Error when query: %s \n Exception: %s" %(lang, e))
        return []
    
    def get_count(self, table_name): 
        lang = "SELECT COUNT(1) FROM " + table_name
        rows = self.query(lang)
        return int(rows[0][0]) if len(rows)>0 else 0

    def upsert(self, lang):
        try:
            conn = self.conn_tran or self.pool.get_conn()
            cursor = conn.cursor()
            cursor.execute(lang)
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid)) if cursor.lastrowid else (-1,-1)
            cursor.close()
            return rowcount, primaryid
        except:
            print "Error when upsert sql:", lang
            logging.error("Error when upsert sql: %s" % lang)
            return -1, -1

    def execute_lang(self, lang, autocommit=False):
        try:
            conn = self.conn_tran or self.pool.get_conn()
            cursor = conn.cursor()
            cursor.execute(lang)
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid) if cursor.lastrowid else -1)
            
            if lang.upper().strip().startswith("UPDATE ") and rowcount == 0:
                matchcount = self.__get_match_row_count(cursor._info)    
                rowcount = matchcount 

            if autocommit and not self.conn_tran:
                conn.commit()

            cursor.close()
            return rowcount, primaryid
        except Exception, e:
            print "Error when execute_lang sql:", lang, ",exception：", e
            logging.error("Error when execute_lang sql: %s \n Exception: %s" %(lang, e))
            return  -1, -1

    def execute(self, lang, params=(), autocommit=False):
        if not params:
            return self.execute_lang(lang, autocommit)
        try:
            conn = self.conn_tran or self.pool.get_conn()
            cursor = conn.cursor()
            cursor.execute(lang, params)
            rowcount, primaryid = (cursor.rowcount, int(cursor.lastrowid) if cursor.lastrowid else -1)
            if lang.upper().startswith("UPDATE ") and rowcount == 0:
                matchcount = self.__get_match_row_count(cursor._info)    
                rowcount = matchcount 
            if autocommit and not self.conn_tran:
                conn.commit()
            cursor.close()
            return rowcount, primaryid
        except Exception, e:
            print "Exception:", e, "Error when execute sql:", lang
            logging.error("Error when execute sql: %s \n Exception: %s" %(lang, e))
            return -1, -1

    
    def __get_match_row_count(self, _cursor_info):
        return int(re.search(r'Rows matched: (\d+)', _cursor_info).group(1))

    def start_transaction(self): 
        self.conn_tran = self.pool.get_conn(True)

    def rollback(self):
        self.conn_tran.rollback()
        self.conn_tran = None

    def commit(self):
        self.conn_tran.commit()
        self.conn_tran = None
