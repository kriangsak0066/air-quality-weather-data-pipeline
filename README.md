# Air Quality & Weather Analytics Pipeline

A data engineering portfolio project that ingests PM2.5 air quality data from the OpenAQ API, stores raw and processed files, loads data into DuckDB, and builds staging, warehouse, data quality, and dashboard-ready mart tables.

## Project Objective

This project demonstrates an end-to-end analytics pipeline for air quality monitoring. The goal is to help analysts understand PM2.5 levels, data freshness, measurement quality, and dashboard-ready air quality categories.

## Architecture

```text
OpenAQ API
  -> Raw JSON files
  -> Processed CSV files
  -> DuckDB staging table
  -> Cleaned warehouse table
  -> Data quality summary
  -> Dashboard mart
```

## Tech Stack

- Python
- OpenAQ API
- pandas
- DuckDB
- SQL
- python-dotenv
- Power BI-ready mart tables

## Data Layers

| Layer | Object | Purpose |
|---|---|---|
| Raw | `data/raw/*.json` | Store original API response |
| Processed | `data/processed/*.csv` | Flatten API response into tabular format |
| Staging | `stg.latest_pm25` | Preserve source-like data in DuckDB |
| Warehouse | `dw.pm25_measurements` | Parse types and add quality flags |
| Data Quality | `dq.pm25_quality_summary` | Summarize data quality checks |
| Mart | `mart.pm25_latest_dashboard` | Dashboard-ready PM2.5 table |

## Key Data Quality Checks

- PM2.5 value must be non-negative
- Measurement timestamp must be recent within 24 hours
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- Sensor ID and location ID should not be missing

## Current Data Quality Findings

Based on the latest ingestion run:

| Metric | Result |
|---|---:|
| Total rows | 100 |
| Valid PM2.5 value rows | 96 |
| Invalid PM2.5 value rows | 4 |
| Recent measurement rows | 45 |
| Stale measurement rows | 55 |
| Valid coordinate rows | 100 |
| Valid PM2.5 value rate | 96% |
| Recent measurement rate | 45% |
| Valid coordinate rate | 100% |

## Dashboard Mart

The table `mart.pm25_latest_dashboard` includes:

- PM2.5 value
- PM2.5 category
- Measurement age in hours
- Freshness status
- Data quality status
- Sensor and location IDs
- Latitude and longitude

## How to Run

Create and activate a virtual environment:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAQ_API_KEY=your_api_key_here
```

Run the pipeline:

```powershell
python src\ingest_latest_pm25.py
python src\load_pm25_to_duckdb.py
python src\run_sql_file.py sql\01_create_dw_pm25_measurements.sql
python src\run_sql_file.py sql\02_create_dq_pm25_summary.sql
python src\run_sql_file.py sql\03_create_mart_pm25_latest_dashboard.sql
```

## Next Steps

- Add Open-Meteo weather data
- Join PM2.5 measurements with weather variables
- Build Power BI dashboard pages
- Add automated data quality tests
- Add orchestration with Airflow