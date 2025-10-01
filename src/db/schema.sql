-- src/db/schema.sql
-- Table to store hourly price points from CoinGecko
CREATE TABLE IF NOT EXISTS prices_hourly (
  id BIGSERIAL PRIMARY KEY,
  symbol TEXT NOT NULL, -- e.g., 'BTC'
  ts TIMESTAMP WITH TIME ZONE NOT NULL,
  close NUMERIC NOT NULL,
  source TEXT NOT NULL, -- e.g., 'coingecko'
  raw JSONB,            -- optional raw data for debugging
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- simple index for efficient latest queries
CREATE INDEX IF NOT EXISTS idx_prices_symbol_ts ON prices_hourly(symbol, ts DESC);


-- Raw data table (Phase 1)
CREATE TABLE IF NOT EXISTS crypto_raw (
    timestamp TIMESTAMP PRIMARY KEY,
    close FLOAT
);

-- Processed features table (Phase 2)
CREATE TABLE IF NOT EXISTS crypto_features (
    timestamp TIMESTAMP PRIMARY KEY,
    close FLOAT,
    lag_1h FLOAT, lag_2h FLOAT, lag_3h FLOAT,
    lag_6h FLOAT, lag_12h FLOAT, lag_24h FLOAT,
    ma_6h FLOAT, ma_12h FLOAT,
    rsi FLOAT, macd FLOAT, macd_signal FLOAT,
    bollinger_hband FLOAT, bollinger_lband FLOAT
);
