select
    {{ surrogate_key(['facility_id']) }} as facility_key,
    facility_id,
    facility_name,
    facility_type,
    ownership_type,
    city,
    province
from {{ ref('stg_facilities') }}

