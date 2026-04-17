import yfinance as yf
import requests
import os
import json
from datetime import datetime

def fetch_and_send():
    ticker_symbol = "AAPL"
    api_url = os.getenv("API_URL") # 例: https://your-project.pages.dev/api/insert
    api_secret = os.getenv("API_SECRET_KEY")

    if not api_url or not api_secret:
        print("API_URL or API_SECRET_KEY is not set.")
        return

    # 株価取得
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period="1d") # 最新の1日分

    if df.empty:
        print("No data found for", ticker_symbol)
        return

    # データの整形
    latest_data = df.iloc[-1]
    date_str = df.index[-1].strftime('%Y-%m-%d')
    
    payload = {
        "ticker": ticker_symbol,
        "date": date_str,
        "open": float(latest_data["Open"]),
        "high": float(latest_data["High"]),
        "low": float(latest_data["Low"]),
        "close": float(latest_data["Close"]),
        "volume": int(latest_data["Volume"])
    }

    print(f"Sending data for {date_str}...")

    # API送信
    headers = {
        "Content-Type": "application/json",
        "X-API-SECRET-KEY": api_secret
    }
    
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        print("Successfully updated D1 via API.")
    else:
        print(f"Failed to update D1: {response.status_code} - {response.text}")

if __name__ == "__main__":
    fetch_and_send()
