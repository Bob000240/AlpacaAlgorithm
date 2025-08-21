import time
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest 
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pandas_ta as ta

import alpaca.data.requests as DataRequest
from Retriever import Retriever
from TechnicalAnalysis import TechnicalAnalysis

API_KEY = "PKWTJIBVMNMS9I071AP3"
SECRET_KEY = "yx9PvdxcScs7Kyo7ef5dv7B614QqiP1nmhaTp2Wm"
StockClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

class Executor :
    def __init__(self, stock, qty, strat):
        self.stock = stock
        self.qty = qty
        self.strat = strat
        if self.strat == "TA":
            self.strat = TechnicalAnalysis(self.stock)
    def buy(self):
        if self.qty is None or self.qty <= 0:
            print(f"Skip BUY {self.stock}: computed qty={self.qty}")
            return None
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=int(self.qty),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        return StockClient.submit_order(order_data)

    def sell(self):
        if self.qty is None or self.qty <= 0:
            print(f"Skip SELL {self.stock}: computed qty={self.qty}")
            return None
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=int(self.qty),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        return StockClient.submit_order(order_data)
    def execute(self):
        if self.strat.testindicatorsOrder() == "buy" or self.strat.testindicatorsOrder() == "SBuy":
            self.buy()
            return "buy"
        elif self.strat.testindicatorsOrder() == "sell" or self.strat.testindicatorsOrder() == "SSell":
            self.sell()
            return "sell"
        else:
            return None

class Stock:
    def __init__(self, name, allocation):
        self.name = name
        self.df = Retriever(name).getLatestData()
        self.share = allocation // self.df.iloc[-1]['close']

class Main:
    def __init__(self):
        self.beginningCapital = float(StockClient.get_account().cash) * 0.1
        self.stocks = []
        self.stocksCount = len(self.stocks)
        self.indAllocation = self.beginningCapital // self.stocksCount if self.stocksCount > 0 else 0
    def updateCapital(self):
        self.stocksCount = len(self.stocks)
        self.indAllocation = self.beginningCapital // self.stocksCount if self.stocksCount > 0 else 0
    def addStock(self, name):
        self.stocks.append(Stock(name, self.indAllocation))
        self.updateCapital()
    def removeStock(self, name):
        for s in self.stocks:
            if s.name == name:
                self.stocks.remove(s)
                break
    def run(self):
        for stock in self.stocks:
            executor = Executor(stock.name, stock.share, "TA")
            order = executor.execute()
            if order:
                print(f"Executed order for {stock.name}: {order}")
            else:
                print(f"No action taken for {stock.name}.")



if __name__ == "__main__":
    main = Main()
    main.addStock("NVDA")
    main.addStock("AAPL")
    main.addStock("TSLA")
    main.addStock("AMZN")
    main.addStock("GOOGL")
    main.addStock("META")
    main.addStock("NVO")
    main.addStock("AMD")
    main.addStock("MSFT")
    main.addStock("LLY")
    while True:
        main.run()
        print("Waiting for next execution cycle...")
        time.sleep(60)