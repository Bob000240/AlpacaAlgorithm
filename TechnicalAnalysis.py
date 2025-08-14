from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_ta as ta
from Retriever import Retriever

class TechnicalAnalysis:
    def __init__(self, stock):
        data = Retriever(stock)
        data.addIndicator("BBands(SMA)")
        data.addIndicator("BBands(EMA)")
        data.addIndicator("RSI")
        data.addIndicator("MACD")
        self.df = data.getTAData()
        self.sigTOVal = {
            "buy": 1,
            "sell": -1,
            "hold": 0
        }
    def testIndicatorsData(self):
        totalIndicators = self.df.shape[1]

        signalInt = pd.Series(0, index=self.df.index, name="signalInt")
        signalInt = self.df.apply(
            lambda row : sum(self.sigTOVal[element] for element in row),
            axis=1
        )
        signal = pd.Series("hold", index=self.df.index, name="signal")
        score = signalInt / totalIndicators
        signal[score == 1] = "SBuy"
        signal[(score > 0.6) & (score < 1)] = "buy"
        signal[score == -1] = "SSell"
        signal[(score < -0.6) & (score > -1)] = "sell"
        return pd.concat([signalInt, signal], axis=1)
    def testindicatorsOrder(self):
        latestRow = self.df.iloc[-1]
        totalIndicators = self.df.shape[1]
        totalIndicatorsVal = sum(self.sigTOVal[element] for element in latestRow)
        if totalIndicatorsVal / totalIndicators == 1:
            return "SBuy"
        elif (totalIndicatorsVal / totalIndicators > 0.6) and (totalIndicatorsVal / totalIndicators < 1):
            return "buy"    
        elif totalIndicatorsVal / totalIndicators == -1:
            return "SSell"  
        elif (totalIndicatorsVal / totalIndicators < -0.6) and (totalIndicatorsVal / totalIndicators > -1):
            return "sell"
        else:
            return "hold"
    def toCSV(self, dataframe):
        return dataframe.to_csv(index=False)