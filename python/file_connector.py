# -*- coding: utf-8 -*-
#!/usr/bin/python
#%%
"""
Created on Fri Oct 06 10:47:10 2017

@author: ThinkAI

Purpose:
    This is a driver script to call the connector based on connection type and validates the connection. Also checks the parsing module to validate the parsing condition

Version History
2.0     -   Second Version
"""
import logging
import os
import sys
import pandas as pd
import json
import re
from itertools import islice
from mongodb import update_collection, read_collectionbyfield
from Getfieldslist import get_fieldtype
from bson.objectid import ObjectId
from Json_Table_Parsing import convert_table
from pandas.io.json import json_normalize

def __get_logger(self):
    """Instantiates logger."""
    return logging.getLogger(os.path.basename(__file__))


def fetch_onerecord(con_id,dir_path,lines_count):
    try:
        os.chdir(dir_path)
        files = sorted(os.listdir(dir_path), key=os.path.getmtime)
        oldest = files[0]
        newest = files[-1]
        with open(files[0]) as myfile:
            try:
                print("Reading file:", files[0])
                chunk = list(islice(myfile, 0, lines_count))

                #print("1st Record:",str(chunk))
                #print(type(str(chunk)))

                if lines_count == 1:
                    get_fieldtype(con_id, str(chunk))

            except:
                logging.error("Unable to read first record from the sorted file.."+str(sys.exc_info()))

    except:
        logging.error("Unable to read file.."+str(sys.exc_info()))

