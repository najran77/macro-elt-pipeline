-- One row per country and year.
select
    country_iso3,
    year,
    count(*) as row_count
from {{ ref('fct_country_indicators_yearly') }}
group by country_iso3, year
having count(*) > 1