CREATE SCHEMA IF NOT EXISTS dq;

CREATE OR REPLACE TABLE dq.pipeline_quality_summary AS
WITH pm25_summary AS (
    SELECT
        COUNT(*) AS pm25_total_rows,
        SUM(CASE WHEN is_valid_pm25_value THEN 1 ELSE 0 END) AS valid_pm25_value_rows,
        SUM(CASE WHEN NOT is_valid_pm25_value THEN 1 ELSE 0 END) AS invalid_pm25_value_rows,
        SUM(CASE WHEN is_recent_measurement THEN 1 ELSE 0 END) AS recent_pm25_rows,
        SUM(CASE WHEN NOT is_recent_measurement THEN 1 ELSE 0 END) AS stale_pm25_rows,
        SUM(CASE WHEN has_valid_coordinates THEN 1 ELSE 0 END) AS valid_pm25_coordinate_rows
    FROM dw.pm25_measurements
),

weather_summary AS (
    SELECT
        COUNT(*) AS weather_total_rows,
        SUM(CASE WHEN is_valid_temperature THEN 1 ELSE 0 END) AS valid_temperature_rows,
        SUM(CASE WHEN is_valid_humidity THEN 1 ELSE 0 END) AS valid_humidity_rows,
        SUM(CASE WHEN is_valid_precipitation THEN 1 ELSE 0 END) AS valid_precipitation_rows,
        SUM(CASE WHEN is_valid_wind_speed THEN 1 ELSE 0 END) AS valid_wind_speed_rows,
        SUM(CASE WHEN has_valid_coordinates THEN 1 ELSE 0 END) AS valid_weather_coordinate_rows
    FROM dw.weather_hourly
),

join_summary AS (
    SELECT
        COUNT(*) AS joined_total_rows,
        SUM(CASE WHEN has_weather_match THEN 1 ELSE 0 END) AS weather_match_rows,
        SUM(CASE WHEN NOT has_weather_match THEN 1 ELSE 0 END) AS missing_weather_match_rows,
        SUM(CASE WHEN combined_quality_status = 'Pass' THEN 1 ELSE 0 END) AS combined_pass_rows,
        SUM(CASE WHEN combined_quality_status = 'Review' THEN 1 ELSE 0 END) AS combined_review_rows
    FROM mart.pm25_weather_dashboard
)

SELECT
    pm25_summary.*,
    weather_summary.*,
    join_summary.*,

    ROUND(valid_pm25_value_rows * 100.0 / NULLIF(pm25_total_rows, 0), 2) AS valid_pm25_value_pct,
    ROUND(recent_pm25_rows * 100.0 / NULLIF(pm25_total_rows, 0), 2) AS recent_pm25_pct,
    ROUND(valid_pm25_coordinate_rows * 100.0 / NULLIF(pm25_total_rows, 0), 2) AS valid_pm25_coordinate_pct,

    ROUND(valid_temperature_rows * 100.0 / NULLIF(weather_total_rows, 0), 2) AS valid_temperature_pct,
    ROUND(valid_humidity_rows * 100.0 / NULLIF(weather_total_rows, 0), 2) AS valid_humidity_pct,
    ROUND(valid_precipitation_rows * 100.0 / NULLIF(weather_total_rows, 0), 2) AS valid_precipitation_pct,
    ROUND(valid_wind_speed_rows * 100.0 / NULLIF(weather_total_rows, 0), 2) AS valid_wind_speed_pct,
    ROUND(valid_weather_coordinate_rows * 100.0 / NULLIF(weather_total_rows, 0), 2) AS valid_weather_coordinate_pct,

    ROUND(weather_match_rows * 100.0 / NULLIF(joined_total_rows, 0), 2) AS weather_match_pct,
    ROUND(combined_pass_rows * 100.0 / NULLIF(joined_total_rows, 0), 2) AS combined_pass_pct,
    ROUND(combined_review_rows * 100.0 / NULLIF(joined_total_rows, 0), 2) AS combined_review_pct

FROM pm25_summary
CROSS JOIN weather_summary
CROSS JOIN join_summary;