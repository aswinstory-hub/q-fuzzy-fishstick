# Module for importing and formating data
import duckdb
from pathlib import Path


class Data:
    def __init__(self):
        self.db_path = Path(__file__).resolve().parent.parent / "prices.db"
    
    def get_single_stock_data(self, ticker :str, full_data=True, start="0", end="0"):
        
        conn = duckdb.connect(str(self.db_path))
        
        if full_data == True:
            df = conn.execute(f"SELECT * FROM prices WHERE symbol = {ticker}")
        else:
            df = conn.execute(f"SELECT * FROM prices WHERE symbol = {ticker} BETWEEN {start} AND {end}")

        conn.close()
        
        return df 

    def ask_symbol() -> str:
        """Interactive prompt — shows available tickers and validates the input."""
        tickers = load_tickers()
        print("\nAvailable symbols:")
        print(", ".join(tickers))

        while True:
            symbol = input("\nSelect any one symbol from the above: ").strip().upper()
            if symbol in tickers:
                print(f"Nice choice! {symbol} is a great stock to select.")
                return symbol
            else:
                print(f"  '{symbol}' is not in the list. Please try again.")
