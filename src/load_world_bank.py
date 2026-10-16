"""Load raw World Bank files into the DuckDB warehouse."""

from pathlib import Path

import duckdb

DB_PATH = Path("data/warehouse.duckdb")
RAW_FILES = "data/raw/world_bank/*/*.json"

LOAD_SQL = f"""
create schema if not exists raw;

create or replace table raw.world_bank_indicators as
select
    indicator.id      as indicator_id,
    indicator.value   as indicator_name,
    countryiso3code   as country_iso3,
    country.value     as country_name,
    date              as year,
    value,
    filename          as source_file,
    current_timestamp as loaded_at
from read_json(
    '{RAW_FILES}',
    format = 'array',
    filename = true,
    columns = {{
        indicator: 'STRUCT(id VARCHAR, value VARCHAR)',
        country: 'STRUCT(id VARCHAR, value VARCHAR)',
        countryiso3code: 'VARCHAR',
        date: 'VARCHAR',
        value: 'DOUBLE',
        unit: 'VARCHAR',
        obs_status: 'VARCHAR',
        decimal: 'INTEGER'
    }}
);
"""


def load():
    """(Re)build the raw table from all raw files."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(LOAD_SQL)
        count = con.execute("select count(*) from raw.world_bank_indicators").fetchone()[0]
    print(f"raw.world_bank_indicators: {count} rows loaded")


if __name__ == "__main__":
    load()