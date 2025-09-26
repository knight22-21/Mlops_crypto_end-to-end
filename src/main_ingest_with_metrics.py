# src/main_ingest_with_metrics.py

import time
import threading
from fastapi import FastAPI
from prometheus_client import make_asgi_app
import uvicorn

from src.ingestion.coingecko_ingest import run_once, INGEST_INTERVAL_SECONDS

# Start Prometheus metrics server
app = FastAPI()
app.mount("/metrics", make_asgi_app())

def ingestion_loop():
    while True:
        try:
            run_once()
        except Exception as e:
            print("[main][error in ingestion]", str(e))
        time.sleep(INGEST_INTERVAL_SECONDS)

if __name__ == "__main__":
    # Run ingestion in background thread
    t = threading.Thread(target=ingestion_loop, daemon=True)
    t.start()

    # Start the metrics HTTP server (for Prometheus)
    uvicorn.run(app, host="0.0.0.0", port=8000)
