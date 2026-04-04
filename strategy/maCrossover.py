import numpy as np 
import pandas as pd 

class MaCrossover:
    def __init__(self, df, fast_length, slow_length):
        self.df = df
        self.fast = int(fast_length)
        self.slow = int(slow_length)

    def signal(self):
        fast_ma = self.df[-20:].mean()

        print(fast_ma)

        


import duckdb

con = duckdb.connect("prices.db")

print(con.execute("SHOW TABLES").fetchall())
df = con.execute("SELECT * FROM prices WHERE symbol = 'RELIANCE.NS'").df()

con.close()

strat = MaCrossover(df, 20, 50)

strat.signal()
