# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 23:08:33 2017

@author: dadmrbalakrishnan
"""

from __future__ import print_function
import json
#import datetime
#from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
#from flatten_json import flatten
from dateutil.parser import parse
import re
import ast
def convert_table(s='',record_index=0):
    if s.strip()[1:].count('[') == 0:
        #print("yes")
        if s[0] == '[':
            s = s.strip()[:-1]
            s = s[1:]
            #df_raw_data = pd.read_json(s,orient="record")
            #df_raw_data['Record_ID']=record_index
            #df_raw_data['Sub_Record_ID'] = record_index
            #print(df_raw_data)
            #return df_raw_data
            return  json.loads(s),'dict'
        else:
            #s = "["+s+"]"
            #df_raw_data = pd.read_json(s,orient="record")
            #df_raw_data['Record_ID']=record_index
            #df_raw_data['Sub_Record_ID'] = record_index
            #print(df_raw_data)
            #return df_raw_data
            return  json.loads(s),'dict'
    else:
        Colm_List = {}
        least_colm_txt = ''
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

        def add_data(y,have_list):

                def flatten(x,i=0, name=''):
                    if type(x) is dict:
                        for a in x:
                            flatten(x[a],i, name + a + '~')
                    elif type(x) is list:
                        i=0
                        for a in x:
                            flatten(a,i, name + '`')
                            i+=1
                        i=0
                    else:
                        fname = re.sub('~+', '~', name[:-1], flags=re.I)
                        update_df(fname,x,i)
                flatten(y)


        def find_list(keys):

                have_list = []
                for key in keys:
                    setter=0
                    for key2 in keys:
                        if key[:key.rfind('~')]+'~' in key2 and "`" in key2:
                            setter =1
                    if min(result.keys(), key=len) == key and "`" in key:
                        setter =0
                    if setter==1:
                        have_list.append(key)
                return have_list

        def find_type(keys):
                field_list = {}
                def is_date(string):
                    try:
                        parse(string)
                        return True
                    except ValueError:
                        return False
                for key in keys:
                    field_type = str(type(keys[key]).__name__)
                    if is_date(str(keys[key])) :
                        field_type = "DateTime"
                    field_list[str(key)] = field_type
                return field_list
        def create_df_col(keys):
                df_collection = {}
                for key in keys:
                    df_collection[key]=pd.DataFrame({key:[]})
                return df_collection


        def update_df(col_name,value,ii):
                current_loc=0;
                loop_ind = 1
                col = col_name
                if '##' in list(Colm_List[col_name][col_name].unique()):
                    loop_ind = 0;
                    if value is None:
                        value = 'null'
                    Colm_List[col_name][Colm_List[col_name][col_name] == '##'] = str(value)
                if loop_ind ==  1:
                    Colm_List[col_name].loc[Colm_List[col_name].shape[0],col] = value
                current_loc = Colm_List[col_name].shape[0]-1
                colname_list = re.split('[~]',col_name[len(least_colm_txt):])
                match_ind = 0
                if len(colname_list) > 1:
                  for col in Colm_List:
                    if col_name==col:
                        match_ind = 1
                    #if len(colname_list) > 1:
                    if (least_colm_txt+colname_list[0]+"~")==col[:len((least_colm_txt+colname_list[0]+"~"))]:
                            if col_name[:col_name.rfind('~')] not in col:
                                if Colm_List[col].shape[0] == 0 and (Colm_List[col].shape[0]) <= current_loc:
                                    Colm_List[col].loc[0,col] = "##"
                                if ii>0 and Colm_List[col].shape[0] != 0 and len(colname_list) > 2:
                                           def back_loop(dd):
                                               t = dd[:dd.rfind('~')]
                                               tt = t[:t.rfind('~')]
                                               if tt in col and '`' not in col[len(tt)+2:] and Colm_List[col].shape[0] <=current_loc:
                                                    #if Colm_List[col].shape[0] <=current_loc:
                                                       if match_ind == 1:
                                                           Colm_List[col].loc[Colm_List[col].shape[0],col] = "##"#Colm_List[col].loc[Colm_List[col].shape[0]-1]
                                                       else:
                                                           Colm_List[col].loc[Colm_List[col].shape[0],col] = Colm_List[col].loc[Colm_List[col].shape[0]-1,col]

                                               return t
                                           colm_array_length = len(colname_list)
                                           t = col_name
                                           while  colm_array_length > 2:
                                               t = back_loop(t)
                                               colm_array_list = re.split('[~]',t[len(least_colm_txt):])
                                               colm_array_length = len(colm_array_list)


        def merge_df(Record_id,have_list):
                df_result = pd.concat(Colm_List.values(), axis=1,copy=False)
                df_result['Record_ID'] = Record_id
                df_result = pd.concat([df_result,pd.DataFrame(np.arange(df_result.shape[0]),columns=["Sub_Record_ID"])], axis=1)
                for col in Colm_List:
                    df_result[col] = df_result[col].replace('##',method='ffill')
                    if col not in have_list:
                         df_result[col] = df_result.loc[0, col]
                return df_result


        #print(s[0])
        if s[0] == '[':
            s = ast.literal_eval(s)
            #print(s)
            counter=0
            for x in list(s):
                x= str(x).replace("\\'", 'XXREPLACEMEOHYEAHXX').replace("'", '"').replace('XXREPLACEMEOHYEAHXX', "\\'")
                #print(x)
                data = json.loads(str(x))
                #print(datetime.datetime.now())
                result = flatten_json(data)
                #print(result)
                least_col = min(result.keys(), key=len)
                #print(least_col)
                least_colm = least_col[:least_col.find("~`")]
                least_colm = least_colm[:least_colm.rfind('~')]
                have_list = find_list(result.keys())
                #print(least_colm)
                sep=''
                if len(least_colm)+2 <= len(least_col) and least_colm != '':
                        if least_col[len(least_colm):len(least_colm)+2] == '~`':
                            sep="~'"
                        else:
                            sep="~"

                least_colm_txt = least_colm+sep
                Colm_List = create_df_col(result.keys())
                add_data(data,have_list)
                if counter == 0:
                    df_result = pd.DataFrame(merge_df(record_index,have_list))
                    #print(df_result.head())
                else:
                    #print(pd.DataFrame(merge_df(1,have_list)).head(),)
                    df_result = df_result.append(pd.DataFrame(merge_df(record_index,have_list)),ignore_index=True)
                    #print(df_result.head())
                #print(datetime.datetime.now())
                counter+=1
            df_result["Sub_Record_ID"] = np.arange(df_result.shape[0])
        else:
                data = json.loads(s)
                #print("loads Json "+str(datetime.datetime.now()))
                result = flatten_json(data)
                #print("Flatten Json "+str(datetime.datetime.now()))
                least_col = min(result.keys(), key=len)
                least_colm = least_col[:least_col.find("~`")]
                least_colm = least_colm[:least_colm.rfind('~')]
                have_list = find_list(result.keys())
                sep=''
                if len(least_colm)+2 <= len(least_col) and least_colm != '':
                        if least_col[len(least_colm):len(least_colm)+2] == '~`':
                            sep="~'"
                        else:
                            sep="~"
                least_colm_txt = least_colm+sep
                #print("Find Have list "+str(datetime.datetime.now()))
                Colm_List = create_df_col(result.keys())
                #print("create df "+str(datetime.datetime.now()))
                add_data(data,have_list)
                #print("add_data df "+str(datetime.datetime.now()))
                df_result = pd.DataFrame(merge_df(record_index,have_list))
                #print("Merge Data df "+str(datetime.datetime.now()))
        #df_raw_data = pd.DataFrame()
        #df_raw_data = df_result.append(df_result)
        return(df_result,'df')
