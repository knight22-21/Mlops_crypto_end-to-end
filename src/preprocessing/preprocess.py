import time
from prometheus_client import start_http_server
from src.preprocessing.feature_engineering import add_features
from src.db.supabase_utils import fetch_raw_data, store_processed_data
from src.monitoring.metrics import preprocess_duration, missing_values_handled

def run_preprocessing():
    start_time = time.time()

    raw_df = fetch_raw_data()
    if raw_df.empty:
        print("⚠️ No raw data found in crypto_raw table.")
        return

    missing_count = raw_df.isnull().sum().sum()
    raw_df = raw_df.dropna().drop_duplicates()

    processed_df = add_features(raw_df)
    store_processed_data(processed_df)

    preprocess_duration.set(time.time() - start_time)
    missing_values_handled.set(missing_count)

    print("✅ Preprocessing complete.")

if __name__ == "__main__":
    # Expose Prometheus metrics on port 8001
    start_http_server(8001)
    run_preprocessing()
