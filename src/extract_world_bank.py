"""Extract economic indicators from the World Bank API."""

import requests

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


if __name__ == "__main__":
    countries = ";".join(COUNTRIES)
    for indicator, name in INDICATORS.items():
        records = fetch_all_pages(countries, indicator, START_YEAR, END_YEAR)
        print(f"{indicator} ({name}): {len(records)} records")
        missing = sum(1 for r in records if r["value"] is None)
        print(f"   of which {missing} without value")