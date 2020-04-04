import os
from flask import Flask, flash, request, redirect, url_for, jsonify,json
import requests
from flask_cors import CORS, cross_origin
import numpy as np
from flask import Response
from flask import jsonify
import csv
import random
import time
import os
import pandas as pd
import pickle

app = Flask(__name__)

CORS(app, support_credentials=True)

df = pd.read_csv("final.csv" ,error_bad_lines=False)
model = pickle.loads("model.pickle")

#Run this block only one and then comment
cols = ["id","timestamp"]
cols.append(df.cols.tolist())
with open('record.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(cols)


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
        
@app.route('/healthstatus', methods =['GET'])
@cross_origin(supports_credentials=True)
def get_status():
    if(request.method=='GET'):
        id = request.args.get("id")
        print("id:",id)
        #retrive all the records with this id from the csv
        df_record = pd.read_csv("record.csv")
        df_patient = df.loc[df['id'] == id]
        #for each row in resulting df,for each attr, find 10 rows with least deviation w.r.t. other attributes, find min and max- return attr_val, min,max
        #return as dictionary of dictionaries
        #outer dictionary key will be timestamp
        #d["ts1"] = {"attr1":x,"min":y,"max":z}
        #d["ts2"] = {"attr2":x,"min":y,"max":z}
        return jsonify(result=result), 200
    else:
        return jsonify(), 405

#input- id, timestamp, attributes
@app.route('/store', methods =['GET'])
@cross_origin(supports_credentials=True)
def store():
    if(request.method=='GET'):
        inp=[]
        d = request.args
        l = list(d.values)
        with open('record.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([l])
        
        return jsonify(result=result), 200
    else:
        return jsonify(), 405

if(__name__=="__main__"):
    app.run(host='0.0.0.0')
    
