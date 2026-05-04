select
    {{ surrogate_key(['patient_id']) }} as patient_key,
    patient_id,
    gender,
    birth_date,
    age_at_2025_end,
    age_band,
    insurance_class,
    city,
    province,
    registered_at
from {{ ref('stg_patients') }}

