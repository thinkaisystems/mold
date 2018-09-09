import pandas as pd
import string
import time
import numpy as np
from time import mktime
from datetime import datetime
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from mongodb import append_collection
from mongodb import read_collectionbyid
import json
def postprocessing(data=pd.DataFrame(),abnormal=pd.DataFrame(),scaler= MinMaxScaler(copy=True, feature_range=(0, 1)),text_field_LE={},model_id=''):
    data_index = data.index
    db_record = read_collectionbyid('nnmodels',model_id)
    Scaler_deco_data = pd.DataFrame(scaler.inverse_transform(data),columns=data.columns)
    Scaler_deco_data.set_index(data_index,inplace=True)
    #print('shape')
    #print(Scaler_deco_data.dtypes)

    def ldecoder(data,feature='',le=LabelEncoder()):
        #print(data.dtypes)
        new_col=str(feature)+"_Encoded"
        #print(new_col)
        data[feature]=le.inverse_transform(data[new_col].astype('int'))
        data.drop(new_col,axis=1,inplace=True)
        return data

    for key,tx_f in text_field_LE.items():
        #print(tx_f)
        data = ldecoder(Scaler_deco_data,key,tx_f)
    abnormal.loc[abnormal['Actual'].notnull(),'Actual'] = 'YES'
    #abnormal['Actual'].set_value(abnormal['Actual'].notnull(),value='YES')
    abnormal['Actual'].fillna('NO', inplace=True)
    #print([data,abnormal['Actual']])
    #print(data)
    df_result = pd.concat([data,abnormal['Actual']], axis=1,copy=False)
    df_result.reset_index(level=0, inplace=True)
    df_result.sort_values(db_record['MainField'],inplace=True)
    result_json = df_result.to_json(orient='records')
    #result_json = json.loads(result_json)
    #insert_record = {}
    #insert_record["Timestamp"] = datetime.now()
    #insert_record["Model_id"] = model_id
    #insert_record["Result"] = result_json
    #insert_record.update(unique_val_list)
    #print(type(insert_record))
    #print(result_json)
    append_collection("nnresults", 'S_Model_id',model_id, 'Result',result_json)
    #print(result_json)