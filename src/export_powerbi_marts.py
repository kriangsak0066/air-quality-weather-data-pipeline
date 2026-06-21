from pathlib import Path

import duckdb


DATABASE_PATH = "air_quality.duckdb"
EXPORT_DIR = Path("data/powerbi")


TABLE_EXPORTS = {
    "mart.pm25_latest_dashboard": "pm25_latest_dashboard.csv",
    "mart.pm25_weather_dashboard": "pm25_weather_dashboard.csv",
    "dq.pm25_quality_summary": "pm25_quality_summary.csv",
    "dq.pipeline_quality_summary": "pipeline_quality_summary.csv",
}


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    with duckdb.connect(DATABASE_PATH) as conn:
        for table_name, file_name in TABLE_EXPORTS.items():
            output_path = EXPORT_DIR / file_name

            conn.execute(
                f"""
                COPY (
                    SELECT *
                    FROM {table_name}
                )
                TO ?
                WITH (HEADER, DELIMITER ',');
                """,
                [str(output_path)],
            )

            row_count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name};"
            ).fetchone()[0]

            print(f"Exported {table_name} -> {output_path} ({row_count} rows)")


if __name__ == "__main__":
    main()