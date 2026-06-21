import os

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

url = f"{BASE_URL}/parameters/2/latest"

params = {
    "limit": 100,
    "page": 1
}

response = requests.get(url, headers=headers, params=params, timeout=30)

print(f"Status code: {response.status_code}")

if response.status_code != 200:
    print(response.text)
    response.raise_for_status()

payload = response.json()
records = payload.get("results", [])

rows = []

for record in records:
    coordinates = record.get("coordinates", {})
    datetime_info = record.get("datetime", {})

    rows.append(
        {
            "sensor_id": record.get("sensorsId"),
            "location_id": record.get("locationsId"),
            "parameter": "pm25",
            "unit": "µg/m³",
            "value": record.get("value"),
            "datetime_utc": datetime_info.get("utc"),
            "datetime_local": datetime_info.get("local"),
            "latitude": coordinates.get("latitude"),
            "longitude": coordinates.get("longitude"),
        }
    )
df = pd.DataFrame(rows)

print("\nRows fetched:", len(df))
print("\nColumns:")
print(df.columns.tolist())

print("\nPreview:")
print(df.head(10).to_string(index=False))