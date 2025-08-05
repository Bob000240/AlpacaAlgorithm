import pandas as pd
import pandas_ta as ta

class KDJ:
    """
    A class to compute the KDJ indicator on stock data. 
    Attributes:
        dataframe (pd.DataFrame): DataFrame containing stock data.
        close_col (str): Column name for the closing prices.
    """
    def __init__(self, dataframe, close_col='close'):
        self.dataframe = dataframe
        self.close_col = close_col
    def compute(self, length=14, k=3, d=3):
        df = ta.kdj(self.dataframe[self.close_col], length=length, k=k, d=d)
        result = pd.DataFrame()
        result['KDJ_K'] = df[f'K_{length}_{k}']
        result['KDJ_D'] = df[f'D_{length}_{d}']
        result['KDJ_J'] = df[f'J_{length}_{k}_{d}']
        return result
    #def signalStrat:
    