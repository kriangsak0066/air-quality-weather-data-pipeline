CREATE SCHEMA IF NOT EXISTS dq;

CREATE OR REPLACE TABLE dq.pm25_quality_summary AS
WITH base AS (
    SELECT
        COUNT(*) AS total_rows,

        SUM(CASE WHEN sensor_id IS NULL THEN 1 ELSE 0 END) AS missing_sensor_id_rows,
        SUM(CASE WHEN location_id IS NULL THEN 1 ELSE 0 END) AS missing_location_id_rows,
        SUM(CASE WHEN measured_at_utc IS NULL THEN 1 ELSE 0 END) AS missing_measured_at_rows,
        SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) AS missing_value_rows,

        SUM(CASE WHEN is_valid_pm25_value THEN 1 ELSE 0 END) AS valid_pm25_value_rows,
        SUM(CASE WHEN NOT is_valid_pm25_value THEN 1 ELSE 0 END) AS invalid_pm25_value_rows,

        SUM(CASE WHEN is_recent_measurement THEN 1 ELSE 0 END) AS recent_measurement_rows,
        SUM(CASE WHEN NOT is_recent_measurement THEN 1 ELSE 0 END) AS stale_measurement_rows,

        SUM(CASE WHEN has_valid_coordinates THEN 1 ELSE 0 END) AS valid_coordinate_rows,
        SUM(CASE WHEN NOT has_valid_coordinates THEN 1 ELSE 0 END) AS invalid_coordinate_rows,

        MAX(ingested_at_utc) AS latest_ingested_at_utc
    FROM dw.pm25_measurements
)

SELECT
    total_rows,
    missing_sensor_id_rows,
    missing_location_id_rows,
    missing_measured_at_rows,
    missing_value_rows,
    valid_pm25_value_rows,
    invalid_pm25_value_rows,
    recent_measurement_rows,
    stale_measurement_rows,
    valid_coordinate_rows,
    invalid_coordinate_rows,

    ROUND(valid_pm25_value_rows * 100.0 / NULLIF(total_rows, 0), 2) AS valid_pm25_value_pct,
    ROUND(recent_measurement_rows * 100.0 / NULLIF(total_rows, 0), 2) AS recent_measurement_pct,
    ROUND(valid_coordinate_rows * 100.0 / NULLIF(total_rows, 0), 2) AS valid_coordinate_pct,

    latest_ingested_at_utc
FROM base;