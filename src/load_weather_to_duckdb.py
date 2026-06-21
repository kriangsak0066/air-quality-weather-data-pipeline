from pathlib import Path

import duckdb


DATABASE_PATH = "air_quality.duckdb"
PROCESSED_DIR = Path("data/processed")


def get_latest_weather_file() -> Path:
    files = sorted(PROCESSED_DIR.glob("weather_hourly_*.csv"))

    if not files:
        raise FileNotFoundError("No processed weather CSV files found in data/processed.")

    return files[-1]


def main() -> None:
    latest_file = get_latest_weather_file()

    print(f"Loading file: {latest_file}")

    with duckdb.connect(DATABASE_PATH) as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS stg;")

        conn.execute(
            """
            CREATE OR REPLACE TABLE stg.weather_hourly AS
            SELECT
                CAST(forecast_time_utc AS VARCHAR) AS forecast_time_utc,
                CAST(requested_latitude AS DOUBLE) AS requested_latitude,
                CAST(requested_longitude AS DOUBLE) AS requested_longitude,
                CAST(model_latitude AS DOUBLE) AS model_latitude,
                CAST(model_longitude AS DOUBLE) AS model_longitude,
                CAST(timezone AS VARCHAR) AS timezone,
                CAST(elevation AS DOUBLE) AS elevation,
                CAST(temperature_2m AS DOUBLE) AS temperature_2m,
                CAST(relative_humidity_2m AS DOUBLE) AS relative_humidity_2m,
                CAST(precipitation AS DOUBLE) AS precipitation,
                CAST(wind_speed_10m AS DOUBLE) AS wind_speed_10m,
                CAST(ingested_at_utc AS VARCHAR) AS ingested_at_utc
            FROM read_csv_auto(?, all_varchar = true);
            """,
            [str(latest_file)],
        )

        row_count = conn.execute(
            "SELECT COUNT(*) FROM stg.weather_hourly;"
        ).fetchone()[0]

        preview = conn.execute(
            """
            SELECT *
            FROM stg.weather_hourly
            LIMIT 10;
            """
        ).fetchdf()

    print(f"Rows loaded: {row_count}")
    print("\nPreview:")
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()