import pandas as pd
import numpy as np
from flask import Flask,request
import json
import requests
from datanse import *
from list import *
from utils import *
from flask_cors import CORS, cross_origin
import os

# cnx = {'host':'127.0.0.1','port':'3306','user':'root','password':'Password12@','database':'stock'}

cnx = {'host':os.environ['HOST'],'port':os.environ['PORT'],'user':os.environ['USER'],'password':os.environ['PASSWORD'],'database':os.environ['DB']}

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/',methods=["GET"])
def index():
    
    deletePrevData(cnx)
    
    for key,value in FinalList.items():
        print(key)
        print(value)
        output = stock(key,value)
        
    return json.dumps(output)

@app.route('/get_data',methods=["GET"])
@cross_origin()
def getdata():
    
    query = "select * from stockdata"
    df = fetch_and_rename(query,cnx)
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['date'] = df['date'].astype(str)
    
    out = df.to_json(orient='records')
    return out


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
