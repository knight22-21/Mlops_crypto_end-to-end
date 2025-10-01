# Crypto Data Pipeline (MLOps End-to-End)

This repository implements an end-to-end data pipeline for collecting, processing, and feature engineering cryptocurrency price data, ready for downstream ML modeling and monitoring.

---

## Project Overview

The goal of this project is to build a robust pipeline that:

* Ingests hourly crypto price data from **CoinGecko** into a Postgres database (`prices_hourly` table).
* Extracts and prepares raw data (`crypto_raw` table).
* Performs feature engineering to create time-series features (`crypto_features` table).
* Enables monitoring, metrics, and later modeling.

The pipeline is designed with modular components to allow automation and extensibility.

---

## Architecture & Data Flow

```plaintext
CoinGecko API
     ↓
Ingestion (main_ingest_with_metrics.py)
     ↓
Postgres: prices_hourly
     ↓
Raw Data Preparation (prepare_raw.py)
     ↓
Postgres: crypto_raw
     ↓
Feature Engineering & Preprocessing (preprocess.py)
     ↓
Postgres: crypto_features
```

---

## Database Schema

* **prices_hourly**
  Stores raw hourly price points fetched from CoinGecko with timestamps, symbols, and raw JSON.

* **crypto_raw**
  Contains extracted timestamps and closing prices, simplified for feature engineering.

* **crypto_features**
  Stores processed features including lags, moving averages, RSI, MACD, Bollinger bands, etc.

---

## Getting Started

### Prerequisites

* Python 3.8+
* PostgreSQL or Supabase database
* Virtual environment (recommended)

### Setup

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/crypto-mlops.git
   cd crypto-mlops
   ```

2. Create and activate virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set your Supabase/Postgres DB URL in an environment variable:

   ```bash
   # PowerShell (Windows)
   $env:SUPABASE_DB_URL="postgresql://username:password@host:port/database"

   # macOS/Linux
   export SUPABASE_DB_URL="postgresql://username:password@host:port/database"
   ```

---

## Running the Pipeline

### 1. Ingest data from CoinGecko

Fetch latest crypto prices and store in `prices_hourly`:

```bash
python main_ingest_with_metrics.py
```

---

### 2. Prepare raw data for feature engineering

Extract simplified raw data into `crypto_raw` table:

```bash
python -m src.preprocessing.prepare_raw
```

---

### 3. Feature Engineering & Preprocessing

Generate time-series features and store in `crypto_features`:

```bash
python -m src.preprocessing.preprocess
```

---

## Verification

You can verify the pipeline outputs by querying your database:

```sql
SELECT * FROM prices_hourly ORDER BY ts DESC LIMIT 5;
SELECT * FROM crypto_raw ORDER BY timestamp DESC LIMIT 5;
SELECT * FROM crypto_features ORDER BY timestamp DESC LIMIT 5;
```

---

## Next Steps

* Automate pipeline runs with cron or workflow orchestrators (Airflow, Prefect, Dagster).
* Add ML model training and deployment based on `crypto_features`.
* Integrate monitoring dashboards (Grafana, Prometheus).
* Extend ingestion to multiple coins or data sources.


---

## Troubleshooting

* **Connection refused to Postgres:**
  Ensure your database is running and your `SUPABASE_DB_URL` env variable is correctly set.

* **ModuleNotFoundError for `src`:**
  Run scripts with `-m` flag from the project root, e.g.,

  ```bash
  python -m src.preprocessing.preprocess
  ```
