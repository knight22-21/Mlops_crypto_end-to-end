# src/ingestion/coingecko_ingest.py
import os
import time
import json
import requests
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Prometheus metrics
from src.monitoring.metrics import INGEST_CALLS, INGEST_ERRORS, INGEST_DURATION, LAST_INGEST_TIMESTAMP

load_dotenv()  # loads .env

# Config from env
DATABASE_URL = os.getenv("DATABASE_URL")
COINGECKO_SYMBOL = os.getenv("COINGECKO_SYMBOL", "bitcoin")
COINGECKO_DAYS = int(os.getenv("COINGECKO_DAYS", "7"))
# Default interval - used for scheduling if you run loop
INGEST_INTERVAL_SECONDS = int(os.getenv("INGEST_INTERVAL_SECONDS", "3600"))

# CoinGecko endpoint
COINGECKO_MARKET_CHART = "https://api.coingecko.com/api/v3/coins/{id}/market_chart"

def fetch_hourly_prices(symbol_id="bitcoin", vs_currency="usd", days=7):
    """
    Fetch hourly price points for the last `days` from CoinGecko.
    Returns a pandas DataFrame with columns ['ts', 'close'].
    """
    params = {"vs_currency": vs_currency, "days": days}
    url = COINGECKO_MARKET_CHART.format(id=symbol_id)
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # `prices` is list of [timestamp_ms, price]
    prices = pd.DataFrame(data.get("prices", []), columns=["ts_ms", "close"])
    # convert to timestamp
    prices["ts"] = pd.to_datetime(prices["ts_ms"], unit="ms", utc=True)
    prices = prices[["ts", "close"]]
    return prices, data  # return raw `data` for storing if helpful

def upsert_prices_to_db(df: pd.DataFrame, symbol="BTC", source="coingecko", raw=None):
    """
    Insert price rows to Postgres. We use SQLAlchemy to talk to Supabase Postgres.
    We do simple INSERT ... ON CONFLICT DO NOTHING pattern by deduplicating at client side.
    """
    if df.empty:
        return 0
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    with engine.begin() as conn:
        # optionally deduplicate existing timestamps:
        # find timestamps already in DB for this symbol
        ts_list = tuple(df['ts'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').tolist())
        if len(ts_list) == 0:
            return 0
        # query existing ts
        q = text("SELECT ts FROM prices_hourly WHERE symbol = :symbol AND ts = ANY(:ts_array)")
        # Postgres driver expects list, pass as list
        existing = conn.execute(text("SELECT ts FROM prices_hourly WHERE symbol = :symbol AND ts = ANY(:ts_array)"),
                                {"symbol": symbol, "ts_array": list(df['ts'].dt.tz_convert('UTC').tolist())}).fetchall()
        # Build set of existing ISO strings
        existing_ts = set([r[0].isoformat() for r in existing]) if existing else set()

        insert_count = 0
        for _, row in df.iterrows():
            ts = row['ts'].to_pydatetime()
            iso_ts = ts.isoformat()
            if iso_ts in existing_ts:
                continue
            # Insert
            conn.execute(
                text(
                    "INSERT INTO prices_hourly (symbol, ts, close, source, raw) VALUES (:symbol, :ts, :close, :source, :raw)"
                ),
                {"symbol": symbol, "ts": ts, "close": float(row['close']), "source": source, "raw": json.dumps(raw)}
            )
            insert_count += 1
    return insert_count

@INGEST_DURATION.time()
def run_once():
    try:
        prices_df, raw = fetch_hourly_prices(COINGECKO_SYMBOL, "usd", COINGECKO_DAYS)
        # normalize symbol label (we store 3-letter)
        symbol_label = "BTC" if COINGECKO_SYMBOL.lower() in ("bitcoin", "btc") else COINGECKO_SYMBOL.upper()
        count = upsert_prices_to_db(prices_df, symbol=symbol_label, source="coingecko", raw=raw)
        INGEST_CALLS.inc()
        LAST_INGEST_TIMESTAMP.set_to_current_time()
        print(f"[ingest] inserted {count} rows for {symbol_label}")
        return count
    except Exception as e:
        INGEST_ERRORS.inc()
        print("[ingest][error]", str(e))
        raise

if __name__ == "__main__":
    # simple loop-based scheduler for development:
    while True:
        try:
            run_once()
        except Exception:
            pass
        time.sleep(INGEST_INTERVAL_SECONDS)
