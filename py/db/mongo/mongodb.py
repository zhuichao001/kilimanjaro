# -*- coding: utf-8 -*- 

import pyutil.common.util as common_util
import pyutil.db.mongo as mongo
import time
import sys


class mongodb:
    def __init__(self, db_config):
        print ":::MONGO_CONFIG:::", db_config
        self.m = mongo.mongo(db_config)

    def __filter_fileds(self, items, fieldList):
        if not fieldList:
            return items

        result = []
        for item in items:
            for field in item.keys():
                if field not in fieldList:
                    del item[field]
            result.append(item)
        return result

    def Find(self, tabName, fieldList=[], indexMap={}, limit=(), orderby=((),"asc"), out=dict):
        items =  self.m.get(tabName, indexMap, json=True)
        return self.__filter_fileds(items, fieldList)

    def Max(self, tabName, field, indexMap={}):
        items = self.Find(tabName, [field], indexMap)
        return max(items)

    def Min(self, tabName, field, indexMap={}):
        items = self.Find(tabName, [field], indexMap)
        return min(items)

    def Count(self, tabName, indexMap={}):
        return self.m.count(tabName, indexMap)

    def Exist(self, tabName, indexMap):
        return self.m.count(tabName, indexMap)>0

    def Update(self, tabName, dataMap, indexMap):
        return self.m.update(tabName, dataMap, indexMap)

    def Insert(self, tabName, dataMap):
        return self.m.insert(tabName, dataMap)

    def UpOrInsert(self, tabName, dataMap, indexMap):
        #TODO
        return None

    def Delete(self, tabName, indexMap={}):
        #TODO
        return None

    def Search(self, tabName, fieldList=[], conditionList={}, relation="OR",  order=[], limit=(), out=list):
        #TODO
        return None

    def Columns(self, tabName):
        return self.columns(tabName)

    def FieldInt(self, tabName, field, indexMap, default=0):
        items = self.Find(tabName, [field], indexMap)
        if items !=0:
            print "WARNING: mongor.FieldInt result is not single, ", tabName, field, indexMap,
            return default
        return int(items[0])

    def FieldStr(self, tabName, field, indexMap):
        #TODO
        return None

    def AddField(self, tabName, field, num, indexMap):
        #TODO
        return None

    def IncField(self, tabName, field, indexMap):
        #TODO
        return None
