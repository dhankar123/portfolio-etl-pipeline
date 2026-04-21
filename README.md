# Portfolio ETL Pipeline

A simple, production-style ETL project in Python for portfolio use.
It demonstrates modular design, data quality checks, logging, metadata tracking, and unit tests.

## Overview

This pipeline processes raw sales data and produces curated analytics-ready output.

- **Extract:** Read raw data from CSV.
- **Transform:** Validate schema, clean records, convert types, and derive metrics.
- **Load:** Save curated data and run metadata.

## Tech Stack

- Python
- Pandas
- SQLAlchemy
- PostgreSQL (optional load target)
- Pytest
- GitHub Actions (CI)
- Docker and Docker Compose

## Project Structure

```text
.
|-- data
|   |-- raw
|   |   `-- sales_raw.csv
|   `-- curated
|-- logs
|-- src
|   `-- etl_pipeline
|       |-- __init__.py
|       |-- config.py
|       |-- extract.py
|       |-- transform.py
|       |-- load.py
|       |-- logging_config.py
|       |-- models.py
|       `-- pipeline.py
`-- tests
    `-- test_transform.py
```

## Features

- Modular ETL layers (`extract`, `transform`, `load`)
- Config-driven paths via `PipelineConfig`
- Structured logging to file and console
- Data quality validation and filtering
- Optional PostgreSQL load target
- Derived business metrics:
  - `gross_revenue = quantity * unit_price`
  - `net_revenue = gross_revenue * (1 - discount_pct)`
- Run metadata output (timestamp + row counts)
- Unit tests for transform logic

## What To Use For Specific Tasks

- **Task: Run a basic ETL job locally**
  - Use: `python -m etl_pipeline.pipeline`
  - Why: Runs extract, transform, and CSV load quickly for local development.

- **Task: Validate data cleaning and business logic**
  - Use: `src/etl_pipeline/transform.py` + `pytest`
  - Why: Transform module contains schema checks, filtering, and derived metrics; tests verify behavior.

- **Task: Trace failures or debug pipeline behavior**
  - Use: `logs/pipeline.log`
  - Why: Structured logs show stage-wise progress and row counts.

- **Task: Share run proof (audit/reporting)**
  - Use: `data/curated/pipeline_run_metadata.json`
  - Why: Stores timestamp and run metrics (`rows_extracted`, `rows_transformed`, `rows_loaded`).

- **Task: Load curated data into a real database**
  - Use: `ENABLE_POSTGRES_LOAD=true` with `POSTGRES_URL` and `POSTGRES_TABLE_NAME`
  - Why: Persists output directly to PostgreSQL table for downstream BI/analytics.

- **Task: Run full stack without local dependency setup**
  - Use: `docker compose up --build`
  - Why: Starts PostgreSQL and ETL runner in containers with consistent environment.

- **Task: Keep code quality checked automatically**
  - Use: `.github/workflows/ci.yml`
  - Why: CI runs tests on push/PR and prevents broken code from being merged.

- **Task: Change input/output locations or deployment settings**
  - Use: `src/etl_pipeline/config.py` and environment variables
  - Why: Config-driven setup avoids hardcoded paths and eases environment changes.

## Quick Start

1. Install dependencies:

```bash
pip install -e ".[dev]"
```

2. Run the pipeline:

```bash
python -m etl_pipeline.pipeline
```

3. Run tests:

```bash
pytest
```

## Environment Variables

- `ENABLE_POSTGRES_LOAD` (default: `false`)
  - Purpose: enables PostgreSQL load when set to `true`.
- `POSTGRES_URL` (default: `postgresql+psycopg://etl_user:etl_password@localhost:5432/etl_db`)
  - Purpose: SQLAlchemy connection string for database load.
- `POSTGRES_TABLE_NAME` (default: `sales_curated`)
  - Purpose: target table name for curated dataset.

## PostgreSQL Load (Optional)

The pipeline can also load curated data into PostgreSQL.

Set environment variables:

```bash
ENABLE_POSTGRES_LOAD=true
POSTGRES_URL=postgresql+psycopg://etl_user:etl_password@localhost:5432/etl_db
POSTGRES_TABLE_NAME=sales_curated
```

Then run:

```bash
python -m etl_pipeline.pipeline
```

If `ENABLE_POSTGRES_LOAD` is not `true`, the pipeline only writes CSV and metadata files.

## Docker Setup

1. Start PostgreSQL and run ETL in containers:

```bash
docker compose up --build
```

2. Stop containers:

```bash
docker compose down
```

The Compose setup runs:
- `postgres` (database service)
- `etl` (pipeline runner service)

## CI Pipeline

GitHub Actions workflow is included at `.github/workflows/ci.yml`.
It runs on push and pull requests, installs dependencies, and executes `pytest`.

## Output Files

After running, check:

- Curated dataset: `data/curated/sales_curated.csv`
- Run metadata: `data/curated/pipeline_run_metadata.json`
- Logs: `logs/pipeline.log`

## Project Creation Flow

This is the sequence used to build this project:

1. Define use case (sales ETL for analytics output)
2. Create modular folder and package structure
3. Centralize paths and settings in config
4. Build extract module with input validation
5. Build transform module for cleaning and business logic
6. Build load module for curated output and metadata
7. Add logging for observability
8. Add tests for transformation rules
9. Run end-to-end and verify artifacts

## Concepts Used

- **ETL pattern:** Extract -> Transform -> Load
- **Separation of concerns:** One responsibility per module
- **Config-driven design:** Environment and path flexibility
- **Data quality checks:** Required columns, valid types, valid rows
- **Observability:** Logging and run-level metadata
- **Testability:** Unit tests for core transformations

## Runtime Flow

When running `python -m etl_pipeline.pipeline`:

1. Load config and initialize logging
2. Extract raw CSV into DataFrame
3. Transform and validate data
4. Load curated output CSV
5. Write pipeline metadata JSON
6. Return run metrics

## Portfolio Pitch (Short)

"Built a production-style ETL pipeline in Python with modular architecture, data validation, derived business metrics, structured logging, run metadata, and unit tests."

## Next Improvements

- Add orchestration (Prefect or Airflow)
- Add linting checks in CI (ruff/black)
- Add incremental loading with watermark logic
