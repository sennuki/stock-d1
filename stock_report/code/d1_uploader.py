import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class D1Uploader:
    def __init__(self):
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.database_id = os.getenv("CLOUDFLARE_D1_DATABASE_ID")
        
        if not all([self.api_token, self.account_id, self.database_id]):
            print("Warning: Cloudflare environment variables are not fully set.")

    def execute_query(self, sql, params=None):
        """D1 APIを使用してSQLクエリを実行する"""
        if not self.api_token:
            return None
            
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "sql": sql,
            "params": params or []
        }
        
        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error executing D1 query: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None

    def upsert_stock(self, symbol, name_ja=None, sector=None, industry=None, market_cap=None, daily_change=None, current_price=None, is_recent_actual=False):
        """銘柄情報を更新または挿入する"""
        sql = """
        INSERT INTO stocks (symbol, name_ja, sector, industry, market_cap, daily_change, current_price, is_recent_actual, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(symbol) DO UPDATE SET
            name_ja=COALESCE(excluded.name_ja, stocks.name_ja),
            sector=COALESCE(excluded.sector, stocks.sector),
            industry=COALESCE(excluded.industry, stocks.industry),
            market_cap=COALESCE(excluded.market_cap, stocks.market_cap),
            daily_change=COALESCE(excluded.daily_change, stocks.daily_change),
            current_price=COALESCE(excluded.current_price, stocks.current_price),
            is_recent_actual=COALESCE(excluded.is_recent_actual, stocks.is_recent_actual),
            last_updated=CURRENT_TIMESTAMP
        """
        return self.execute_query(sql, [symbol, name_ja, sector, industry, market_cap, daily_change, current_price, 1 if is_recent_actual else 0])

    def upsert_fundamentals(self, data_list):
        """財務データを一括更新または挿入する"""
        # Note: D1 API allows batching but for simplicity we'll do one query
        # In production, use batch endpoint for better performance
        results = []
        for d in data_list:
            sql = """
            INSERT INTO fundamentals (symbol, period_type, item, date, value)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(symbol, period_type, item, date) DO UPDATE SET
                value=excluded.value
            """
            res = self.execute_query(sql, [d['symbol'], d['period_type'], d['item'], d['date'], d['value']])
            results.append(res)
        return results

    def upsert_prices(self, symbol, df_prices):
        """株価データ(pandas/polars)を挿入する"""
        # ここでは数件ずつバッチ処理することを推奨
        pass

    def upsert_analysis_report(self, symbol, content_markdown, model_name=None):
        """分析レポート（変動理由など）を更新または挿入する"""
        sql = """
        INSERT INTO analysis_reports (symbol, content_markdown, model_name, generated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(symbol) DO UPDATE SET
            content_markdown=excluded.content_markdown,
            model_name=COALESCE(excluded.model_name, analysis_reports.model_name),
            generated_at=CURRENT_TIMESTAMP
        """
        return self.execute_query(sql, [symbol, content_markdown, model_name])
