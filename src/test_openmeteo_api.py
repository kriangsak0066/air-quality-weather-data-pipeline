import json

import requests


BASE_URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.7563,
    "longitude": 100.5018,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "forecast_days": 1,
    "timezone": "UTC",
}

response = requests.get(BASE_URL, params=params, timeout=30)

print(f"Status code: {response.status_code}")
print(f"Request URL: {response.url}")

if response.status_code != 200:
    print(response.text)
    response.raise_for_status()

data = response.json()

print("\nTop-level keys:")
print(data.keys())

print("\nResponse preview:")
print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])