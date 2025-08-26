from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest 

from TechnicalAnalysis import TechnicalAnalysis

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPACA_PUBLIC_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
StockClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

class Executor :
    def __init__(self, stock, buyQty, sellQty, strat):
        self.stock = stock
        self.buyQty = buyQty
        self.sellQty = sellQty
        self.strat = strat
        if self.strat == "TA":
            self.strat = TechnicalAnalysis(self.stock)
        else:
            raise ValueError(f"Strategy {self.strat} not recognized.")
    def buy(self):
        if self.buyQty is None or self.buyQty <= 0:
            print(f"Skip BUY {self.stock}: computed buyQty={self.buyQty}")
            return None
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=int(self.buyQty),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY
        )
        return StockClient.submit_order(order_data)

    def sell(self):
        if self.sellQty is None or self.sellQty <= 0:
            print(f"Skip SELL {self.stock}: computed sellQty={self.sellQty}")
            return None
        order_data = MarketOrderRequest(
            symbol=self.stock,
            qty=int(self.sellQty),
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

        

    
