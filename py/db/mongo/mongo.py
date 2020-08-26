#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
 
import pymongo  
import datetime  
from bson.objectid import ObjectId  
   
class mongo:
    def __init__(self, config):  
        self.client = pymongo.MongoClient(config["host"], config["port"])
        self.db = self.client[config["database"]]


    def __filter_objectid(self, items, json):
        if json==True and items:
            for item in items:
                del item["_id"]
        return list(items)

       
    def insert(self, tableName, item):
        id = self.db[tableName].insert(item)  
        return id


    def insert_multi(self, tableName, items):  
        id = self.db[tableName].insert(items)  
        return id


    def get(self, tableName, indexMap={}, orderby=(), json=True):
        items = list(self.db[tableName].find(indexMap))
        return self.__filter_objectid(items, json)

   
    def get_one(self, tableName, indexMap={}, json=True):
        item = self.db[tableName].find_one(indexMap)
        return self.__filter_objectid(item)

   
    def get_by_objectid(self, tableName, objectid, json=True):  
        item = self.db[tableName].find_one({"_id": ObjectId(str(objectid))})  
        return self.__filter_objectid(item, json)


    def columns(self, tableName):
        return self.get_one(tableName).keys()
       

    def update(self, tableName, dataMap, indexMap): 
        item = self.db[tableName].update(indexMap)
        return self.__filter_objectid(item, True)


    def count(self, tableName, indexMap):
        return len(self.get(tableName, indexMap)) if indexMap self.db[tableName].count()
       

    def remove(self, tableName, indexMap):  
        self.db[tableName].remove(indexMap)


    def clear(self, tableName):
        self.collection.remove()  
