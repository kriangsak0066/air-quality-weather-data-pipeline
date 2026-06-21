import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")
BASE_URL = "https://api.openaq.org/v3"

if not API_KEY:
    raise ValueError("OPENAQ_API_KEY is missing. Please add it to your .env file.")

headers = {
    "X-API-Key": API_KEY
}

params = {
    "limit": 100,
    "page": 1
}

url = f"{BASE_URL}/parameters/2/latest"

response = requests.get(url, headers=headers, params=params, timeout=30)

print(f"Status code: {response.status_code}")

if response.status_code != 200:
    print(response.text)
    response.raise_for_status()

payload = response.json()
records = payload.get("results", [])

run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

raw_dir = Path("data/raw")
processed_dir = Path("data/processed")

raw_dir.mkdir(parents=True, exist_ok=True)
processed_dir.mkdir(parents=True, exist_ok=True)

raw_file = raw_dir / f"openaq_latest_pm25_{run_timestamp}.json"
processed_file = processed_dir / f"latest_pm25_{run_timestamp}.csv"

with raw_file.open("w", encoding="utf-8") as file:
    json.dump(payload, file, indent=2, ensure_ascii=False)

rows = []

for record in records:
    coordinates = record.get("coordinates", {})
    datetime_info = record.get("datetime", {})

    rows.append(
        {
            "sensor_id": record.get("sensorsId"),
            "location_id": record.get("locationsId"),
            "parameter": "pm25",
            "unit": "ug/m3",
            "value": record.get("value"),
            "datetime_utc": datetime_info.get("utc"),
            "datetime_local": datetime_info.get("local"),
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
            "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )

df = pd.DataFrame(rows)

df.to_csv(processed_file, index=False, encoding="utf-8")

print(f"Raw file saved: {raw_file}")
print(f"Processed file saved: {processed_file}")
print(f"Rows saved: {len(df)}")

print("\nPreview:")
print(df.head(10).to_string(index=False))