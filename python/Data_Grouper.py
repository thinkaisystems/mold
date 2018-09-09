import pandas as pd
from mongodb import read_collectionbyid
from pandas.io.json import json_normalize
import pendulum as pen
import time
from time import mktime
from datetime import datetime
from Streaming_Pre_Processing import pre_processing
from Streaming_Post_Processing import  postprocessing
from mongodb import read_collectionbyid
from Stream_Model import stream_model

def data_grouper(Data,typ,span_timestamp,model_id,df_l,dic_l,TimeSeriesField,IntervalSpan):

    if IntervalSpan != None:
        pd_t = pd.DataFrame()
        if span_timestamp == None:
            if typ == 'dict':
                #print(Data[TimeSeriesField])
                #print(type(Data[TimeSeriesField]))
                try:
                    pd_t['time'] = pd.date_range( pen.parse(Data[TimeSeriesField]), periods=2, freq=IntervalSpan)
                except:
                    pd_t['time'] = pd.date_range( datetime.fromtimestamp(mktime(time.strptime(Data[TimeSeriesField], '%d/%b/%Y:%H:%M:%S %z'))), periods=2, freq=IntervalSpan)
            else:
                try:
                    pd_t['time'] = pd.date_range( pen.parse(Data.iloc[0][TimeSeriesField]), periods=2, freq=IntervalSpan)
                except:
                    pd_t['time'] = pd.date_range( datetime.fromtimestamp(mktime(time.strptime(Data.iloc[0][TimeSeriesField], '%d/%b/%Y:%H:%M:%S %z'))), periods=2, freq=IntervalSpan)
            #print(pd_t.iloc[1]['time'])
            span_timestamp =  pd_t.iloc[1]['time']

        if typ == 'dict':
                try:
                    current_time = pen.parse(Data[TimeSeriesField])
                except:
                   current_time = datetime.fromtimestamp(mktime(time.strptime(Data[TimeSeriesField], '%d/%b/%Y:%H:%M:%S %z')))
        else:
                try:
                    current_time = pen.parse(Data.iloc[0][TimeSeriesField])
                except:
                    current_time = datetime.fromtimestamp(mktime(time.strptime(Data.iloc[0][TimeSeriesField], '%d/%b/%Y:%H:%M:%S %z')))

        if current_time > span_timestamp:
            #print("Start : " + str(datetime.now()))
            raw_input_data = pd.DataFrame()
            if len(dic_l) > 0 and len(df_l) > 0:
                raw_input_data_dic = json_normalize(dic_l,sep='~')
                raw_input_data_df = pd.concat(df_l,axis=0)
                raw_input_data = raw_input_data_dic.append(raw_input_data_df,ignore_index=False)
            elif len(df_l) > 0:
                raw_input_data = pd.concat(df_l,axis=0)
            elif len(dic_l) > 0:
                raw_input_data = json_normalize(dic_l,sep='~')
            #print(raw_input_data)
            Model_input_Data,text_field_LE,scaler = pre_processing(raw_input_data,model_id)
            normal,abnormal = stream_model(Model_input_Data,model_id)
            postprocessing(Model_input_Data,abnormal,scaler,text_field_LE,model_id)

            dic_l = []
            df_l = []
            span_timestamp = None

        if typ == 'dict':
            dic_l.append(Data)
        else:
            df_l.append(Data)
    else:
        raw_input_data = pd.DataFrame()
        if typ == 'dict':
            raw_input_data = json_normalize(Data,sep='~')
        else:
            raw_input_data = pd.concat(Data,axis=0)
        #print(raw_input_data)
        Model_input_Data,text_field_LE,scaler = pre_processing(raw_input_data,model_id)
        normal,abnormal = stream_model(Model_input_Data,model_id)
        postprocessing(Model_input_Data,abnormal,scaler,text_field_LE,model_id)

    return span_timestamp,df_l,dic_l
