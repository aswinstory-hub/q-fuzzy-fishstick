import numpy as np 
import pandas as pd 

class MaCrossover:
    def __init__(self, prices, fast_length, slow_length):
        self.df = prices
        self.fast = int(fast_length)
        self.slow = int(slow_length)

    def signal(self):
        fast_ma = self.df.rolling(self.fast).mean()

        print(fast_ma)

        


import duckdb

con = duckdb.connect("prices.db")

df = con.execute("SELECT * FROM prices WHERE symbol = 'RELIANCE.NS'").df()

con.close()

strat = MaCrossover(df['close'], 20, 50)

strat.signal()
