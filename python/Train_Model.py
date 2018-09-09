from sklearn.model_selection import train_test_split
import AnomalyDetection as AD
import math
import pandas as pd
import logging
import os
from mongodb import read_collectionbyid
def trainmodel(data_processed=pd.DataFrame(),model_id=''):
    Local_File_Path=os.path.dirname(os.path.realpath(__file__))
    MODEL_PATH=Local_File_Path+"/Model/model.h5"
    MODEL_SAVE_PATH=Local_File_Path+"/Model/model.json"
    TB_LOG_DIR=Local_File_Path+"/TB/"+model_id+"/"
    if not os.path.exists(TB_LOG_DIR):
       os.makedirs(TB_LOG_DIR)
       os.chmod(TB_LOG_DIR,0o755) 
    OUT_PATH="/node-parser/data/Results/"
    RANDOM_STATE=77
    THRESHOLD=3 #2*STD away from mean will be
    logger=logging.getLogger(os.path.basename(__file__))
    #logger = __get_logger()
    db_record = read_collectionbyid('nnmodels',model_id)
    config_over_field_name = db_record['MainField']
    config_job_function = db_record['ModelType']
    config_job_sub_function = db_record['ModelMethod']

    if config_job_function == 'anomaly':
        # Split data into train/test
        test_columns = list(data_processed.columns)
        ix = test_columns.index(config_over_field_name)
        train, test = train_test_split(data_processed, \
                                       test_size=0.2, \
                                       random_state=77)
        X_test_pd = pd.DataFrame(test)
        #print('split')
        #print(X_test_pd)
        X_train = pd.DataFrame(train.iloc[:, ix])
        X_test = pd.DataFrame(test.iloc[:, ix])
        X_test_index = X_test.index

        # Build the Model
        ad_obj = AD.AnomalyDetection(logger)

        if config_job_sub_function == 'NN':
            X_train = X_train.values.reshape(X_train.shape[0], 1)
            X_test = X_test.values.reshape(X_test.shape[0], 1)
            encoding_dim = int(math.log(X_train.shape[0]))
            input_dim = X_train.shape[1]
            nn_model = ad_obj.build_nn_model(encoding_dim, input_dim)
            nn_model = ad_obj.compile_nn_model(nn_model)
            # Run Model
            nb_epoch = int(math.pow(X_train.shape[0], 3 / 5))
            batch_size = int(math.sqrt(X_train.shape[0]))
            nn_model, history = ad_obj.run_nn_model(nn_model, X_train, X_test,
                                                    nb_epoch,
                                                    batch_size,
                                                    MODEL_PATH,
                                                    TB_LOG_DIR,
                                                    )

            # Visualize Training History
            # ad_obj.depict_nn_training_hist(history)
            ad_obj.save_nn_model(nn_model,MODEL_SAVE_PATH)
            nn_history_file = OUT_PATH + "nn_history.json"
            ad_obj.export_nn_training_result(history, nn_history_file)
            result = ad_obj.predict_nn_model(nn_model, X_test)
            result.set_index(X_test_index,inplace=True)
            # ad_obj.plot_nn_result(THRESHOLD,error_df,test)
            normal, abnormal = ad_obj.export_nn_result(THRESHOLD, result, test, OUT_PATH)
            normal.set_index(X_test_index,inplace=True)
            abnormal.set_index(X_test_index,inplace=True)

        if config_job_sub_function == 'SVM':
            svm_model=ad_obj.build_svm_model(X_train)
            ad_obj.save_svm_model(MODEL_PATH)
            pred,result=ad_obj.predict_svm_model(svm_model,X_test)
            result.set_index(X_test_index,inplace=True)
            #ad_obj.plot_svm_result(X_test,pred)
            normal,abnormal=ad_obj.export_svm_result(X_test,pred,OUT_PATH)
            normal.set_index(X_test_index,inplace=True)
            abnormal.set_index(X_test_index,inplace=True)


    # test_columns = list(data_processed.columns)
    # ix = test_columns.index(config_over_field_name)
    # test = pd.DataFrame(data_processed.iloc[:, ix])
    # if config_job_sub_function == 'NeuralNet':
    #     X_test=test.values.reshape(X_test.shape[0], 1)
    #     # Build the Model
    #     ad_obj = AD.AnomalyDetection(logger)
    #     #Load Model
    #     model=ad_obj.load_nn_model(MODEL_PATH)
    #     model=ad_obj.compile_nn_model(model)
    #     result = ad_obj.predict_nn_model(nn_model, X_test)
    #     # ad_obj.plot_nn_result(THRESHOLD,error_df,test)
    #     normal, abnormal = ad_obj.export_nn_result(THRESHOLD, result, test, OUT_PATH)
    #
    # if config_job_sub_function == 'SVM':
    #     model=ad_obj.load_svm_model(MODEL_PATH)
    #     pred, result = ad_obj.predict_svm_model(svm_model, test)
    #     ad_obj.plot_svm_result(X_test, pred)
    #     normal, abnormal = ad_obj.export_svm_result(test, pred, OUT_PATH)

    return X_test_pd,normal,abnormal



