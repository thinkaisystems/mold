# -*- coding: utf-8 -*-
#!/usr/bin/python
#%%
"""
Created on Thu Sep 14 10:47:10 2017

@author: vprayagala2

Purpose:
    This script is to read a json file and return pandas data frame
    Input: Json file with absolute path
    Output : Pandas Dataframe

Version History
1.0     -   First Version
"""
#%%
#Define Class/Functions
def read_data(file_name):
    import os as os
    import math
    import pandas as pd
    from time import time
    #Set the directory and file to be read
    if not os.path.exists(file_name):
        print("File Not Found, Please Input Absolute path for the file")
    else:
        file_stats=os.stat(file_name)
        if file_stats.st_size > 2*math.pow(10,9):
            print("Cannot Handle More than 2GB data currently")
    #Time at start of reading file        
    t0=time()
    data=pd.read_json(file_name,lines=True)
    print('='*80)
    print("File was read in %0.3fs" % (time() - t0))
    print('='*80)
    
    return data
    
def data_summary(data):
    print('='*80)
    print(data.shape)
    print(data.dtypes)
    print('='*80) 
    
def get_meta_data(file_name):
    import json
    df=get_sample_data(file_name,0,6)
    json_meta_data=json.dumps({"Column_Headers":list(df.columns)})
    return json_meta_data

def get_sample_data(file_name,start=0,end=100):
    #result=pd.DataFrame()
    import pandas as pd
    import json
    from itertools import islice
    if (end - start) > 1000:
        print("Cannot get Sample size grater than 1000 records\n")
    else:
        f=open(file_name)
        chunk = list(islice(f,start,end))
        #loading the json file content in data list
        if len(chunk) == 0:
            print("Invalid Start/End positions, cannot find data\n")
        else:
            data=[]
            for line in chunk:
                data.append(json.loads(line))
            df=pd.DataFrame.from_dict(data,orient='columns')
            #result=df.copy()
            return df
#%%
#Test Functions
#in_file="C:\\Data\\LogAnalysis\\nginx_json_logs.json"
#data=read_data("C:\\Data\\LogAnalysis\\nginx_json_logs.json")
#data_summary(data)
#col=get_metadata("C:\\Data\\LogAnalysis\\nginx_json_logs.json")
#print("Type:{}".format(type(col)))
#print(col)
#samp_data=get_sample_data(in_file)
#print(samp_data.head())
