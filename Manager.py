import time
from alpaca.trading.client import TradingClient
from Retriever import Retriever
from Executor import Executor

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPACA_PUBLIC_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
StockClient = TradingClient(API_KEY, SECRET_KEY, paper=True)

class Stock:
    def __init__(self, name, allocation):
        self.name = name
        self.df = Retriever(name).getLatestData()
        self.buyShare = int(allocation // self.df['close'].iloc[-1]) if allocation > 0 else 0
        try:
            position = StockClient.get_open_position(name)
            self.availableShares = int(position.qty)
        except Exception:
            self.availableShares = 0
        self.sellShare = int(self.availableShares) // 2 if self.availableShares % 2 == 0 else int(self.availableShares) // 2 + 1

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
            executor = Executor(stock.name, stock.buyShare, stock.sellShare, "TA")
            order = executor.execute()
            if order:
                print(f"Executed order for {stock.name}: {order}")
            else:
                print(f"No action taken for {stock.name}.")
            stock = Stock(stock.name, self.indAllocation)



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