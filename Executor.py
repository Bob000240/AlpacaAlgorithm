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

API_KEY = ""
SECRET_KEY = ""
StockClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

class Executor :
    def __init__(self, stock, qty, strat):
        self.stock = stock
        self.qty = qty
        self.strat = strat
        if self.strat == "TA":
            self.strat = TechnicalAnalysis("NVDA")
    def buy(self):
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=self.qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        order = StockClient.submit_order(order_data)
        return order
    def sell(self):
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=self.qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        order = StockClient.submit_order(order_data)
        return order
    def run(self):
        if self.strat.testindicatorsOrder() == "buy" or self.strat.testindicatorsOrder() == "SBuy":
            return self.buy()
        elif self.strat.testindicatorsOrder() == "sell" or self.strat.testindicatorsOrder() == "SSell":
            return self.sell()
        else:
            print("No action taken based on strategy signals.")
            return None

        

    
