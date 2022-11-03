from scipy.stats import norm
from math import *
from datetime import *
import pandas as pd 
import numpy as np
import pandas_datareader as web

#S = price of underlying asset at time t
#K = strike price
#T = expiration time
#r = risk-free interest rate (force of interest)
#sigma = std deviation of the stock's returns 

def d1(S, K, T, r, sigma):
    '''d1 parameter of black scholes'''
    return (log(S/K)+(r+sigma**2/2.)*T)/(sigma*sqrt(T))

def d2(S,K,T,r,sigma):
    '''d2 parameter of black scholes'''
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)

def call_op(S,K,T,r,sigma):
    return S*norm.cdf(d1(S,K,T,r,sigma))-K*exp(-r*T)*norm.cdf(d2(S,K,T,r,sigma))
  
def put_op(S,K,T,r,sigma):
    return K*exp(-r*T)-S*call_op(S,K,T,r,sigma)

def getPrice(stock, exp, strike):
    date = datetime.now()
    oneYrBack = date.replace(year=date.year-1)

    data = web.DataReader(stock, 'yahoo', oneYrBack, date)
    data = data.sort_values(by="Date")
    data = data.dropna()
    data = data.assign(close_day_before=data.Close.shift(1))
    data['returns'] = ((data.Close - data.close_day_before)/data.close_day_before)

    sigma = np.sqrt(252) * data['returns'].std()

    #used for the risk free interest rate 
    uty = (web.DataReader("^TNX", 'yahoo', date.replace(day=date.day-1), date)['Close'].iloc[-1])/100
    lcp = data['Close'].iloc[-1]
    t = (datetime.strptime(exp, "%m-%d-%Y") - datetime.utcnow()).days / 365

    return ('The Option Price is: ', call_op(lcp, strike, t, uty, sigma))

print(getPrice('SPY', '11-18-2022', 360))