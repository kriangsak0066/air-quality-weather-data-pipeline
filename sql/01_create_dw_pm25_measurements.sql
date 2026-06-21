CREATE SCHEMA IF NOT EXISTS dw;

CREATE OR REPLACE TABLE dw.pm25_measurements AS
SELECT
    sensor_id,
    location_id,
    parameter,
    unit,
    value,
    CAST(datetime_utc AS TIMESTAMPTZ) AS measured_at_utc,
    datetime_local,
    latitude,
    longitude,
    CAST(ingested_at_utc AS TIMESTAMPTZ) AS ingested_at_utc,

    CASE
        WHEN value IS NOT NULL AND value >= 0 THEN TRUE
        ELSE FALSE
    END AS is_valid_pm25_value,

    CASE
        WHEN CAST(datetime_utc AS TIMESTAMPTZ) >= CAST(ingested_at_utc AS TIMESTAMPTZ) - INTERVAL 24 HOURS
        THEN TRUE
        ELSE FALSE
    END AS is_recent_measurement,

    CASE
        WHEN latitude BETWEEN -90 AND 90
         AND longitude BETWEEN -180 AND 180
        THEN TRUE
        ELSE FALSE
    END AS has_valid_coordinates

FROM stg.latest_pm25;