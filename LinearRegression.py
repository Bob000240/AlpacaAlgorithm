from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_ta as ta
from Retriever import Retriever

class LinearRegression:
    def __init__(self, stock):
        data = Retriever(stock)
        self.dataframe = data
        self.X = data.drop(columns=['open', 'high', 'low', 'close', 'volume', 'datetime']).to_numpy()
        self.Y = data['close'].to_numpy()
        self.X = np.column_stack((np.ones((self.X.shape[0])),self.X))  # add intercept
        self.beta_hat = np.linalg.pinv(self.X.T @ self.X) @ self.X.T @ self.Y
    def mostOptimalIndicators(self):
        pass
    def getX(self):
        print(type(self.X))
        print(self.X.shape)
        return self.X
    def getY(self):
        print(type(self.Y))
        print(self.Y.shape)
        return self.Y
    def get_coefficients(self):
        return self.beta_hat

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
