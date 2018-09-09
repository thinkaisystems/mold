from sklearn.model_selection import train_test_split
import AnomalyDetection as AD
import math
import pandas as pd
import logging
import os
from mongodb import read_collectionbyid
def stream_model(data_processed=pd.DataFrame(),model_id=''):
    Local_File_Path=os.path.dirname(os.path.realpath(__file__))
    MODEL_PATH=Local_File_Path+"/Model/model.h5"
    TB_LOG_DIR=Local_File_Path+"/TB"
    MODEL_SAVE_PATH=Local_File_Path+"/Model/model.json"
    OUT_PATH="/node-parser/data/Results/"
    RANDOM_STATE=77
    THRESHOLD=3 #2*STD away from mean will be
    logger=logging.getLogger(os.path.basename(__file__))
    #logger = __get_logger()
    db_record = read_collectionbyid('nnmodels',model_id)
    config_over_field_name = db_record['MainField']
    config_job_function = db_record['ModelType']
    config_job_sub_function = db_record['ModelMethod']
    X_test_index = data_processed.index
    test_columns = list(data_processed.columns)
    ix = test_columns.index(config_over_field_name)
    test = pd.DataFrame(data_processed.iloc[:, ix])
    if config_job_sub_function == 'NN':
        X_test=test.values.reshape(test.shape[0], 1)
        # Build the Model
        ad_obj = AD.AnomalyDetection(logger)
        #Load Model
        model=ad_obj.load_nn_model(MODEL_PATH,MODEL_SAVE_PATH)
        model=ad_obj.compile_nn_model(model)
        result = ad_obj.predict_nn_model(model, X_test)
        # ad_obj.plot_nn_result(THRESHOLD,error_df,test)
        normal, abnormal = ad_obj.export_nn_result(THRESHOLD, result, test, OUT_PATH)
        normal.set_index(X_test_index,inplace=True)
        abnormal.set_index(X_test_index,inplace=True)

    if config_job_sub_function == 'SVM':
        model=ad_obj.load_svm_model(MODEL_PATH)
        pred, result = ad_obj.predict_svm_model(model, test)
        #ad_obj.plot_svm_result(X_test, pred)
        normal, abnormal = ad_obj.export_svm_result(test, pred, OUT_PATH)
        normal.set_index(X_test_index,inplace=True)
        abnormal.set_index(X_test_index,inplace=True)

    #print(normal)
    return normal,abnormal



