import os
import sys
import pandas as pd
import polars as pl
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add stock_report/code to path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

import market_data
import utils
from d1_uploader import D1Uploader

def sync_stock_prices(symbol, uploader):
    try:
        ticker = utils.get_ticker(symbol)
        # 10 years of historical closing price
        hist = ticker.history(period="10y")
        if hist is not None and not hist.empty:
            # Extract just Date and Close
            hist_reset = hist.reset_index()
            # If Date is a DatetimeIndex with timezone, convert to just date string
            if 'Date' in hist_reset.columns:
                hist_reset['date_str'] = hist_reset['Date'].dt.strftime('%Y-%m-%d')
            else:
                return f"Error: No Date column for {symbol}"

            price_records = [
                {'date': row['date_str'], 'close': float(row['Close'])}
                for _, row in hist_reset.iterrows()
            ]
            
            # Upsert into D1
            uploader.upsert_prices(symbol, price_records)
            return f"Success: {symbol} ({len(price_records)} rows)"
    except Exception as e:
        return f"Error syncing {symbol}: {e}"
    return f"No data for {symbol}"

def main():
    # Fetch all S&P 500 tickers
    print("S&P 500リストを取得中...")
    df_sp500 = market_data.fetch_sp500_companies_optimized()
    symbols = df_sp500['Symbol_YF'].to_list()
    
    print(f"{len(symbols)} 銘柄の終値をD1に同期中...")
    uploader = D1Uploader()
    
    # Use ThreadPoolExecutor for parallel processing if needed, 
    # but D1 API might rate limit, so we'll do one by one for now or with small concurrency
    max_workers = 3
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(sync_stock_prices, s, uploader): s for s in symbols}
        for future in tqdm(as_completed(futures), total=len(symbols)):
            result = future.result()
            # print(result)

if __name__ == "__main__":
    main()
