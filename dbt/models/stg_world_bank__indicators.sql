with source as (
    select * from {{ source('raw', 'world_bank_indicators') }}
),

deduplicated as (
    select *
    from source
    qualify row_number() over (
        partition by indicator_id, country_iso3, year
        order by source_file desc
    ) = 1
)

select
    indicator_id,
    indicator_name,
    country_iso3,
    country_name,
    cast(year as integer) as year,
    value
from deduplicated