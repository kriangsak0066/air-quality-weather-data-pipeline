CREATE SCHEMA IF NOT EXISTS dw;

CREATE OR REPLACE TABLE dw.weather_hourly AS
SELECT
    CAST(forecast_time_utc AS TIMESTAMPTZ) AS forecast_time_utc,
    requested_latitude,
    requested_longitude,
    model_latitude,
    model_longitude,
    timezone,
    elevation,
    temperature_2m,
    relative_humidity_2m,
    precipitation,
    wind_speed_10m,
    CAST(ingested_at_utc AS TIMESTAMPTZ) AS ingested_at_utc,

    CASE
        WHEN temperature_2m BETWEEN -60 AND 60 THEN TRUE
        ELSE FALSE
    END AS is_valid_temperature,

    CASE
        WHEN relative_humidity_2m BETWEEN 0 AND 100 THEN TRUE
        ELSE FALSE
    END AS is_valid_humidity,

    CASE
        WHEN precipitation >= 0 THEN TRUE
        ELSE FALSE
    END AS is_valid_precipitation,

    CASE
        WHEN wind_speed_10m >= 0 THEN TRUE
        ELSE FALSE
    END AS is_valid_wind_speed,

    CASE
        WHEN requested_latitude BETWEEN -90 AND 90
         AND requested_longitude BETWEEN -180 AND 180
         AND model_latitude BETWEEN -90 AND 90
         AND model_longitude BETWEEN -180 AND 180
        THEN TRUE
        ELSE FALSE
    END AS has_valid_coordinates

FROM stg.weather_hourly;