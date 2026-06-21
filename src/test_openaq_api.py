import json
import os

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

location_id = 8118
url = f"{BASE_URL}/locations/{location_id}"

response = requests.get(url, headers=headers, timeout=30)

print(f"Status code: {response.status_code}")

if response.status_code != 200:
    print(response.text)
    response.raise_for_status()

data = response.json()

print("\nTop-level keys:")
print(data.keys())

print("\nLocation response preview:")
print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])