# -*- coding: utf-8 -*-
#!/usr/bin/python
#%%
"""
Created on Thu Sep 14 11:32:40 2017

@author: vprayagala2

Purpose:
    This script is to pre-process Data Frame. It extracts the specific columns, converts types
    aggregates data, fills missing values
    
    Input: Pandas Data Frame
    Output : Processed Data Frame
    
Version History
1.0     -   First Version
"""
#%%
def pre_process_data(data):
    import pandas as pd
    #Extract the timestamp /Date 
    data['TS']=data.time.str[:20]
    data['TS'] = pd.to_datetime(data['TS'],format='%d/%b/%Y:%H:%M:%S')
    data['Date']=[d.date() for d in data['TS']]
    data['Hour']=[d.time().hour for d in data['TS']]
    data['Minute']=[d.time().minute for d in data['TS']]
    data['Seconds']=[d.time().second for d in data['TS']]
    return data

def encode_feature(data,feature):
    from sklearn.preprocessing import LabelEncoder
    
    le=LabelEncoder()
    
    new_col=str(feature)+"_Encoded"
    data[new_col]=le.fit_transform(data[feature])  
    
    return data,le

def decode_feature(data,feature,encoder):
   
    new_col=str(feature) + "_Decoded"
    data[new_col]=encoder.inverse_transform(data[feature])  
    
    return data

def extract_features(data,fields):
    from time import time
    #from sklearn.preprocessing import LabelEncoder
    
    t0=time()
    columns=data.columns
    columns_to_drop=[item for item in columns if item not in fields]
    data.drop(columns_to_drop,axis=1,inplace=True)
   
    #print("\nFeature Extraction Completed in %0.3fs" % (time() - t0))
    return data

def aggregate_data(data,agg_by,agg_over,agg_fun): 
    #Drop columns not required
    import pandas as pd
    from time import time
    
    t0=time()
    columns=data.columns
    data['DT'] = pd.to_datetime(data.Date) +data.Hour.astype('timedelta64[h]')+data.Minute.astype('timedelta64[m]')
    retain_columns=agg_by.copy()
    retain_columns.append('DT')
    retain_columns.append(agg_over)
    columns_to_drop=[item for item in columns if item not in retain_columns]
    data.drop(columns_to_drop,axis=1,inplace=True)
   
    #Apply the function on the required fields
    #print("\nGrouping Data on:{}".format(agg_on))
    print(data.dtypes)
    agg_columns=agg_by.copy()
    agg_columns.append('DT')
    print("Agg {} over {} by {}".format(agg_columns,agg_over,agg_fun))
    #dict1={agg_over:agg_fun}
    #print(dict1)
    processed_grp=data.groupby(by=agg_columns,as_index=False,sort=False)
    processed_agg=processed_grp[agg_over].agg(agg_fun).set_index('DT')
    #processed=pd.DataFrame({'Count':data.groupby(agg_on).size()}).reset_index(level=agg_on)
    #processed=pd.DataFrame({'Count':data.groupby(agg_on).size()}).reset_index(level=agg_on).set_index(['Date','Hour','Minute'])
    #processed=pd.DataFrame({'Count':data.groupby(agg_by).agg({agg_over:agg_fun})})
    #processed=processed_agg.reset_index(level=['DT']).set_index(['DT'])
    #processed.sort_values('Count',axis=0,ascending=False,inplace=True)
    #processed.drop(['Hour','Minute'],axis=1,inplace=True)
    
    #print('='*80)
    #print("Top Rows:")
    #print(processed.head())
    #print("Pre-Processing Completed in %0.3fs" % (time() - t0))
    
    return processed_agg

def aggregate_data_ts(data,fields,agg_on): 
    #Drop columns not required
    import pandas as pd
    from time import time
    
    t0=time()
    columns=data.columns
    columns_to_drop=[item for item in columns if item not in fields]
    data.drop(columns_to_drop,axis=1,inplace=True)
    
    if agg_on == 'Date':
        data['DT'] = pd.to_datetime(data.Date)
    if agg_on == 'Hour':
        data['DT'] = pd.to_datetime(data.Date) +data.Hour.astype('timedelta64[h]')
 
    if agg_on == 'Minute':
        data['DT'] = pd.to_datetime(data.Date) +data.Hour.astype('timedelta64[h]')+data.Minute.astype('timedelta64[m]')
    if agg_on == 'Seconds':
        data['DT'] = pd.to_datetime(data.Date) +data.Hour.astype('timedelta64[h]')+data.Minute.astype('timedelta64[m]') +data.Seconds.astype('timedelta64[s]')

    print(data.head())
    data.drop(['Date','Hour','Minute','Seconds'],axis=1,inplace=True)
    processed=pd.DataFrame({'Count':data.groupby('DT').size()}).reset_index(level=['DT']).set_index(['DT'])
    
    
    return processed

def split_data(data,test_size,seed):
    from sklearn.model_selection import train_test_split
    X_train, X_test = train_test_split(data, test_size=test_size, random_state=seed)
    return X_train,X_test
#%%
#Custom Classes/Modules
#import Read_Json_File as RJF
#import pandas as pd
#data=RJF.read_data("C:\\Data\\LogAnalysis\\nginx_json_logs.json")
#RJF.data_summary(data)
##data_source=pd.DataFrame(data._source.values.tolist())
#data=pre_process_data(data)
#data_feat=extract_features(data,fields=['bytes','remote_ip','request','response',
#                                        'Date','Hour','Minute','Seconds'])
#data_agg=aggregate_data(data_feat,agg_on=['Date','Hour','Minute','remote_ip','response'],agg_fun=['size'])

