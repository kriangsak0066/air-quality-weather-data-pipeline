# Architecture

## Overview

This project follows a layered analytics pipeline pattern. Each layer has a specific responsibility, from preserving raw API responses to producing dashboard-ready tables.

```text
OpenAQ API + Open-Meteo API
  -> data/raw
  -> data/processed
  -> stg.latest_pm25 + stg.weather_hourly
  -> dw.pm25_measurements + dw.weather_hourly
  -> dq.pm25_quality_summary + dq.pipeline_quality_summary
  -> mart.pm25_latest_dashboard + mart.pm25_weather_dashboard
  -> Power BI
```

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Raw | Store the original JSON API response for traceability |
| Processed | Convert nested JSON records into flat CSV files |
| Staging | Load processed files into DuckDB while preserving source-like values |
| Warehouse | Parse data types and add business/data quality flags |
| Data Quality | Summarize checks for analyst trust and monitoring |
| Mart | Provide dashboard-ready fields and categories |

## Design Decisions

### Preserve raw data

The raw JSON response is stored before transformation. This makes the pipeline easier to audit, debug, and rerun when transformation logic changes.

### Keep staging close to source

Datetime fields are stored as strings in the staging table to avoid timezone conversion issues during initial loading. Datetime parsing is handled in the warehouse layer.

### Add quality flags instead of dropping rows

Invalid or stale records are kept in the warehouse table and marked with flags. This allows analysts to understand data quality issues instead of silently losing records.

### Separate data quality from dashboard marts

The data quality summary is stored in its own `dq` schema. The dashboard mart focuses on analyst-friendly fields such as PM2.5 category, freshness status, and data quality status.

## Current Limitation

The current weather ingestion uses a fixed Bangkok coordinate as a technical demo. Future iterations should fetch weather dynamically for PM2.5 sensor locations and support historical trends.