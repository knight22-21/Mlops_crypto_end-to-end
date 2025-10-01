import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
print("Connecting to DB:", DB_URL)
def get_connection():
    return psycopg2.connect(DB_URL)

def fetch_raw_data():
    conn = get_connection()
    query = "SELECT timestamp, close FROM crypto_raw ORDER BY timestamp ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def store_processed_data(df: pd.DataFrame):
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO crypto_features
            (timestamp, close, lag_1h, lag_2h, lag_3h, lag_6h, lag_12h, lag_24h,
             ma_6h, ma_12h, rsi, macd, macd_signal, bollinger_hband, bollinger_lband)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING;
        """, tuple(row.values))
    conn.commit()
    conn.close()
