-- 銘柄マスター
CREATE TABLE IF NOT EXISTS stocks (
    symbol TEXT PRIMARY KEY,
    name_ja TEXT,
    sector TEXT,
    industry TEXT,
    market_cap REAL,
    daily_change REAL,
    current_price REAL,
    is_recent_actual INTEGER DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 財務データ (縦持ち)
CREATE TABLE IF NOT EXISTS fundamentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    period_type TEXT NOT NULL, -- 'annual' or 'quarterly'
    item TEXT NOT NULL,         -- 'Revenue', 'Net Income', etc.
    date TEXT NOT NULL,         -- 'YYYY-MM-DD'
    value REAL,
    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_fundamentals_unique ON fundamentals(symbol, period_type, item, date);

-- 株価データ
CREATE TABLE IF NOT EXISTS prices (
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume INTEGER,
    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
);

-- 分析レポート
CREATE TABLE IF NOT EXISTS analysis_reports (
    symbol TEXT PRIMARY KEY,
    content_markdown TEXT,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    model_name TEXT,
    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
);
