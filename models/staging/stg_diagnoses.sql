-- depends_on: {{ ref('raw_diagnosis') }}

select
    trim(diagnosis_event_id) as diagnosis_event_id,
    trim(encounter_id) as encounter_id,
    upper(trim(diagnosis_code)) as diagnosis_code,
    trim(diagnosis_name) as diagnosis_name,
    trim(diagnosis_group) as diagnosis_group,
    trim(diagnosis_type) as diagnosis_type,
    cast(diagnosis_event_date as date) as diagnosis_event_date
from {{ source('raw_healthcare', 'raw_diagnosis') }}
