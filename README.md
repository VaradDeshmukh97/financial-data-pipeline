# Financial Data Pipeline

A compact, runnable example of a point-in-time financial data pipeline. It ingests financial observations from CSV, validates and normalizes records, stores them in SQLite, and creates an as-of snapshot.

**All sample data is synthetic. This is a personal portfolio demonstration, not an RCK production system.**

## Run

Requires Python 3.10+ and no third-party runtime dependencies.

```bash
python -m financial_data_pipeline.cli ingest data/sample_financials.csv --db outputs/financials.db
python -m financial_data_pipeline.cli snapshot --db outputs/financials.db --as-of-date 2025-04-01 --output outputs/snapshot.csv
```

## Why this is relevant

Financial research needs more than a number and a period. It needs to know **when the information became available**, which source it came from, which unit it uses, and whether it can be reproduced later. The pipeline therefore separates `period_end` from `available_date` and applies the as-of cutoff when producing a snapshot.

## Design choices

- Validation happens before persistence; invalid rows are rejected with row-level messages.
- Metric labels are normalized to a small canonical taxonomy.
- SQLite enforces an idempotent key on company, metric, period and availability date.
- Source name and source URL are retained with each observation.
- Parsing, validation, persistence and snapshot generation are separated.

## Scope

The example does not connect to SEC endpoints, market-data providers or client databases. A production implementation would require provider adapters, governed metric taxonomies, currency/unit conversion, restatement handling, richer audit trails, access controls and monitoring.
