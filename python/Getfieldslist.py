# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 19:08:23 2017

@author: dadmrbalakrishnan
"""
from __future__ import print_function
import json
import pendulum as pen
import re
import ast
import sys
from mongodb import update_collection
from mongodb import read_collectionbyid
from bson.objectid import ObjectId
from time import mktime
import time
from datetime import datetime


def get_fieldtype(Con_id='', s=''):
    try:
        field_list = {}
        field_value = {}
        l_fields = '|'
        l_type = '|'
        l_fields_time = '|'
        time_series = False

        def flatten_json(y):
            out = {}

            def flatten(x, name=''):
                if type(x) is dict:
                    for a in x:
                        flatten(x[a], name + a + '~')
                elif type(x) is list:
                    for a in x:
                        flatten(a, name + '`')
                else:
                    fname = re.sub('~+', '~', name[:-1], flags=re.I)
                    out[fname] = x

            flatten(y)
            return out

        def find_type(keys):

            def is_date(string):
                try:
                    pen.parse(string)
                    return True
                except:
                    try:
                        #print(string)
                        datetime.fromtimestamp(mktime(time.strptime(string, '%d/%b/%Y:%H:%M:%S %z')))
                        return True
                    except:
                        return False

            def is_int(string):
                try:
                    v = int(string)
                    return False
                except:
                    return True

            def is_float(string):
                try:
                    v = float(string)
                    return False
                except:
                    return True

            for key in keys:
                field_type = str(type(keys[key]).__name__)
                if is_date(str(keys[key])) and is_int(str(keys[key])) and is_float(str(keys[key])):
                    field_type = "DateTime"
                field_list[str(key)] = field_type
                field_value[str(key)] = (str(keys[key]))

        if s[0] == '[':
            s = ast.literal_eval(s)
            for x in list(s):
                x = str(x).replace("\\'", 'XXREPLACEMEOHYEAHXX').replace("'", '"').replace('XXREPLACEMEOHYEAHXX', "\\'")
                data = json.loads(x)
                result = flatten_json(data)
                find_type(result)
        else:
            data = json.loads(s)
            result = flatten_json(data)
            find_type(result)
            print(field_list)
        for r, v in field_list.items():
            if v == 'DateTime':
                time_series = True
                l_fields_time = l_fields_time + r + '|'
            l_fields = l_fields + r + '|'
            l_type = l_type + v + '|'
            # l_field_value = '|'
            # for val in field_value:
            # l_field_value = l_field_value+val+'|'
        record_insert = {"Con_id": Con_id, "Field_list": l_fields, "Field_Type_List": l_type,
                         "Time_Series_Field_List": l_fields_time, "Time_Series": time_series,
                         "Field_Value": field_value}
        update_collection("nnfieldslist", "Con_id", Con_id, record_insert)
        update_collection("nnconnections", "_id", ObjectId(Con_id), {"Status": "Successful", "Error_Message": ""})
    except:
        update_collection("nnconnections", "_id", ObjectId(Con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while Parsing Josn. Error Message <--> " + str(
                                                                         sys.exc_info())})