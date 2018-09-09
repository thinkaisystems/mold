from file_connector import onerecord as file_con_onerecord, filestream
from kafka_connector import onerecord, kafkastream
from sys import argv
import logging
import datetime
import os
import sys
from mongodb import read_collectionbyid, update_collection
from bson.objectid import ObjectId
from Pre_Processing import pre_processing
from  Train_Model import trainmodel
from Post_Processing import  postprocessing
from mongodb import read_collectionbyid
import numpy as np

# create logger
def __get_logger(self):
    """Instantiates logger."""
    return logging.getLogger(os.path.basename(__file__))

def read_connection(model_id):
    #try:
        read_model = read_collectionbyid("nnmodels", model_id)
        lines_count = read_model['NumOfRecords']
        TrainConId = read_model['TrainConId']

        if TrainConId == "":
            TrainConId = read_model['ConId']
        read_con = read_collectionbyid("nnconnections", TrainConId)
        ConType = read_con['ConType']
        if (ConType == "1"):
            dir_path= read_con['FileLocation']
            print("Reading DataSet Started")
            raw_input_data = filestream(TrainConId,dir_path,lines_count)

        else:
            broker_endpoints = read_con['BrokerEndPoint']
            topics_list = read_con['TopicName']
            #print(broker_endpoints)
            raw_input_data = kafkastream(TrainConId,broker_endpoints,topics_list,lines_count)

        print("Reading DataSet Ended")
        print("Pre-Processing Data Started")
        Model_input_Data,text_field_LE,scaler,unique_val_list = pre_processing(raw_input_data,model_id)
        print("Pre-Processing Data Ended")
        print("Training Model Started")
        result,normal,abnormal = trainmodel(Model_input_Data,model_id)
        print("Training Model Ended")
        print("Post-Processing Data Started")
        postprocessing(result,abnormal,scaler,text_field_LE,unique_val_list,model_id)
        print("Post-Processing Data Ended")

    #except:
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        #logging.error("Model Created Failed:"+str(sys.exc_info()))
        #update_collection("nnconnections", "_id", ObjectId(TrainConId), {"Status": "Failed",
        #                                                             "Error_Message": "Model Creation Failed. Error Message <--> " + str(
        #                                                                 sys.exc_info())})
read_connection(sys.argv[1])