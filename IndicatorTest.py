from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_ta as ta
from Retriever import Retriever

class IndicatorTest:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        

spy = Retriever("NVDA")
spy.addIndicator("BBands")
spy.addIndicator("RSI")
spy.addIndicator("MACD")
spy.addIndicator("SMA")
print(spy.getIndicatorData())
print(spy.getCombineData())
print(spy.getStockData())




lr = LinearRegression(spy.getCombineData())
print("X values (indicators):")
print(lr.getX())
print("Y values (closing prices):")
print(lr.getY())
print("Coefficients of the linear regression model:")
print(lr.get_coefficients())
print("Linear Regression Model Summary:")
