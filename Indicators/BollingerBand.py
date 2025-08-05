import pandas as pd
import pandas_ta as ta

class BBands:
    """
    A class to compute Bollinger Bands on stock data.
    Attributes:
        dataframe (pd.DataFrame): DataFrame containing stock data.
        close_col (str): Column name for the closing prices.
    """
    def __init__(self, ma, dataframe, close_col='close'):
        self.dataframe = dataframe
        self.close_col = close_col
        self.ma = ma

    def compute(self, length=20, std=2, mamode=None):
        if mamode == None:
            mamode = self.ma
        df = ta.bbands(self.dataframe[self.close_col], length=length, std=std, mamode=mamode)
        result = pd.DataFrame()
        result[f'BBANDS_lower_{mamode.upper()}'] = df[f'BBL_{length}_{std:.1f}']
        result[f'BBANDS_mid_{mamode.upper()}'] = df[f'BBM_{length}_{std:.1f}']
        result[f'BBANDS_upper_{mamode.upper()}'] = df[f'BBU_{length}_{std:.1f}']
        return result
    def signalStrat(self):
        df = self.compute()
        price = self.dataframe[self.close_col]

        upper = df[f'BBANDS_upper_{self.ma.upper()}']
        lower = df[f'BBANDS_lower_{self.ma.upper()}']

        signal = pd.Series("hold", index=self.dataframe.index, name =f'BBands_{self.ma}_result')
        signal[price > upper] = 'sell'
        signal[price < lower] = 'buy'
        #signal.fillna('hold', inplace=True)
        return signal