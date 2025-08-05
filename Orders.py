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

API_KEY = ""
SECRET_KEY = ""
StackClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

class Orders:
    def __init__(self, stock, orderType, qty):
        self.stock = stock
        self.orderType = orderType
        self.qty = qty
    def buy(self):
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=self.qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        order = StackClient.submit_order(order_data)
        return order
    def sell(self):
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=self.qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        order = StackClient.submit_order(order_data)
        return order
        

    
