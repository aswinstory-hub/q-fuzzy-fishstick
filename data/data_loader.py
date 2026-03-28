import duckdb
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
from typing import List

from utils import DB_PATH, load_tickers_ns

TABLE_NAME = "prices"
DEFAULT_START = "2015-01-01"


# -----------------------------
# 1. Connect to DuckDB
# -----------------------------
con = duckdb.connect(DB_PATH)

try:
    # -----------------------------
    # 2. Get the latest date in the database
    # -----------------------------
    latest_date = con.execute(f"""
        SELECT MAX(date) FROM {TABLE_NAME}
    """).fetchone()[0]

    if latest_date is None:
        print(f"No data found in DB. Starting fresh from {DEFAULT_START}.")
        start_date = DEFAULT_START
    else:
        start_date = str(latest_date + timedelta(days=1))
        print(f"Latest date in DB: {latest_date}")

    print(f"Downloading from:  {start_date}")

    # Guard: don't download if already up to date
    if start_date > str(date.today()):
        print("Database is already up to date.")
        con.close()
        raise SystemExit(0)

    # -----------------------------
    # 3. Read tickers from file
    # -----------------------------
    symbols = load_tickers_ns()
    print(f"Tickers to update: {len(symbols)}")


    # -----------------------------
    # 4. Download new prices from yfinance
    # -----------------------------
    def download_prices(symbols: List[str], start: str) -> pd.DataFrame:
        try:
            df = yf.download(
                tickers=symbols,
                start=start,
                group_by="ticker",
                threads=True,
                auto_adjust=True
            )
        except Exception as e:
            print(f"Error downloading data from yfinance: {e}")
            return pd.DataFrame()

        if df.empty:
            print("No new data available.")
            return pd.DataFrame()

        frames = []

        if len(symbols) == 1:
            sub = df.copy()
            sub.reset_index(inplace=True)
            sub.columns = [c.lower().replace(" ", "_") for c in sub.columns]
            sub["symbol"] = symbols[0]
            frames.append(sub)
        else:
            for symbol in symbols:
                try:
                    sub = df[symbol].copy()
                    sub.reset_index(inplace=True)
                    sub.columns = [c.lower().replace(" ", "_") for c in sub.columns]
                    sub["symbol"] = symbol
                    frames.append(sub)
                except KeyError:
                    print(f"  Warning: No data for {symbol}, skipping.")

        if not frames:
            return pd.DataFrame()

        return pd.concat(frames, ignore_index=True)


    prices_df = download_prices(symbols, start=start_date)

    if not prices_df.empty:
        # -----------------------------
        # 5. Clean and select columns
        # -----------------------------
        prices_df = prices_df[
            ["symbol", "date", "open", "high", "low", "close", "volume"]
        ]

        # -----------------------------
        # 6. Deduplicated insert
        # -----------------------------
        con.execute(f"""
            INSERT INTO {TABLE_NAME}
            SELECT *
            FROM prices_df
            WHERE (symbol, date) NOT IN (
                SELECT symbol, date FROM {TABLE_NAME}
            )
        """)

        print(f"\nInserted {len(prices_df)} new rows.")

        # -----------------------------
        # 7. Sanity check
        # -----------------------------
        print(
            con.execute(f"""
            SELECT
                symbol,
                COUNT(*) AS rows,
                MIN(date) AS start_date,
                MAX(date) AS end_date
            FROM {TABLE_NAME}
            GROUP BY symbol
            """).fetchdf()
        )
    else:
        print("Database is already up to date.")

finally:
    # -----------------------------
    # 8. Always close the connection
    # -----------------------------
    con.close()
