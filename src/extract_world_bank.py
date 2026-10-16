"""Extract economic indicators from the World Bank API."""

import requests
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://api.worldbank.org/v2"
# Countries to track (ISO 3166-1 alpha-3 codes)
COUNTRIES = ["USA", "FRA", "DEU", "GBR", "JPN", "CHN", "IND", "BRA", "MEX", "ZAF", "KOR", "TUR","MDG"]

# World Bank indicators to extract
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current US$)",
    "NY.GDP.PCAP.CD": "GDP per capita (current US$)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "SP.POP.TOTL": "Population, total",
    "SL.UEM.TOTL.ZS": "Unemployment (% of labor force)",
}

START_YEAR = 2000
END_YEAR = 2025
RAW_DIR = Path("data/raw/world_bank")
def fetch_page(country, indicator, start_year, end_year, page=1, per_page=50):
    """Fetch one page of results for an indicator."""
    url = f"{BASE_URL}/country/{country}/indicator/{indicator}"
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "page": page,
        "per_page": per_page,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def fetch_all_pages(country, indicator, start_year, end_year, per_page=1000):
    """Fetch every page of an indicator and return all records in a single list."""
    all_records = []
    page = 1
    while True:
        metadata, records = fetch_page(
            country, indicator, start_year, end_year, page=page, per_page=per_page
        )
        # The API returns None instead of an empty list when there is no data
        all_records.extend(records or [])
        if page >= metadata["pages"]:
            break
        page += 1
    return all_records

def save_raw(records, indicator, extracted_at):
    """Save raw API records to a JSON file, partitioned by ingestion date."""
    folder = RAW_DIR / f"ingestion_date={extracted_at:%Y-%m-%d}"
    folder.mkdir(parents=True, exist_ok=True)
    file_name = f"{indicator.replace('.', '_')}__{extracted_at:%Y%m%dT%H%M%SZ}.json"
    path = folder / file_name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)
    return path

if __name__ == "__main__":
    extracted_at = datetime.now(timezone.utc)
    countries = ";".join(COUNTRIES)
    for indicator, name in INDICATORS.items():
        records = fetch_all_pages(countries, indicator, START_YEAR, END_YEAR)
        path = save_raw(records, indicator, extracted_at)
        print(f"{indicator}: {len(records)} records saved to {path}")