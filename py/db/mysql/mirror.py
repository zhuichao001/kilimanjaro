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

class mirror:
    def __init__(self, address, db_name):
        self.DB = db_name
        self.ADDRESS = address


    def __get_address(self):
        if type_util.is_str(self.ADDRESS):
            return self.ADDRESS
        elif type_util.is_array(self.ADDRESS):
            return random.choice(self.ADDRESS)
        else:
            return "UNKWON HOST ADDRESS"
    

    def __filter_fileds(self, result, fieldList):

        def key_filter(item):
            if not fieldList:
                return item

            _fieldList = [k if k.upper().find(" AS ")<0 else k.strip().split()[-1] for k in fieldList]

            if type_util.is_array(item):
                return [ key_filter(i) for i in item ]
            elif type_util.is_dict(item):
                new_obj = {}
                for k in item:
                    if k in  _fieldList:
                        new_obj[k] =  item[k]
                return new_obj
            else:
                return item

        try:
            obj = json.loads(result).get("data")
            if type_util.is_array(obj):
                return [ key_filter(o) for o in obj ]
            elif type_util.is_dict(obj):
                return key_filter(obj)
            else:
                return obj
        except Exception,e:
            print "Error when __filter_fields:", str(e)
            return None


    def __query_encode(self, indexMap):
        if not indexMap:
            return ""
        param_list = []
        for k,v in indexMap.items():
            if k.startswith("__") and k.endswith("__"):
                param_list.append( "%s=%s" % (k, str(v)) )
            elif type_util.is_array(v):
                param_list.append( "%s=json:%s" % (k, quote(json.dumps(v))) )
            elif type_util.is_int(v):
                param_list.append( "%s=int:%d" % (k, v) )
            elif type_util.is_str(v):
                param_list.append( "%s=str:%s" % (k, str(v)) )
            else:
                param_list.append( "%s=%s" % (k, str(v)) )
        return "&".join(param_list)


    def __url(self, tabName, indexMap, method="GET"):
        query_str = self.__query_encode(indexMap)
        if method.upper() in ["GET", "POST"]:
            prefix = "%s/%s/%ss" % (self.__get_address(), self.DB, tabName)
            return prefix +"?" + query_str if query_str else prefix
        else:
            prefix = "%s/%s/%s" % (self.__get_address(), self.DB, tabName)
            return prefix +"?" + query_str if query_str else prefix


    def Find(self, tabName, fieldList=[], indexMap={}, limit=(), orderby=((),"asc"), out=dict):
        if type_util.is_array(limit)  and len(limit)==2:
            indexMap["__start__"] = str(limit[0])
            indexMap["__count__"] = str(limit[1])
        if type_util.is_array(orderby) and len(orderby)>=2:
            indexMap["__orderby__"] = quote(json.dumps(orderby))
        if type_util.is_array(fieldList):
            indexMap["__fieldlist__"] = quote(json.dumps(fieldList))
        indexMap["__out__"] = "dict" if out==dict else "list"

        url = self.__url(tabName, indexMap, "GET")

        result = http_util.Request(url)
        
        return self.__filter_fileds(result, fieldList)


    def Max(self, tabName, field, indexMap={}):
        return max(self.Find(tabName, [field], indexMap))


    def Min(self, tabName, field, indexMap={}):
        return min([ o for o in self.Find(tabName, [field], indexMap) if o])


    def Exist(self, tabName, indexMap):
        result = self.Find(tabName, fieldList=[], indexMap={}, limit=(), orderby=((),"asc"), out=dict)
        if result.get("data"):
            return True
        else:
            return False


    def Update(self, tabName, dataMap, indexMap):
        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))
        url = self.__url(tabName, indexMap, "PUT")

        result = http_util.Request(url, json.dumps(dataMap), method="PUT")
        jsn = json.loads(result) 
        if jsn.get('code',0) == 1:
            return jsn.get('data')
        else:
            return None


    def Insert(self, tabName, dataMap):
        url = self.__url(tabName, {}, "POST")

        result = http_util.Request(url, json.dumps(dataMap), method="POST")
        jsn = json.loads(result) 
        if jsn.get('code',0) == 1:
            data = jsn.get('data')
            return data[0], data[1]
        else:
            return None


    def UpOrInsert(self, tabName, dataMap, indexMap):
        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))
        if self.Exist(tabName, indexMap):
            return self.Update(tabName, dataMap, indexMap)
        else:
            return self.Insert(tabName, dataMap)


    def Delete(self, tabName, indexMap={}):
        if isinstance(indexMap, dict):
            indexMap = common_util.FilterMap(indexMap, self.Columns(tabName))
        url = self.__url(tabName, indexMap, "DELETE")

        result = http_util.Request(url, method="DELETE")
        jsn = json.loads(result) 
        if jsn.get('code',0) == 1:
            return jsn.get('data', None)
        else:
            return None


    def Search(self, tabName, fieldList=[], indexMap={}, limit=(), orderby=((),"asc"), out=dict):
        return self.Find(tabName , fieldList , indexMap , limit , orderby , out)


    def Count(self, tabName, indexMap={}):
        query_str = self.__query_encode(indexMap)
        url = "%s/%s/%s/ext?action=count&" % (self.__get_address(), self.DB, tabName) + query_str
        result = http_util.Request(url)
        try:
            return json.loads(result)["data"] or 0
        except Exception, e:
            print "Error!!! mirror.Count, Exception:", str(e)
            return 0


    @db_util.func_cache
    def Columns(self, tabName):
        url = "%s/%s/%s/ext?action=columns" % (self.__get_address(), self.DB, tabName)

        result = http_util.Request(url)
        try:
            return json.loads(result)["data"] or []
        except Exception, e:
            print "Error!!! mirror.Columns, Exception:", str(e)
            return []
