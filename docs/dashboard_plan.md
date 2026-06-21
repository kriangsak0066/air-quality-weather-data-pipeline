# Dashboard Plan

## Objective

The dashboard will help analysts monitor PM2.5 levels, identify stale measurements, and understand data quality risks before using air quality metrics for decision-making.

Primary mart tables:

```text
mart.pm25_latest_dashboard
mart.pm25_weather_dashboard
```

Data quality tables:

```text
dq.pm25_quality_summary
dq.pipeline_quality_summary
```

## Page 1: Executive Overview

Main questions:

- How many PM2.5 measurements are available?
- What percentage of measurements are recent?
- What percentage of PM2.5 values are valid?
- How many records need review?

Suggested visuals:

- KPI card: Total measurements
- KPI card: Recent measurement rate
- KPI card: Valid PM2.5 value rate
- KPI card: Review records
- Bar chart: PM2.5 category distribution
- Donut chart: Data quality status

## Page 2: Air Quality Monitoring

Main questions:

- Which sensors currently report the highest PM2.5 values?
- Which measurements are recent enough to trust?
- Where are high PM2.5 readings located?

Suggested visuals:

- Table: top PM2.5 values by sensor/location
- Map: latitude and longitude colored by PM2.5 category
- Bar chart: top sensors by PM2.5 value
- Filter: freshness status
- Filter: data quality status
- Scatter plot: PM2.5 value vs temperature or humidity

## Page 3: Data Quality

Main questions:

- How much data is stale?
- How many values are invalid?
- Are coordinates valid?
- Which records should be reviewed before analysis?
- What percentage of PM2.5 records matched weather data?

Suggested visuals:
- KPI card: weather match rate
- KPI card: combined pass rate
- KPI card: stale measurement rows
- KPI card: invalid PM2.5 value rows
- KPI card: valid coordinate rate
- Bar chart: data quality status by freshness status
- Table: records where `data_quality_status = 'Review'`

## Key Measures

Suggested Power BI measures:

```DAX
Total Measurements = COUNTROWS(pm25_latest_dashboard)

Recent Measurements =
CALCULATE(
    COUNTROWS(pm25_latest_dashboard),
    pm25_latest_dashboard[freshness_status] = "Recent"
)

Recent Measurement Rate =
DIVIDE([Recent Measurements], [Total Measurements])

Review Records =
CALCULATE(
    COUNTROWS(pm25_latest_dashboard),
    pm25_latest_dashboard[data_quality_status] = "Review"
)

Average PM2.5 =
AVERAGE(pm25_latest_dashboard[pm25_value])
```

## Next Dashboard Enhancements

- Add location names and country metadata
- Add weather variables from Open-Meteo
- Add historical trend pages
- Add data freshness monitoring by ingestion run