-- depends_on: {{ ref('raw_patient') }}

select
    trim(patient_id) as patient_id,
    trim(gender) as gender,
    cast(birth_date as date) as birth_date,
    trim(city) as city,
    trim(province) as province,
    trim(insurance_class) as insurance_class,
    cast(registered_at as date) as registered_at,
    date_diff(date('2025-12-31'), cast(birth_date as date), year) as age_at_2025_end,
    case
        when date_diff(date('2025-12-31'), cast(birth_date as date), year) < 18 then '0-17'
        when date_diff(date('2025-12-31'), cast(birth_date as date), year) < 35 then '18-34'
        when date_diff(date('2025-12-31'), cast(birth_date as date), year) < 50 then '35-49'
        when date_diff(date('2025-12-31'), cast(birth_date as date), year) < 65 then '50-64'
        else '65+'
    end as age_band
from {{ source('raw_healthcare', 'raw_patient') }}
