-- A test fails if it returns at least one row.
-- Here: any indicator / country / year combination that appears more than once.
select
    indicator_id,
    country_iso3,
    year,
    count(*) as row_count
from {{ ref('stg_world_bank__indicators') }}
group by indicator_id, country_iso3, year
having count(*) > 1