def file_stream(con_id,dir_path, lines_count):
    raw_input_data = pd.DataFrame()
    count = 0
    i = 0
    error_count = 0
    f_count = 0
    start = 0
    end = lines_count
    rem_rows = 0
    os.chdir(dir_path)
    files = sorted(os.listdir(dir_path), key=os.path.getmtime)
    oldest = files[0]
    newest = files[-1]
    # print("Oldest:",oldest)
    # print("Newest:", newest)
    print("List of JSON files Found:", files, ".........")
    df_l = []
    dic_l = []

    try:
        if lines_count == -1:

            num_files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
            print("num_files",num_files)

            while f_count < num_files:
                with open(files[f_count]) as myfile:
                    try:
                        print("Reading file:",files[f_count])
                        chunk = list(islice(myfile,0,None))
                        #print(len(chunk))
                        #print("chunk length:",len(chunk))
                        #print("old f_count,start,end:",f_count,start,end)
                        f_count = f_count + 1

                        for record in chunk:
                            try:
                                s = record
                                result = json.loads(s)  # try to parse...
                                value, typ = convert_table(record, count)
                                if typ == 'dict':
                                    dic_l.append(value)
                                else:
                                    df_l.append(value)
                                count += 1
                                print("\r Records Read... " + str(count), end="")
                                # print("Original", raw_input_data)
                                # print(raw_input_data.head())
                                # print(raw_input_data.shape)
                                # break  # parsing worked -> exit loop

                            except Exception as e:
                                # print("Exception"+str(e))
                                # "Expecting , delimiter"
                                # position of unexpected character after '"'
                                unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
                                # position of unescaped '"' before that
                                unesc = s.rfind(r'"', 0, unexp)
                                s = s[:unesc] + r'\"' + s[unesc + 1:]
                                # position of correspondig closing '"' (+2 for inserted '\')
                                closg = s.find(r'"', unesc + 2)
                                s = s[:closg] + r'\"' + s[closg + 1:]
                                res = json.dumps(result)
                                # res.strip('\'"')
                                value, typ = convert_table(record, count)
                                if typ == 'dict':
                                    dic_l.append(value)
                                else:
                                    df_l.append(value)
                                count += 1
                                # print("Formatted", raw_input_data)
                                # print(raw_input_data.head())
                                # print(raw_input_data.shape)
                            except:
                                error_count += 1
                                logging.error("Errror while parsing json" + str(sys.exc_info()))

                    except:
                        logging.info("Processed all records..")
                        raise

        while lines_count > 0:

            with open(files[f_count]) as myfile:
                try:
                    print("Reading file:",files[f_count])
                    chunk = list(islice(myfile, start, end))
                    rem_rows = len(chunk)
                    #print(chunk)
                    #print("chunk length:",len(chunk))
                    #print("old f_count,start,end:",f_count,start,end)
                    end = lines_count - len(chunk)
                    lines_count = lines_count - len(chunk)
                    #print("-----------------------------------------------------------------END:",end)

                    for record in chunk:
                        try:
                                    s = record
                                    result = json.loads(s)  # try to parse...
                                    value,typ = convert_table(record, count)
                                    if typ == 'dict':
                                        dic_l.append(value)
                                    else:
                                        df_l.append(value)
                                    count += 1
                                    print("\r Records Read... "+str(count), end="")
                                    #print("Original", raw_input_data)
                                    #print(raw_input_data.head())
                                    #print(raw_input_data.shape)
                                    #break  # parsing worked -> exit loop

                        except Exception as e:
                                    # print("Exception"+str(e))
                                    # "Expecting , delimiter"
                                    # position of unexpected character after '"'
                                    unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
                                    # position of unescaped '"' before that
                                    unesc = s.rfind(r'"', 0, unexp)
                                    s = s[:unesc] + r'\"' + s[unesc + 1:]
                                    # position of correspondig closing '"' (+2 for inserted '\')
                                    closg = s.find(r'"', unesc + 2)
                                    s = s[:closg] + r'\"' + s[closg + 1:]
                                    res = json.dumps(result)
                                    # res.strip('\'"')
                                    value,typ = convert_table(record, count)
                                    if typ == 'dict':
                                        dic_l.append(value)
                                    else:
                                        df_l.append(value)
                                    count+=1
                                    #print("Formatted", raw_input_data)
                                    #print(raw_input_data.head())
                                    #print(raw_input_data.shape)
                        except:
                            error_count+=1
                            logging.error("Errror while parsing json"+str(sys.exc_info()))

                    if end > 0:
                            #print("end----------------------------NEXT FILE--------------------------------------------",end)
                            try:
                                f_count = f_count+1
                                start = 0
                                #end = lines_count - len(chunk)
                                i = len(chunk)
                                #print("new f_count,start,end:", f_count, start, end)

                            except:
                                logging.error("Unable to update object with latest intialization variables.."+str(sys.exc_info()))
                                raise

                    else:
                            break

                except:
                    logging.info("Processed all records..")
                    raise

        if len(dic_l) > 0 and len(df_l) > 0:
            raw_input_data_dic = json_normalize(dic_l,sep='~')
            raw_input_data_df = pd.concat(df_l,axis=0)
            raw_input_data = raw_input_data_dic.append(raw_input_data_df,ignore_index=False)
        elif len(df_l) > 0:
            raw_input_data = pd.concat(df_l,axis=0)
        elif len(dic_l) > 0:
            raw_input_data = json_normalize(dic_l,sep='~')
        #print(raw_input_data)
        return raw_input_data

    except:
        logging.error("Unable to open file.."+str(sys.exc_info()))
        raise

def filestream(con_id,dir_path,lines_count):
    try:
        logging.basicConfig(level=logging.INFO)

        dir_path = dir_path
        lines_count = lines_count
        return file_stream(con_id,dir_path,lines_count)

    except:
        logging.error("Unable to read file.." + str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while reading file. Error Message <--> " + str(
                                                                         sys.exc_info())})

def onerecord(con_id,dir_path,lines_count):
    try:
        logging.basicConfig(level=logging.INFO)

        dir_path = dir_path
        lines_count = lines_count
        fetch_onerecord(con_id,dir_path,lines_count)

    except:
        logging.error("Unable to read file.." + str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while reading file. Error Message <--> " + str(
                                                                         sys.exc_info())})
if __name__ == '__filestream__':
    filestream()

if __name__ == '__onerecord__':
    onerecord()

#onerecord()
#filestream()