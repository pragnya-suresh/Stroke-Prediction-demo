import os
from flask import Flask, flash, request, redirect, url_for, jsonify,json
import requests
from flask_cors import CORS, cross_origin
from flask import Response
from flask import jsonify
from sklearn.neighbors import NearestNeighbors
import csv
import random
import time
import os
import pandas as pd
import numpy as np
import joblib
import json

app = Flask(__name__)

CORS(app, support_credentials=True)

df = pd.read_csv("final.csv" ,error_bad_lines=False)

df_transformed = pd.read_csv("final_transformed.csv" ,error_bad_lines=False)
df_stddev = pd.read_csv("std_dev.csv" ,error_bad_lines=False)
model = joblib.load('model.pkl')


# creating the record.csv if it does not exist
file_exists = os.path.isfile('record.csv')

if not file_exists:
    print("Creating new record.csv")
    #cols = ['nsrrid', 'ventrate', 'qrs', 'avcanba', 'avcanoa', 'avcarbp2', 'avcaroa2', 'avcanoa3', 'avcaroa4', 'avcanba5', 'oaroa5', 'estrgn1', 'lipid1', 'minfa10', 'cgrtts10', 'climb125', 'wksblk25', 'wk1blk25', 'bathe25', 'rawpf_s1', 'rawgh_s1', 'rawvt_s1', 'mh_s1', 'age_s1', 'stroke']
    cols = ['nsrrid','ventrate','qrs','avhnoa3','oaroa5','systbp','diasbp','rest10','minfa10','shots10','cgrtts10','modact25','lift25','climbs25','climb125','wksblk25','wk1blk25','bathe25','hlthlm25',
            'rawpf_s1','pf_s1','rawbp_s1','rawgh_s1','gh_s1','rawvt_s1','mh_s1','pcs_s1','mcs_s1','age_s1','bmi_s1','weight','height','stroke']
    with open('record.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(cols)



#Run this block only once and then comment
# cols = ["id","timestamp"]
# cols.append(df.columns.tolist())
# with open('record.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(cols)

@app.route('/register_patient', methods=['GET', 'POST'])
def get_registration_variables():
    """ Needs to return {vars: list1, descriptions: list2}
    """
    # l = ['nsrrid', 'ventrate', 'qrs', 'avcanba', 'avcanoa', 'avcarbp2', 'avcaroa2', 'avcanoa3', 'avcaroa4', 'avcanba5', 'oaroa5', 'estrgn1', 'lipid1', 'minfa10', 'cgrtts10', 'climb125', 'wksblk25', 'wk1blk25', 'bathe25', 'rawpf_s1', 'rawgh_s1', 'rawvt_s1', 'mh_s1', 'age_s1']
    
    categorical = ['wksblk25', 'wk1blk25', 'climb125', 'bathe25', 'rest10', 'modact25', 'lift25', 'climbs25', 'hlthlm25']
    breathing = ['avhnoa3', 'oaroa5']
    observed = ['systbp', 'diasbp', 'minfa10', 'cgrtts10', 'shots10', 'bmi_s1', 'weight', 'height', 'age_s1']
    calculated = ['rawpf_s1', 'rawgh_s1', 'rawvt_s1', 'rawbp_s1', 'mh_s1', 'pf_s1', 'gh_s1', 'pcs_s1', 'mcs_s1']
    ecg = ['ventrate', 'qrs']

    categorical_desc = ['Health limits walking several blocks', 'Health limits walking a single block',
                    'Health limits climbing a flight of stairs', 'Health limits bathing and dressing',
                    'Quality of sleep: restless/restful', 'Moderate activities, such as moving a table, pushing a vacuum cleaner, bowling, or playing golf',
                    'Health limits Lifting or carrying groceries', 'Health limits climbing several flights of stairs', 'Health limited your social activities']
    breathing_desc = ['Average Hypopnea length with >=3\% oxygen desaturation or arousal (Non-rapid eye movement sleep (NREM), Non-supine)', 
                    'Number of Obstructive Apnea with >=5\% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)']
    observed_desc = ['Seated Systolic Blood Pressure', 'Seated Diastolic Blood Pressure','Minutes taken to fall asleep the previous night','How many cigarettes 4 hours before going to\
                sleep last night?', 'How many mixed drinks or shots of liquor 4 hours before going to sleep last night?', 'Body mass index', 'Weight in kilograms', 'Height in centimeters', 
                'Age at time of test']
    calculated_desc = ['Physical Functioning Raw Score', 'General Health Perceptions Raw Score', 'Vitality Raw Score', 'Pain Index Raw Score', 'Mental Health Index Standardized Score',
                    'Physical Functioning Standardized Score', 'General Health Perceptions Standardized Score', 'Physical Component Scale Standardized Score', 'Mental Component Scale Standardized Score']
    ecg_desc = ['Ventricular rate', 'QRS axis']

    # # No Stroke default values
    # categorical_default = ['0.0', '0.0', '0.0', '0.0', '0.0', '3.0', '2.0', '0.0', '4.0']
    # breathing_default = ['25.0', '20.0']
    # observed_default = ['132.0', '65.0', '10.0', '0.0', '0.0', '33.44', '103.0', '174.0', '77']
    # calculated_default = ['28.88', '22.44', '18.0', '9.4', '76.0', '94.44', '87.0', '54.26', '54.01']
    # ecg_default = ['55.0', '103.0']

    # Stroke default values
    categorical_default = ['2.0', '3.0', '0.0', '3.0', '3.0', '1.0', '2.0', '1.0', '2.0']
    breathing_default = ['20.5', '0.0']
    observed_default = ['114.0', '80.0', '28.61048689138580', '1.0', '0.0', '22.191956417', '63.4', '174.0', '77']
    calculated_default = ['16.666666667', '15.0', '8.0', '6.2', '56.0', '33.333333333', '50.0', '32.146072659', '35.69566048']
    ecg_default = ['59.0','31.0']

    l = ['nsrrid'] + categorical + breathing + observed + calculated + ecg
    descriptions = ['NSRR Subject ID'] + categorical_desc + breathing_desc + observed_desc + calculated_desc + ecg_desc
    defaults = ['1'] + categorical_default + breathing_default + observed_default + calculated_default + ecg_default

    if request.method == 'GET':
        
        # descriptions = ['NSRR Subject ID', 'Ventricular rate', 'QRS Axis', 'Average Central Apnea length w/ arousals (Non-rapid eye movement sleep (NREM), Supine, all oxygen desaturations)', 'Average Central Apnea length w/ arousals (Non-rapid eye movement sleep (NREM), Non-supine, all oxygen desaturations)', 'Average Central Apnea length (Rapid eye movement sleep (REM), Supine, >=2% oxygen desaturation)', 'Average Central Apnea length with >=2% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Average Central Apnea length with >=3% oxygen desaturation or arousal (Non-rapid eye movement sleep (NREM), Non-supine)', 'Average Central Apnea length with >=4% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Average Central Apnea length with >=5% oxygen desaturation or arousal (Non-rapid eye movement sleep (NREM), Supine)', 'Number of Obstructive Apnea with >=5% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Estrogens, Excluding Vaginal Creams ', 'Any Lipid-Lowering Medication ', 'Morning Survey : minutes to fall asleep', 'Morning Survey : cigarettes before bed', 'Quality of Life (QOL) : Health limits climbing one flight of stairs', 'Quality of Life (QOL) : Health limits walking several blocks', 'Quality of Life (QOL) : Health limits walking one block', 'Quality of Life (QOL) : Health limits bathing and dressing', 'Short Form 36 Health Survey (SF-36) Calculated : Physical Functioning Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : General Health Perceptions Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : Vitality Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : Mental Health Index Standardized Score', 'Age at Sleep Heart Health Study Visit One (SHHS1)']
        
        d = {'registration_variables': l, 'descriptions':descriptions, 'defaults': defaults}

        return jsonify(d), 200
    
    elif request.method == 'POST':
        # user_data = request.get_json(force=True)
        # print(user_data)
        l = ['nsrrid','ventrate','qrs','avhnoa3','oaroa5','systbp','diasbp','rest10','minfa10','shots10','cgrtts10','modact25','lift25','climbs25','climb125','wksblk25','wk1blk25','bathe25','hlthlm25',
            'rawpf_s1','pf_s1','rawbp_s1','rawgh_s1','gh_s1','rawvt_s1','mh_s1','pcs_s1','mcs_s1','age_s1','bmi_s1','weight','height']
        user_data = dict()
        values = []
        for i in l:
            user_data[i] = request.form[i]
            values.append(float(request.form[i]))

        attributes = np.array(values[1:])
        attributes = attributes.reshape(1,-1)
        result = model.predict(attributes)[0]
        user_data['stroke'] = result

        values.append(result)
        df_record = pd.read_csv('record.csv')
        row_index = df_record.shape[0]

        df_record.loc[row_index] = values

        df_record.to_csv('record.csv', index=False)

        return jsonify(user_data), 201
    else:
        return jsonify(), 405

@app.route('/graph_buttons', methods=['GET'])
def get_graph_buttons():
    l = ['ventrate','qrs','avhnoa3','oaroa5','systbp','diasbp','rawpf_s1','pf_s1','rawbp_s1','rawgh_s1','gh_s1','rawvt_s1','mh_s1','pcs_s1','mcs_s1','bmi_s1','weight']
    if request.method == 'GET':
        
        d = {'registration_variables': l}

        return jsonify(d), 200

# modification
@app.route('/result', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_result():
    """Predicts the record.csv's last entry result """
    if(request.method=='GET'):
        df = pd.read_csv('record.csv')
        
        #latest entry result
        result = list(df["stroke"])[-1]

        if(result==1.0):
            result="Stroke"
        else:
            result="No Stroke"
        return jsonify({'prediction':result}), 200
    else:
        return jsonify(), 405

# old implementation
# @app.route('/result', methods =['GET'])
# @cross_origin(supports_credentials=True)
# def get_result():
#     if(request.method=='GET'):
#         inp=[]
#         d = request.args
#         for i in d:
#             inp.append(d[i])
#         result = model.predict([inp])[0]
#         print(result)
#         if(result==1.0):
#             result="Stroke"
#         else:
#             result="No Stroke"
#         return jsonify(result=result), 200
#     else:
#         return jsonify(), 405

# @app.route('/var_min_max/<attr_name>', methods =['GET'])
# def get_var_min_max(attr_name):
#     """Returns timeseries of an attribute along with min and max values
#     """
#     """ Todo: /healthstatus is changed to this. Make sure the return type format is as follows (UI is dependent on it) 
#     """
#     if request.method == 'GET':
#         d = {'ts1': 9, 'ts2': 15, 'ts3':21, 'ts4':17, 'ts5': 19, 'min': 12, 'max': 16}
#         d = {'labels': ['ts1', 'ts2', 'ts3', 'ts4', 'ts5'], 'data': [9, 15, 21, 17, 19]}

#         d['min'] = [12 for i in range(len(d['labels']))]
#         d['max'] = [16 for i in range(len(d['labels']))]

#         return jsonify(d), 200
#     else:
#         return jsonify({}), 405
def convert(o):
    if isinstance(o, np.int64):
        return int(o)

@app.route('/var_min_max/<attr_name>', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_status(attr_name):
    if(request.method=='GET'):
        
        #retrive all the records with this id from the csv
        param = attr_name
        print("Param : ", param)
        X = df_transformed.loc[:, df_transformed.columns != param]
        df_record = pd.read_csv("record.csv")
        # print(df_record)

        nsrrid = list(df_record["nsrrid"])[-1]
        

        df_patient = df_record.loc[df_record['nsrrid'] == nsrrid]

        attr_data = list(df_patient[param])
        
        df_patient = df_patient.loc[:, df_patient.columns != 'nsrrid']
        df_patient = df_patient.loc[:, df_patient.columns != param]
        # print(df_patient.head(), end="******\n")
        df_stddev_trans = df_stddev.loc[:, df_stddev.columns != param]
        # print(df_stddev_trans.head(), end="******\n")
        #transform the record by the dividing each value by the std deviation
        # df_patient_trans = df_patient/df_stddev_trans
        df_patient_trans = df_patient.div(df_stddev_trans.iloc[0])
        attr = X.columns.tolist()
        # print(attr)
        # print(len(attr)==len(df_patient_trans.columns.tolist()))
        n_neighbors = 5
        neigh = NearestNeighbors(n_neighbors=n_neighbors)
        d = dict()
        d['data'] = attr_data
        d['labels'] = []
        d['min'] = []
        d['max'] = []
        for index, r in df_patient_trans.iterrows():
            # print(index)
            d['labels'].append(int(index))
            row=[]
            # inner_d={}
            for i in attr:
                row.append(r[i])
            # print(row)
            print(X)
            neigh.fit(X)
            print(row)
            neighbours = neigh.kneighbors([row])
            #gives a tuple(dist,index)
            ind = []
            for i in range(n_neighbors):
                ind.append(neighbours[1][0][i])
            print("indices",ind)
            df_nearest = df.iloc[ind]
            print("Nearest neighbours retrieved:\n", df_nearest)
            # print("User's record \n")
            # print(row)
            # # print()
            # l1 = list(df_nearest.iloc[-1])
            # l2 = list(df_record.iloc[-1])
            # print(len(l1), len(row))
            # diffs = [(l1[i] - row[i])**2 for i in range(0,len(l1))]
            # print("Differences")
            # print(diffs)
            # print("Max differene, index")
            # print(max(diffs), diffs.index(max(diffs)))

            df_nearest.to_csv("Nearest_neighbours.csv")
            # inner_d["min"] = df_nearest[param].min()
            # inner_d["param"] = param
            # inner_d["max"] = df_nearest[param].max()
        
            # d[index] = inner_d

            d['min'].append(df_nearest[param].min().item())
            d['max'].append(df_nearest[param].max().item())
            print(type(d['min'][0]))

        print("result d:",d)
        #for each row in resulting df,for each attr, find 10 rows with least deviation w.r.t. other attributes, find min and max- return attr_val, min,max
        #return as dictionary of dictionaries
        #outer dictionary key will be timestamp
        #d[0] = {"attr1":x,"min":y,"max":z}
        #d[1] = {"attr2":x,"min":y,"max":z}
        
        return jsonify(d)
    else:
        return jsonify(), 405

# #input- id, timestamp, attributes
# @app.route('/store', methods =['POST'])
# @cross_origin(supports_credentials=True)
# def store():
#     if(request.method=='POST'):
#         inp=[]
#         d = list(request.forms.keys())[0]
#         print("d:",d)

#         with open('record.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([d])
        
#         return jsonify(result=result), 200
#     else:
#         return jsonify(), 405

if(__name__=="__main__"):
    app.run(host='0.0.0.0')