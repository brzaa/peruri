select
    {{ surrogate_key(['diagnosis_code']) }} as diagnosis_key,
    diagnosis_code,
    any_value(diagnosis_name) as diagnosis_name,
    any_value(diagnosis_group) as diagnosis_group
from {{ ref('stg_diagnoses') }}
group by diagnosis_code

