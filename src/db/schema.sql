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
