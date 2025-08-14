from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
import alpaca.data.requests as DataRequest

from datetime import datetime, timedelta
import pandas as pd
from Indicators.IndicatorFactory import IndicatorFactory


API_KEY = "PKWTJIBVMNMS9I071AP3"
SECRET_KEY = "yx9PvdxcScs7Kyo7ef5dv7B614QqiP1nmhaTp2Wm"
DataClient = StockHistoricalDataClient(API_KEY, SECRET_KEY)

class Retriever:
    def __init__(self, stock):
        self.stock = stock
        self.stockData = pd.DataFrame()
        hData = DataRequest.StockBarsRequest(
            symbol_or_symbols = self.stock,
            start = datetime.now() - timedelta(days=1),
            end = datetime.now(),
            #limit = 100,
            # currency: SupportedCurrencies | None = None,
            sort = "desc",
            timeframe = TimeFrame.Minute,
            # adjustment: Adjustment | None = None,
            # feed: DataFeed | None = None,
            # asof: str | None = None
        )
        raw = DataClient.get_stock_bars(hData)  
        dataList = []
        for item in raw[stock]:
            dataList.append({
                "open": item.open,
                "high": item.high,
                "low": item.low,
                "close": item.close,
                "volume": item.volume,
                "datetime": item.timestamp
            })
        self.stockData = pd.DataFrame(dataList)
        self.stockData = self.stockData.sort_values("datetime")  # oldest to newest

        self.indicatorData = pd.DataFrame()
        self.signalData = pd.DataFrame()
        self.combinedData = pd.DataFrame()

        self.indicatorFactory = IndicatorFactory(self.stockData)
    def addIndicator(self, indicator):
        self.indicatorFactory.addIndicator(indicator)
    def getIndicatorData(self):
        self.indicatorData = self.indicatorFactory.computeIndicators()
        self.indicatorData = self.indicatorData
        return self.indicatorData
    def getTAData(self):
        self.signalData = self.indicatorFactory.TAStrats()
        return self.signalData
    def getCombineData(self):
        self.combinedData = pd.concat([self.stockData, self.indicatorData, self.signalData], axis=1)
        self.combinedData = self.combinedData.dropna()
        return self.combinedData
    def getStockData(self):
        return self.stockData
    def getLatestData(self):
        return self.stockData.tail(1)
    def toCSV(self, dataframe):
        return dataframe.to_csv(index=False)

"""
spy = Retriever("NVO")
spy.addIndicator("BBands(SMA)")
spy.addIndicator("BBands(EMA)")
spy.addIndicator("RSI")
spy.addIndicator("MACD")
print(spy.getSignalData())
print(spy.getIndicatorData())
print(spy.getStockData())
print(spy.getCombineData())


with open("data.csv", "w") as f:

    f.write(spy.toCSV(spy.getCombineData()))
"""