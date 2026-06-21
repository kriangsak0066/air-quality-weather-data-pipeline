CREATE SCHEMA IF NOT EXISTS mart;

CREATE OR REPLACE TABLE mart.pm25_weather_dashboard AS
WITH pm25 AS (
    SELECT
        sensor_id,
        location_id,
        parameter,
        unit,
        value AS pm25_value,
        measured_at_utc,
        DATE_TRUNC('hour', measured_at_utc) AS measured_hour_utc,
        ingested_at_utc AS pm25_ingested_at_utc,
        latitude AS pm25_latitude,
        longitude AS pm25_longitude,
        is_valid_pm25_value,
        is_recent_measurement,
        has_valid_coordinates AS has_valid_pm25_coordinates,

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
        END AS freshness_status
    FROM dw.pm25_measurements
),

weather AS (
    SELECT
        forecast_time_utc,
        temperature_2m,
        relative_humidity_2m,
        precipitation,
        wind_speed_10m,
        requested_latitude AS weather_requested_latitude,
        requested_longitude AS weather_requested_longitude,
        model_latitude AS weather_model_latitude,
        model_longitude AS weather_model_longitude,
        is_valid_temperature,
        is_valid_humidity,
        is_valid_precipitation,
        is_valid_wind_speed,
        has_valid_coordinates AS has_valid_weather_coordinates
    FROM dw.weather_hourly
)

SELECT
    pm25.sensor_id,
    pm25.location_id,
    pm25.pm25_value,
    pm25.pm25_category,
    pm25.measured_at_utc,
    pm25.measured_hour_utc,
    pm25.pm25_latitude,
    pm25.pm25_longitude,
    pm25.freshness_status,

    weather.forecast_time_utc AS weather_hour_utc,
    weather.temperature_2m,
    weather.relative_humidity_2m,
    weather.precipitation,
    weather.wind_speed_10m,
    weather.weather_requested_latitude,
    weather.weather_requested_longitude,
    weather.weather_model_latitude,
    weather.weather_model_longitude,

    CASE
        WHEN weather.forecast_time_utc IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_weather_match,

    CASE
        WHEN pm25.is_valid_pm25_value
         AND pm25.is_recent_measurement
         AND pm25.has_valid_pm25_coordinates
         AND COALESCE(weather.is_valid_temperature, FALSE)
         AND COALESCE(weather.is_valid_humidity, FALSE)
         AND COALESCE(weather.is_valid_precipitation, FALSE)
         AND COALESCE(weather.is_valid_wind_speed, FALSE)
         AND COALESCE(weather.has_valid_weather_coordinates, FALSE)
        THEN 'Pass'
        ELSE 'Review'
    END AS combined_quality_status

FROM pm25
LEFT JOIN weather
    ON pm25.measured_hour_utc = weather.forecast_time_utc;