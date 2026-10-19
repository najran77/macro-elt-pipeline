select
    country_iso3,
    country_name,
    region,
    currency_code
from {{ ref('country_reference') }}