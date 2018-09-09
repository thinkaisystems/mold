# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 22:10:12 2017

@author: dadmrbalakrishnan
"""

import pandas as pd
import string
import time
import numpy as np
from time import mktime
from datetime import datetime
import pendulum as pen
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from mongodb import read_collectionbyid
from mongodb import read_collectionbyfield

def pre_processing(raw_input_data=pd.DataFrame(),model_id=''):
    db_record = read_collectionbyid('nnmodels',model_id)
    if db_record['TrainConId'] == '':
        con_id = db_record['ConId']
    else:
        con_id = db_record['TrainConId']
    field_list = read_collectionbyfield('nnfieldslist','Con_id',con_id)
    fiel_l = field_list['Field_list'].split('|')
    fiel_t = field_list['Field_Type_List'].split('|')
    #print(fiel_l)
    field_type = {}
    for i in range(len(fiel_l)):
        field_type[fiel_l[i]] = fiel_t[i]
    Main_Field = db_record['MainField']
    Main_Field_Type = field_type[Main_Field]
    Time_Field = db_record['TimeSeriesField']
    filter = ''
    filter_value = 200.02
    filter_value1 = 0
    Inf_Field = []
    IntervalSpan = db_record['IntervalSpan'].replace('~','')
    if IntervalSpan == '' : IntervalSpan = None
    for x in db_record['FieldsSelected'].split(','):
        Inf_Field.append(x)
    fun = db_record['AggregationFun']
    text_field_list = []
    unique_val_list = {}
    #print(raw_input_data.head())
    for Field in Inf_Field:
        unique_val_list[Field] = str(list(raw_input_data[Field].unique()))
        if field_type[Field] == 'str':
            text_field_list.append(Field)
    def lencoder(data,feature):
        le=LabelEncoder()
        new_col=str(feature)+"_Encoded"
        data[new_col]=le.fit_transform(data[feature].astype(str))
        #print(le.inverse_transform(data[new_col]))
        data.drop(feature,axis=1,inplace=True)
        return data,le
    def minmaxscaler(data,time_field):
        scaler = MinMaxScaler(copy=False, feature_range=(0, 1))
        data.set_index(time_field,inplace=True)
        data_index = data.index
        #data.drop(time,axis=1,inplace=True)
        #print(data.columns)
        data = pd.DataFrame(scaler.fit_transform(data),columns=data.columns)
        data.set_index(data_index,inplace=True)
        return data,scaler
    raw_input_data = raw_input_data[list([Time_Field,Main_Field])+Inf_Field]
    #raw_input_data = raw_input_data.filter()
    raw_input_data = raw_input_data.replace('', np.nan, inplace=False)
    raw_input_data = raw_input_data.dropna(inplace=False,axis=0)
    if Main_Field_Type == 'int' or Main_Field_Type == 'float':
        raw_input_data[Main_Field] = pd.to_numeric(raw_input_data[Main_Field], errors='coerce')
    if filter == '=':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] == filter_value]
    elif filter == '!=':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] != filter_value]
    elif filter == '>':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] > filter_value]
    elif filter == '<':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] < filter_value]
    elif filter == '>=':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] >= filter_value]
    elif filter == '<=':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] <= filter_value]
    elif filter == 'like':
        raw_input_data = raw_input_data[raw_input_data[Main_Field].str.contains(filter_value)]
    elif filter == 'btw':
        raw_input_data = raw_input_data[raw_input_data[Main_Field] >= filter_value & raw_input_data[Main_Field] <= filter_value1]

    #print(raw_input_data)

    try :
        raw_input_data[Time_Field] = raw_input_data[Time_Field].apply(lambda x: pen.parse(x))
    except:
        raw_input_data[Time_Field] = raw_input_data[Time_Field].apply(lambda x: datetime.fromtimestamp(mktime(time.strptime(x, '%d/%b/%Y:%H:%M:%S %z'))))
    #raw_input_data[Time_Field] = pd.to_datetime(raw_input_data[Time_Field],format='%d/%b/%Y:%H:%M:%S %z')
    #print(raw_input_data.columns)
    #raw_input_data[Time_Field]=raw_input_data[Time_Field].apply(lambda x: datetime.datetime.strftime(x))
    #raw_input_data['time1'] = raw_input_data[Time_Field].apply(lambda x: dateparser.parse(x))
    if (fun == 'sum'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.sum, axis=0).reset_index()
    if (fun == 'count'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].agg('count').reset_index()
    if (fun == 'average'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.average, axis=0).reset_index()
    if (fun == 'mean'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.mean, axis=0).reset_index()
    if (fun == 'median'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.median, axis=0).reset_index()
    if (fun == 'product'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.prod, axis=0).reset_index()
    if (fun == 'maximum'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.max, axis=0).reset_index()
    if (fun == 'maximum'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.min, axis=0).reset_index()
    if (fun == 'cumsum'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.cumsum, axis=0).reset_index()
    if (fun == 'cumprod'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].apply(np.cumprod, axis=0).reset_index()
    if (fun == 'cumsum'):
        Grouped_input_data = raw_input_data.sort_values(Time_Field,ascending=True).groupby(list([pd.Grouper(key=Time_Field, freq=IntervalSpan)])+Inf_Field)[Main_Field].cumsum().reset_index()

    #raw_input_data.replace('', np.nan, inplace=True)
    #print(Grouped_input_data)
    #raw_input_data.fillna(method='ffill')
    text_field_LE = {}
    for tx_f in text_field_list:
        Encoded_input_data,text_field_LE[tx_f] = lencoder(Grouped_input_data,tx_f)
    #print(Encoded_input_data)
    #print(Encoded_input_data)
    Model_input_Data,scaler = minmaxscaler(Encoded_input_data,Time_Field)
    #print(Model_input_Data)
    #print(scaler)
    #print(datetime)
    return Model_input_Data,text_field_LE,scaler,unique_val_list