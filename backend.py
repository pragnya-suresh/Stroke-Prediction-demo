import os
from flask import Flask, flash, request, redirect, url_for, jsonify,json, render_template
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
import pickle
import pandas as pd

app = Flask(__name__)

CORS(app, support_credentials=True)

#df = pd.read_csv("final.csv" ,error_bad_lines=False)
# model = pickle.loads("model.pickle")
#
##Run this block only once and then comment
#cols = ["id","timestamp"]
#cols.append(df.cols.tolist())
#with open('record.csv', 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow(cols)

@app.route('/variables/<category>', methods=['GET'])
def get_variables(category):
    
    if request.method=='GET':
        df = pd.read_csv('code/shhs-data-dictionary-0.15.0-variables.csv')
        cat_df = df[df['folder']==category]
        var_desc = dict(zip(list(cat_df['id']),list(cat_df['display_name'])))

        return jsonify(var_desc), 200
    else:
        return jsonify(), 405

@app.route('/register_patient', methods=['GET', 'POST'])
def get_registration_variables():
    """ Needs to return {vars: list1, descriptions: list2}
    """
    if request.method == 'GET':

        l = ['nsrrid', 'timestamp', 'ventrate', 'qrs', 'avcanba', 'avcanoa', 'avcarbp2', 'avcaroa2', 'avcanoa3', 'avcaroa4', 'avcanba5', 'oaroa5', 'estrgn1', 'lipid1', 'minfa10', 'cgrtts10', 'climb125', 'wksblk25', 'wk1blk25', 'bathe25', 'rawpf_s1', 'rawgh_s1', 'rawvt_s1', 'mh_s1', 'age_s1']
        descriptions = ['NSRR Subject ID', 'Appointment number', 'Ventricular rate', 'QRS Axis', 'Average Central Apnea length w/ arousals (Non-rapid eye movement sleep (NREM), Supine, all oxygen desaturations)', 'Average Central Apnea length w/ arousals (Non-rapid eye movement sleep (NREM), Non-supine, all oxygen desaturations)', 'Average Central Apnea length (Rapid eye movement sleep (REM), Supine, >=2% oxygen desaturation)', 'Average Central Apnea length with >=2% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Average Central Apnea length with >=3% oxygen desaturation or arousal (Non-rapid eye movement sleep (NREM), Non-supine)', 'Average Central Apnea length with >=4% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Average Central Apnea length with >=5% oxygen desaturation or arousal (Non-rapid eye movement sleep (NREM), Supine)', 'Number of Obstructive Apnea with >=5% oxygen desaturation or arousal (Rapid eye movement sleep (REM), Non-supine)', 'Estrogens, Excluding Vaginal Creams ', 'Any Lipid-Lowering Medication ', 'Morning Survey : minutes to fall asleep', 'Morning Survey : cigarettes before bed', 'Quality of Life (QOL) : Health limits climbing one flight of stairs', 'Quality of Life (QOL) : Health limits walking several blocks', 'Quality of Life (QOL) : Health limits walking one block', 'Quality of Life (QOL) : Health limits bathing and dressing', 'Short Form 36 Health Survey (SF-36) Calculated : Physical Functioning Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : General Health Perceptions Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : Vitality Raw Score', 'Short Form 36 Health Survey (SF-36) Calculated : Mental Health Index Standardized Score', 'Age at Sleep Heart Health Study Visit One (SHHS1)']
        
        d = {'registration_variables': l, 'descriptions':descriptions}

        return jsonify(d), 200
    
    elif request.method == 'POST':
        # user_data = request.get_json(force=True)
        # print(user_data)
        
        user_data = dict()
        values = []
        for i in l:
            user_data[i] = request.form[i]
            values.append(request.form[i])

        df = pd.read_csv('record.csv')
        row_index = df.shape[0]

        df.loc[row_index] = values

        df.to_csv('record.csv', index=False)

        return jsonify({}), 201
    else:
        return jsonify(), 405


@app.route('/patient_ids', methods = ['GET'])
def get_patient_ids():

    if request.method == 'GET':
        df = pd.read_csv('record.csv')
        ids = list(df['nsrrid'])

        d = {'patient_ids' : ids}
        return jsonify(d), 200
    else:
        return jsonify({}),405


