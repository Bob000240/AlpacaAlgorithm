from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest 

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

        

    
