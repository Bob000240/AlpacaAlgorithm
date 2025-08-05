import pandas as pd
import pandas_ta as ta

class RSI:
    """
    A class to compute the Relative Strength Index (RSI) on stock data.
    Attributes:
        dataframe (pd.DataFrame): DataFrame containing stock data.
        close_col (str): Column name for the closing prices.
    """
    def __init__(self, dataframe, close_col='close'):
        self.dataframe = dataframe
        self.close_col = close_col

    def compute(self, length=14):
        s = ta.rsi(self.dataframe[self.close_col], length=length)
        result = pd.DataFrame()
        result['RSI'] = s
        return result
    def signalStrat(self):
        df = self.compute()
        rsi = df['RSI']

        signal = pd.Series("hold", index=self.dataframe.index, name ='RSI_result')
        signal[rsi > 70] = 'sell'
        signal[rsi < 30] = 'buy'
        #signal.fillna('hold', inplace=True)
        return signal