from nsepy import get_history
import datetime
from list import *
from utils import *
import mysql.connector
import itertools
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os

# cnx = mysql.connector.connect('host'=os.environ['HOST'],'port'=os.environ['PORT'],'user'=os.environ['USER'],
#                               'password'=os.environ['PASSWORD'],'database'= os.environ['DB'])
cnx = {'host':os.environ['HOST'],'port':os.environ['PORT'],'user':os.environ['USER'],'password':os.environ['PASSWORD'],'database':os.environ['DB']}
# cnx = mysql.connector.connect('host':'127.0.0.1','port':3306,'user':'root','password':'Password12@','database':'stock')

def stock(sec,inlist):
    outlist = []
    ls = inlist
    for stock_a,stock_b in itertools.combinations(ls,2):
        
        zscore = -9999
        print(stock_a,stock_b)
        df_x = fetch_stock_data(stock_a)
        df_y = fetch_stock_data(stock_b)
        
        error_ratio_x,resi_x,beta_x,intercept_x = error_calculation(df_x,df_y)
        error_ratio_y,resi_y,beta_y,intercept_y = error_calculation(df_y,df_x)
        
        if error_ratio_x > error_ratio_y :
            pval = adf_test(resi_y)
            residual = resi_y
            beta = beta_y
            intercept = intercept_y
            stock = stock_a
            stock_a = stock_b
            stock_b = stock
            df_un = df_x
            df_x = df_y
            df_y = df_un
        else:
            pval = adf_test(resi_x)
            residual = resi_x
            beta = beta_x
            intercept = intercept_x
        
        if pval <= 0.05:
            zscore = residual.iloc[-1]/statistics.stdev(residual)
            
        if zscore != -9999:
            risk_ratio = intercept/df_y.iloc[-1]
            out = {"stock_one":stock_a,"stock_two":stock_b,"zscore":zscore,"beta":beta,"intercept":intercept,"risk_ratio":risk_ratio,"p_value":pval}
            insertToDb(sec,out,cnx)
            outlist.append(out)
    
    return {"results":outlist}

