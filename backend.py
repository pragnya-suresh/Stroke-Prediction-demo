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
cols = df.columns.tolist()
model = pickle.loads("model.pickle")



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



if(__name__=="__main__"):
    app.run(host='0.0.0.0')
    
