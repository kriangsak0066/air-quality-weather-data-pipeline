CREATE SCHEMA IF NOT EXISTS mart;

CREATE OR REPLACE TABLE mart.pm25_latest_dashboard AS
SELECT
    sensor_id,
    location_id,
    parameter,
    unit,
    value AS pm25_value,
    measured_at_utc,
    ingested_at_utc,
    latitude,
    longitude,

    DATE_DIFF('hour', measured_at_utc, ingested_at_utc) AS measurement_age_hours,

    CASE
        WHEN value < 0 THEN 'Invalid'
        WHEN value <= 12 THEN 'Good'
        WHEN value <= 35.4 THEN 'Moderate'
        WHEN value <= 55.4 THEN 'Unhealthy for Sensitive Groups'
        WHEN value <= 150.4 THEN 'Unhealthy'
        WHEN value <= 250.4 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS pm25_category,

    CASE
        WHEN is_recent_measurement THEN 'Recent'
        ELSE 'Stale'
    END AS freshness_status,

    CASE
        WHEN is_valid_pm25_value
         AND is_recent_measurement
         AND has_valid_coordinates
        THEN 'Pass'
        ELSE 'Review'
    END AS data_quality_status,

    is_valid_pm25_value,
    is_recent_measurement,
    has_valid_coordinates

FROM dw.pm25_measurements;