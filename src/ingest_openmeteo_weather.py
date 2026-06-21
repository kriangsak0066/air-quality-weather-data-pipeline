import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"

REQUESTED_LATITUDE = 13.7563
REQUESTED_LONGITUDE = 100.5018

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
]


def fetch_weather() -> dict:
    params = {
        "latitude": REQUESTED_LATITUDE,
        "longitude": REQUESTED_LONGITUDE,
        "hourly": HOURLY_VARIABLES,
        "forecast_days": 1,
        "timezone": "UTC",
    }

    response = requests.get(BASE_URL, params=params, timeout=30)

    print(f"Status code: {response.status_code}")
    print(f"Request URL: {response.url}")

    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response.json()


def normalize_hourly_weather(payload: dict) -> pd.DataFrame:
    hourly = payload.get("hourly", {})
    times = hourly.get("time", [])

    rows = []

    for index, forecast_time in enumerate(times):
        rows.append(
            {
                "forecast_time_utc": forecast_time,
                "requested_latitude": REQUESTED_LATITUDE,
                "requested_longitude": REQUESTED_LONGITUDE,
                "model_latitude": payload.get("latitude"),
                "model_longitude": payload.get("longitude"),
                "timezone": payload.get("timezone"),
                "elevation": payload.get("elevation"),
                "temperature_2m": hourly.get("temperature_2m", [None] * len(times))[index],
                "relative_humidity_2m": hourly.get("relative_humidity_2m", [None] * len(times))[index],
                "precipitation": hourly.get("precipitation", [None] * len(times))[index],
                "wind_speed_10m": hourly.get("wind_speed_10m", [None] * len(times))[index],
                "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    payload = fetch_weather()
    df = normalize_hourly_weather(payload)

    run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_file = raw_dir / f"openmeteo_weather_{run_timestamp}.json"
    processed_file = processed_dir / f"weather_hourly_{run_timestamp}.csv"

    with raw_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    df.to_csv(processed_file, index=False, encoding="utf-8")

    print(f"Raw file saved: {raw_file}")
    print(f"Processed file saved: {processed_file}")
    print(f"Rows saved: {len(df)}")

    print("\nPreview:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()