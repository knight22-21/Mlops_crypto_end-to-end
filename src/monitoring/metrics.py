# src/monitoring/metrics.py
from prometheus_client import Counter, Summary, Gauge

# Ingestion counters
INGEST_CALLS = Counter('ingest_calls_total', 'Total successful ingestion calls')
INGEST_ERRORS = Counter('ingest_errors_total', 'Total ingestion errors')
INGEST_DURATION = Summary('ingest_duration_seconds', 'Duration of ingestion operations in seconds')

# DB gauges
LAST_INGEST_TIMESTAMP = Gauge('last_ingest_timestamp_unixtime', 'Unix timestamp of last successful ingestion')


# Phase 2 metrics
preprocess_duration = Gauge("preprocess_duration_seconds", "Time taken for preprocessing")
missing_values_handled = Gauge("missing_values_count", "Number of missing values handled")