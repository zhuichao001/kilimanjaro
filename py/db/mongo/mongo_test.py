#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
 
import pymongo  
import datetime  
from bson.objectid import ObjectId  
   

def test():
    mog = mongo(config)
    id = mog.insert("qiuzi", {"a":12, "b":333})
    print mog.get_by_id("qiuzi", id)
    print mog.insert("qiuzi", [{"a":12, "b":333}, {"x":0, "y":999}])
    print mog.get("qiuzi")
    

if __name__ == '__main__':  
    test()
