# -*- coding: utf-8 -*-
#!/usr/bin/python
#%%
"""
Created on Fri Oct 31 13:15:00 2017 CST

@author: ThinkAI

Purpose:
    This is a driver script to call the connector based on connection type and validates the connection. Also checks the parsing module to validate the parsing condition

Version History
2.0     -   Second Version
"""
from File_Streaming import onerecord as file_con_onerecord, filestream
from Kafka_Streaming import onerecord, kafkastream
from sys import argv
import logging
import datetime
import os
import sys
from mongodb import read_collectionbyid, update_collection
from bson.objectid import ObjectId
from Pre_Processing import pre_processing
from Train_Model import trainmodel
from Post_Processing import  postprocessing
from datetime import datetime
import numpy as np

# create logger
def __get_logger(self):
    """Instantiates logger."""
    return logging.getLogger(os.path.basename(__file__))

def read_connection(model_id):
    try:

        insert_record = {}
        insert_record["Timestamp"] = datetime.now()
        insert_record["S_Model_id"] = model_id
        insert_record["Result"] = []
        update_collection("nnresults",'S_Model_id',model_id, insert_record)
        read_model = read_collectionbyid("nnmodels", model_id)
        #print(read_counters)
        lines_count = read_model['NumOfRecords']
        con_id = read_model['ConId']
        read_con = read_collectionbyid("nnconnections", con_id)
        ConType = read_con['ConType']

        if (ConType == "1"):
            dir_path= read_con['FileLocation']
            #filestream(con_id,dir_path,lines_count)
            print("Reading DataSet Started")
            filestream(con_id,dir_path,lines_count,model_id)

        else:
            broker_endpoints = read_con['BrokerEndPoint']
            topics_list = read_con['TopicName']
            print(broker_endpoints)
            #kafkastream(con_id,broker_endpoints,topics_list,lines_count)
            print("Reading DataSet Started")
            raw_input_data = kafkastream(con_id,broker_endpoints,topics_list,lines_count)
            print("Reading DataSet Ended")
            print("Pre-Processing Data Started")
            Model_input_Data,text_field_LE,scaler,unique_val_list = pre_processing(raw_input_data)
            print("Pre-Processing Data Ended")
            print(Model_input_Data.head())
            print("Training Model Started")
            result,normal,abnormal = trainmodel(Model_input_Data)
            print("Training Model Ended")
            print(result.head(100))
            print("Post-Processing Data Started")
            final_result = postprocessing(Model_input_Data,abnormal,scaler,text_field_LE,unique_val_list)
            print("Post-Processing Data Ended")
            # print(normal.head(100))
            # print(final_result)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        logging.error("Model Created Failed:"+str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while making DB connection. Error Message <--> " + str(
                                                                         sys.exc_info())})
        raise
read_connection(sys.argv[1])