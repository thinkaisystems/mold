from file_connector import onerecord as file_con_onerecord, filestream
from kafka_connector import onerecord, kafkastream
from sys import argv
import logging
import os
import sys
from mongodb import read_collectionbyid, update_collection
from bson.objectid import ObjectId

# create logger
def __get_logger(self):
    """Instantiates logger."""
    return logging.getLogger(os.path.basename(__file__))

def read_connection(con_id):
    try:
        read_counters = read_collectionbyid("nnconnections", con_id)
        #print(read_counters)
        con_type = read_counters['ConType']

        if (con_type == "1"):
            dir_path= read_counters['FileLocation']
            #lines_count = read_counters['NoOfRecords']
            file_con_onerecord(con_id,dir_path,lines_count=1)

        else:
            broker_endpoints = read_counters['BrokerEndPoint']
            topics_list = read_counters['TopicName']
            #lines_count = read_counters['NoOfRecords']
            onerecord(con_id,broker_endpoints,topics_list,lines_count=1)
    except:
        logging.error("Unable to read connection details from DB.."+str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while making DB connection. Error Message <--> " + str(
                                                                         sys.exc_info())})


print(sys.argv[1])
read_connection(sys.argv[1])
