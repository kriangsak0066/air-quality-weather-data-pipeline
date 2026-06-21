import sys
from pathlib import Path

import duckdb


DATABASE_PATH = "air_quality.duckdb"


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError("Usage: python src/run_sql_file.py <sql_file_path>")

    sql_file = Path(sys.argv[1])

    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql_text = sql_file.read_text(encoding="utf-8")

    with duckdb.connect(DATABASE_PATH) as conn:
        conn.execute(sql_text)

    print(f"Executed SQL file: {sql_file}")


if __name__ == "__main__":
    main()