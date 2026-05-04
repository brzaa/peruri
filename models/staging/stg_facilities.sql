-- depends_on: {{ ref('raw_facility') }}

select
    trim(facility_id) as facility_id,
    trim(facility_name) as facility_name,
    trim(facility_type) as facility_type,
    trim(city) as city,
    trim(province) as province,
    trim(ownership_type) as ownership_type
from {{ source('raw_healthcare', 'raw_facility') }}
