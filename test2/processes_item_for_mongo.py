# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:00:10 2018

@author: Administrator
"""


import redis
import pymongo
import json

def process_item():

    redisconn = redis.Redis(
            host = "127.127.127.127",
            port = 6379,
            db = 0
            )
    

    mongoconn = pymongo.MongoClient(
            host = "127.0.0.1",
            port = 27017
            )
    

    dbname = mongoconn["cas"]
    sheetname = dbname["casredis"]
    
    
    
    while True:

        source, data = redisconn.blpop("cas:items")
        data = json.loads(data)
        sheetname.insert_one(data)
        

    
if __name__ == "__main__":
    process_item()