@app.route('/predict_stroke', methods = ['GET'])
def predict_stroke():
    """Predicts the record.csv's last entry result """
    """Todo : 1) api: /result should be changed to this
              2) is prediction is 1, return "yes" else return "no"
    """
    if request.method == 'GET':
        df = pd.read_csv('record.csv')
        attributes = list(df.loc[df.shape[0]-1])
        attributes = np.array(attributes)
        # result = model.predict(attributes)
        result = "yes"
        print(result)
        return jsonify({'prediction': result}), 200
    else:
        return jsonify({}),405

# pragnya this should be changed.... look at the above api
@app.route('/result', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_result():
    if(request.method=='GET'):
        inp=[]
        d = request.args
        for i in l:
            inp.append(d[i])
        result = model.predict(inp)
        print(result)
        return jsonify(result=result), 200
    else:
        return jsonify(), 405


@app.route('/var_min_max/<attr_name>', methods =['GET'])
def get_var_min_max(attr_name):
    """Returns timeseries of an attribute along with min and max values
    """
    """ Todo: /healthstatus is changed to this. Make sure the return type format is as follows (UI is dependent on it) 
    """
    if request.method == 'GET':
        d = {'ts1': 9, 'ts2': 15, 'ts3':21, 'ts4':17, 'ts5': 19, 'min': 12, 'max': 16}
        d = {'labels': ['ts1', 'ts2', 'ts3', 'ts4', 'ts5'], 'data': [9, 15, 21, 17, 19]}

        d['min'] = [12 for i in range(len(d['labels']))]
        d['max'] = [16 for i in range(len(d['labels']))]

        return jsonify(d), 200
    else:
        return jsonify({}), 405

# change this to get_var_min_max
@app.route('/healthstatus', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_status():
    if(request.method=='GET'):
        id = request.args.get("id")
        param = request.args.get("param")
        print("id:",id)
        ts =df_patient[df_patient['id']==id]['timestamp'].values
        #retrive all the records with this id from the csv
        X = df.loc[:, df.columns != 'stroke']
        X = X.loc[:, df.columns != param]
        df_record = pd.read_csv("record.csv")
        df_patient = df.loc[df['id'] == id]
        df_patient = df_patient.loc[:, df_patient.columns != 'id']
        df_patient = df_patient.loc[:, df_patient.columns != 'timestamp']
        df_patient = df_patient.loc[:, df_patient.columns != param]
        prin(len(x),len(df_patient))
        attr = df.columns.tolist()
        neigh = NearestNeighbors(n_neighbors=10)
        d = {}
        for index, r in df_patient.iterrows():
            row=[]
            inner_d={}
            for i in attr:
              row.append(r[i])
            print(row)
            neigh.fit(X)
            neighbours = neigh.kneighbors([row])
            #gives a tuple(dist,index)
            ind = []
            for i in range(10):
                ind.append(neighbours[1][0][i])
            df_nearest = df.iloc[ind]
            inner_d["min"] = df_nearest[param].min()
            inner_d["param"] = param
            inner_d["max"] = df_nearest[param].max()
            d[ts[index]] = inner_d
            
        #for each row in resulting df,for each attr, find 10 rows with least deviation w.r.t. other attributes, find min and max- return attr_val, min,max
        #return as dictionary of dictionaries
        #outer dictionary key will be timestamp
        #d["ts1"] = {"attr1":x,"min":y,"max":z}
        #d["ts2"] = {"attr2":x,"min":y,"max":z}
        
        return jsonify(result=d), 200
    else:
        return jsonify(), 405

#input- id, timestamp, attributes
@app.route('/store', methods =['POST'])
@cross_origin(supports_credentials=True)
def store():
    if(request.method=='POST'):
        inp=[]
        d = list(request.forms.keys())[0]
        print("d:",d)

        with open('record.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([d])
        
        return jsonify(result=result), 200
    else:
        return jsonify(), 405

if(__name__=="__main__"):
    app.run(host='0.0.0.0')
    
