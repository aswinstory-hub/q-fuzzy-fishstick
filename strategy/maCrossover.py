import numpy as np 
import pandas as pd 

class MaCrossover:
    def __init__(self, prices, fast_length, slow_length):
        self.close = prices
        self.fast = int(fast_length)
        self.slow = int(slow_length)

    def get_historical_signals(self):
        fast_ma = self.close.rolling(self.fast).mean()
        slow_ma = self.close.rolling(self.slow).mean()
        
        up_trend = (fast_ma > slow_ma).astype(int)
        prev_candle = (self.close.shift(1) < fast_ma.shift(1)).astype(int)
        curt_candle = (self.close > fast_ma).astype(int)

        cond = (up_trend == prev_candle) & (prev_candle == curt_candle)
        all_nan = up_trend.isna() & prev_candle.isna() & curt_candle.isna()


        if len(up_trend) == len(prev_candle) & len(prev_candle) == len(curt_candle):
            signals =(cond & ~all_nan).astype(int)
        else:
            print("All conditions dont have the same length, dumbass")

        return signals

        


from modules.data import Data 

data = Data() 
stock = "RELIANCE.NS"

df = data.get_single_stock_data(ticker=stock)

strat = MaCrossover(df['close'], 20, 50)

signals = strat.get_historical_signals()

print(signals)
