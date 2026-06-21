from pathlib import Path

import duckdb


DATABASE_PATH = "air_quality.duckdb"
PROCESSED_DIR = Path("data/processed")


def get_latest_processed_file() -> Path:
    files = sorted(PROCESSED_DIR.glob("latest_pm25_*.csv"))

    if not files:
        raise FileNotFoundError("No processed PM2.5 CSV files found in data/processed.")

    return files[-1]


def main() -> None:
    latest_file = get_latest_processed_file()

    print(f"Loading file: {latest_file}")

    with duckdb.connect(DATABASE_PATH) as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS stg;")

        conn.execute(
            """
            CREATE OR REPLACE TABLE stg.latest_pm25 AS
            SELECT
                CAST(sensor_id AS BIGINT) AS sensor_id,
                CAST(location_id AS BIGINT) AS location_id,
                CAST(parameter AS VARCHAR) AS parameter,
                CAST(unit AS VARCHAR) AS unit,
                CAST(value AS DOUBLE) AS value,
                CAST(datetime_utc AS VARCHAR) AS datetime_utc,
                CAST(datetime_local AS VARCHAR) AS datetime_local,
                CAST(latitude AS DOUBLE) AS latitude,
                CAST(longitude AS DOUBLE) AS longitude,
                CAST(ingested_at_utc AS VARCHAR) AS ingested_at_utc
            FROM read_csv_auto(?);
            """,
            [str(latest_file)],
        )

        row_count = conn.execute(
            "SELECT COUNT(*) FROM stg.latest_pm25;"
        ).fetchone()[0]

        preview = conn.execute(
            """
            SELECT *
            FROM stg.latest_pm25
            LIMIT 10;
            """
        ).fetchdf()

    print(f"Rows loaded: {row_count}")
    print("\nPreview:")
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()