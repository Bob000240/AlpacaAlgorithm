import pandas as pd
import pandas_ta as ta
from .BollingerBand import BBands
from .RSI import RSI
from .MACD import MACD

class IndicatorFactory:
    """
    A factory class to create and compute technical indicators on stock data.
    Attributes:
        dataframe (pd.DataFrame): DataFrame containing stock data.
        indicatorList (list): List of indicators to be computed.
    """
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.indicatorList = []
    def addIndicator(self, indicator):
        if indicator == "BBands(SMA)":
            self.indicatorList.append(BBands("SMA", self.dataframe))
        elif indicator == "BBands(EMA)":
            self.indicatorList.append(BBands("EMA", self.dataframe))
        elif indicator == "RSI":
            self.indicatorList.append(RSI(self.dataframe))
        elif indicator == "MACD":
            self.indicatorList.append(MACD(self.dataframe))
        else:
            raise ValueError(f"Unknown indicator: {indicator}")
    def computeIndicators(self):
        results = []
        for indicator in self.indicatorList:
            results.append(indicator.compute())
        indicatorDataFrame = pd.concat(results, axis=1)
        return indicatorDataFrame
    def TAStrats(self):
        signals = []
        for indicator in self.indicatorList:
            signals.append(indicator.TAStrats())
        signalDataFrame = pd.concat(signals, axis=1)
        return signalDataFrame
