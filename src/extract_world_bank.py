"""Extract economic indicators from the World Bank API."""

import requests

BASE_URL = "https://api.worldbank.org/v2"


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
    records = fetch_all_pages("FRA;DEU", "SP.POP.TOTL", 2018, 2023, per_page=5)
    print(f"{len(records)} records fetched")
    for record in records:
        print(record["country"]["value"], record["date"], record["value"])