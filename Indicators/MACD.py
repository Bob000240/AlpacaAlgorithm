import pandas as pd
import pandas_ta as ta

class MACD:
    """
    A class to compute the Moving Average Convergence Divergence (MACD) on stock data.
    Attributes:
        dataframe (pd.DataFrame): DataFrame containing stock data.
        close_col (str): Column name for the closing prices.
    """
    def __init__(self, dataframe, close_col='close'):
        self.dataframe = dataframe
        self.close_col = close_col

    def compute(self, fast=12, slow=26, signal=9):
        df = ta.macd(self.dataframe[self.close_col], fast=fast, slow=slow, signal=signal)
        result = pd.DataFrame()
        result['MACD'] = df[f"MACD_{fast}_{slow}_{signal}"]
        result['MACD_hist'] = df[f"MACDh_{fast}_{slow}_{signal}"]
        result['MACD_sig'] = df[f"MACDs_{fast}_{slow}_{signal}"]
        return result
    def TAStrats(self):
        df = self.compute()
        macd = df['MACD']
        macdSignal = df['MACD_sig']

        signal = pd.Series("hold", self.dataframe.index, name='MACD_result')
        signal[(macd > macdSignal) & (macd.shift(1) <= macdSignal.shift(1))] = 'buy'
        signal[(macd < macdSignal) & (macd.shift(1) >= macdSignal.shift(1))] = 'sell'
        #signal.fillna('hold', inplace=True)
        return signal
