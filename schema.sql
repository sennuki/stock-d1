CREATE TABLE IF NOT EXISTS stocks (
  ticker TEXT,
  date TEXT,
  open REAL,
  high REAL,
  low REAL,
  close REAL,
  volume INTEGER,
  PRIMARY KEY (ticker, date)
);
