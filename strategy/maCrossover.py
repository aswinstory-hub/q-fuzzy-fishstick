import numpy as np 
import pandas as pd 

class MaCrossover:
    def __init__(self, df):
        self.df = df

    def run(self):
        print(self.df.head())


# import duckdb
#
# con = duckdb.connect("prices.db")
#
# print(con.execute("SHOW TABLES").fetchall())
# df = con.execute("SELECT * FROM prices WHERE symbol = 'RELIANCE.NS'").df()
#
# con.close()
#
# strat = MaCrossover(df)
#
# strat.run()
