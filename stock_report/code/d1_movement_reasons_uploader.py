# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import polars as pl
from dotenv import load_dotenv

# モジュールのインポートを可能にするためパスを追加
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from movement_reasons import process_top_movers, GEMINI_MODEL
from d1_uploader import D1Uploader
import utils

load_dotenv(os.path.join(os.path.dirname(base_dir), ".env"))

def sync_movement_reasons_to_d1(df_metrics):
    """
    トップ騰落銘柄の変動理由を生成し、Cloudflare D1に保存する
    """
    print("トップ騰落銘柄の変動理由の生成とD1への同期を開始します...")
    
    # 1. 理由を生成
    reasons = process_top_movers(df_metrics)
    if not reasons:
        print("変動理由が生成されませんでした。")
        return

    # 2. D1に保存
    uploader = D1Uploader()
    success_count = 0
    
    for symbol, data in reasons.items():
        print(f"D1に同期中: {symbol}")
        content = data.get('reason')
        if content:
            # analysis_reportsテーブルに保存
            res = uploader.upsert_analysis_report(
                symbol, 
                content, 
                model_name=GEMINI_MODEL
            )
            if res:
                success_count += 1
                
                # stocksテーブルのis_recent_actualフラグも更新
                uploader.upsert_stock(
                    symbol, 
                    is_recent_actual=True
                )
    
    print(f"D1への同期が完了しました。 (成功: {success_count}/{len(reasons)})")

if __name__ == "__main__":
    # 単体実行用のテストコード
    # 実際には main.py から df_metrics を渡して呼び出される想定
    import market_data
    
    print("テスト実行: 最新の指標データを取得中...")
    # market_dataからSP500の指標を取得するなどの処理 (簡略化)
    # 本番では main.py の flow に組み込む
    pass
