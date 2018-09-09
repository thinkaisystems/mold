# -*- coding: utf-8 -*-
#!/usr/bin/python
#%%
"""
Created on Fri Oct 06 10:47:10 2017

@author: ThinakAI

Purpose:
    This script is to read json records from kafka brokers in chunks based on realtime data
    Input: Kafka borkers endpoints, topic name and no.of line to read as a chunk
    Output : JSON records

Version History
2.0     -   Second Version
"""

import logging
import traceback
import os
import sys
import json
import pandas as pd
import re
from kafka import KafkaConsumer, KafkaClient, TopicPartition, OffsetAndMetadata
from Getfieldslist import get_fieldtype
from mongodb import update_collection
from bson.objectid import ObjectId
from Json_Table_Parsing import convert_table
from pandas.io.json import json_normalize

class StreamConsumer:
    def __init__(self, cfg, group_id=None):
        self.config = cfg
        self.group_id = group_id
        self.consumer = None

    # create logger
    def __get_logger(self):
        """Instantiates logger."""
        return logging.getLogger(os.path.basename(__file__))

    def consume(self, con_id, topics, lines_count, auto_offset='earliest', *args ):
        try:
            count = 0
            isContinue = True
            raw_input_data = pd.DataFrame()
            error_count = 0

            logger = self.__get_logger()
            conf = {
                'bootstrap_servers': ','.join(map(str, self.config.get('hosts'))),
                'group_id': con_id,
                'auto_offset_reset': auto_offset,
                'enable_auto_commit': False,
                'max_partition_fetch_bytes' : 100000,
                'heartbeat_interval_ms' : 10000,
                'consumer_timeout_ms': 30000,
                #'group_min_session_timeout_ms' : 300000,
                #'session_timeout_ms' : 30000,
                'request_timeout_ms': 400000
                #'group_max_session_timeout_ms' : 300000
                # 'max_poll_records': 5,
            }
            try:
                consumer = KafkaConsumer(**conf)
                print("Made Kafka Consumer Connection Successfully")
            except:
                logger.error(("Error creating Consumer with config [{}]".format(conf)))
                raise

            try:
                consumer.subscribe(topics)
            except:
                logger.error("Error subscribing to topics [{}]".format(topics))
                consumer = None
                raise
            df_l = []
            dic_l = []

            while isContinue:
                try:
                    logger.info("Starting to poll topics [{}]...".format(topics))
                    for msg in consumer:
                        count += 1
                        topicPartition = TopicPartition(msg.topic, msg.partition)
                        consumer.commit({topicPartition: OffsetAndMetadata(msg.offset + 1, '')})
                        #print("\r Records Read... " + str(count), end="")
                        #print(msg.value.decode('utf-8').replace("'", '"'))

                        if lines_count == 1:
                            get_fieldtype(con_id,msg.value.decode('utf-8').replace("'", '"'))
                            #print(type(msg.value))
                            #print("Original",msg.value.decode('utf-8').replace("'", '"'))

                        try:
                                    s = msg.value.decode('utf-8').replace("'", '"')
                                    result = json.loads(s)  # try to parse...
                                    #print("Parsing..")
                                    value,typ = convert_table(s, count)
                                    if typ == 'dict':
                                        dic_l.append(value)
                                    else:
                                        df_l.append(value)
                                    print("\r Records Read... "+str(count), end="")
                                    count += 1
                                    #print("Original",raw_input_data)
                                    #print("Original",raw_input_data.head())
                                    #print("Original",raw_input_data.shape)
                                    #break  # parsing worked -> exit loop

                        except Exception as e:
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
                                    #res.strip('\'"')
                                    #print("Formatted String", str(res))
                                    value,typ = convert_table(res, count)
                                    if typ == 'dict':
                                        dic_l.append(value)
                                    else:
                                        df_l.append(value)
                                    count+=1
                                    #print("Formatted",raw_input_data)
                                    #print("Formatted",raw_input_data.head())
                                    #print("Formatted",raw_input_data.shape)
                        except:
                            error_count+=1
                            logging.error("Errror while parsing json"+str(sys.exc_info()))

                except:
                    logger.error("Error polling messages.")
                    raise

            if len(dic_l) > 0 and len(df_l) > 0:
                        raw_input_data_dic = json_normalize(dic_l,sep='~')
                        raw_input_data_df = pd.concat(df_l,axis=0)
                        raw_input_data = raw_input_data_dic.append(raw_input_data_df,ignore_index=False)
            elif len(df_l) > 0:
                        raw_input_data = pd.concat(df_l,axis=0)
            elif len(dic_l) > 0:
                        raw_input_data = json_normalize(dic_l,sep='~')
            # end while running loop

            return raw_input_data

        except Exception:
            logger.error("Error consuming topics [{}]".format(topics))
            logger.debug(traceback.format_exc())
            raise

def kafkastream(con_id,broker_endpoints,topics_list,lines_count):
    try:
        logging.basicConfig(level=logging.INFO)

        brokers = {
        "hosts": [broker_endpoints]
        }

        topics_list = [topics_list]
        lines_count = lines_count
        consumer = StreamConsumer(brokers)
        consumer.consume(con_id, topics_list, lines_count, auto_offset='earliest')

    except:
        logging.error("Unable to make connection.." + str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while making connection. Error Message <--> " + str(
                                                                         sys.exc_info())})

def onerecord(con_id,broker_endpoints,topics_list,lines_count):
    try:
        logging.basicConfig(level=logging.INFO)

        brokers = {
        "hosts": [broker_endpoints]
        }

        topics_list = [topics_list]
        lines_count = lines_count
        consumer = StreamConsumer(brokers)
        consumer.consume(con_id,topics_list, lines_count, auto_offset='earliest')

    except:
        logging.error("Unable to make connection.." + str(sys.exc_info()))
        update_collection("nnconnections", "_id", ObjectId(con_id), {"Status": "Failed",
                                                                     "Error_Message": "Creating connection got error while making connection. Error Message <--> " + str(
                                                                         sys.exc_info())})

if __name__ == '__kafkastream__':
    kafkastream()

if __name__ == '__onerecord__':
    onerecord()

#onerecord()
#kafkastream()