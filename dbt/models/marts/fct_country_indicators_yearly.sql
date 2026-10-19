with indicators as (
    select * from {{ ref('stg_world_bank__indicators') }}
)

select
    country_iso3,
    year,
    max(case when indicator_id = 'NY.GDP.MKTP.CD' then value end) as gdp_usd,
    max(case when indicator_id = 'NY.GDP.PCAP.CD' then value end) as gdp_per_capita_usd,
    max(case when indicator_id = 'FP.CPI.TOTL.ZG' then value end) as inflation_pct,
    cast(max(case when indicator_id = 'SP.POP.TOTL' then value end) as bigint) as population,
    max(case when indicator_id = 'SL.UEM.TOTL.ZS' then value end) as unemployment_pct
from indicators
group by country_iso3, year