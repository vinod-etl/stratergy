import pandas as pd
import numpy as np
import mysql.connector
from nsepy import get_history
from statsmodels.tsa.stattools import adfuller
from datetime import date
import datetime
import statsmodels.api as sm
import statistics


def fetch_and_rename(query,cred):
    
    cnx = mysql.connector.connect(**cred)
    df = pd.read_sql(query,con=cnx)
    cnx.close()
    
    return df

def adf_test(timeseries):
    #Perform Dickey-Fuller test:
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
       dfoutput['Critical Value (%s)'%key] = value
    # print (dfoutput)
    return dfoutput["p-value"]

def deletePrevData(cred):
    
    cnx = mysql.connector.connect(**cred)
    cursor = cnx.cursor()
    Delete_all_rows = """ truncate table stockdata """
    cursor.execute(Delete_all_rows)
    cnx.commit()
    
    return True

def error_calculation(x,y):
	
	z = sm.add_constant(x)
	
	results = sm.OLS(y,z).fit()
	
	intercept = results.params.const
	beta = results.params.Close
	error_ratio = results.bse.const/statistics.stdev(results.resid)
	
	residuals = results.resid
	
	return error_ratio,residuals,beta,intercept

def exportToCsv(out):
    
    data = {"results":out}
    with open('outdata.txt', 'w') as outfile:
        json.dump(data, outfile)


def fetch_stock_data(x):
	
	today = datetime.datetime.now().date()

	olddate = (datetime.datetime.now() - datetime.timedelta(days=1*365)).date()

	df = get_history(symbol=x,start= olddate,
					   end= today)
	df = df['Close']
	
	df.reset_index(drop=True)
	
	return df

def insertToDb(sec,indata,cred):
    
    cnx = mysql.connector.connect(**cred)
    today = datetime.datetime.now()
    mySql_insert_query = """INSERT INTO stockdata (date, zscore, stock_a, stock_b,beta,intercept,risk_ratio,pvalue,sector) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s) """
    
    recordTuple = (today, indata['zscore'], indata['stock_one'], indata['stock_two'],indata['beta'],indata['intercept'],indata['risk_ratio'],indata['p_value'],sec)
    cursor = cnx.cursor()
    cursor.execute(mySql_insert_query, recordTuple)
    cnx.commit()
    
    return True
    