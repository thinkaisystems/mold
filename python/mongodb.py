# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 17:32:27 2017

@author: dadmrbalakrishnan
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient('mongodb://PARAMDOCKERHOSTIP:27017/')
db = client.nnmodel

def read_collectionbyid(collection_name,obj_id):
    #try:
        records = db[collection_name].find_one({"_id": ObjectId(obj_id)})
    #except Exception as e:
        #records = e
        return records

def read_collectionbyfield(collection_name,field,value):
    #try:
        records = db[collection_name].find_one({field: value})
    #except Exception as e:
        #records = e
        return records

def insert_collection(collection_name,dic):
    #try:
        insert_id = db[collection_name].insert_one(dic).inserted_id
    #except Exception as e:
        #insert_id = e
        return insert_id

def update_collection(collection_name,field,value,dic):
    #try:
        result = db[collection_name].update_one({field: value},{'$set': dic},upsert=True)
    #except Exception as e:
        #result = e
        return result

def append_collection(collection_name,s_field,s_value,field,value):
    #try:
        result = db[collection_name].update_one({s_field: s_value},{'$push': {field:value}},upsert=True)
    #except Exception as e:
        #result = e
        return result