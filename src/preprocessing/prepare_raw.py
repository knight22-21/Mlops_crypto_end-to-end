# src/preprocessing/prepare_raw.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def extract_to_raw():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    print("✅ Extracting from prices_hourly to crypto_raw...")

    # Optional: Clear existing raw table first (be careful in prod!)
    cur.execute("DELETE FROM crypto_raw")

    # Extract latest data from prices_hourly
    cur.execute("""
        INSERT INTO crypto_raw (timestamp, close)
        SELECT ts, close
        FROM prices_hourly
        ORDER BY ts
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Done!")

if __name__ == "__main__":
    extract_to_raw()
