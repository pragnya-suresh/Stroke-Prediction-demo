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

app = Flask(__name__)

CORS(app, support_credentials=True)

df = pd.read_csv("final.csv" ,error_bad_lines=False)
model = joblib.load('model.pkl')


#Run this block only once and then comment
cols = ["id","timestamp"]
cols.append(df.columns.tolist())
with open('record.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(cols)


@app.route('/result', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_result():
    if(request.method=='GET'):
        inp=[]
        d = request.args
        for i in d:
            inp.append(d[i])
        result = model.predict([inp])[0]
        print(result)
        if(result==1.0):
            result="Stroke"
        else:
            result="No Stroke"
        return jsonify(result=result), 200
    else:
        return jsonify(), 405
        
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
    
