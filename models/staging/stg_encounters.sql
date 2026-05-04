-- depends_on: {{ ref('raw_encounter') }}

select
    trim(encounter_id) as encounter_id,
    trim(patient_id) as patient_id,
    trim(facility_id) as facility_id,
    cast(admission_date as date) as admission_date,
    cast(discharge_date as date) as discharge_date,
    cast(length_of_stay as int64) as length_of_stay,
    cast(encounter_cost as numeric) as encounter_cost,
    trim(payer_type) as payer_type,
    trim(class_of_care) as class_of_care
from {{ source('raw_healthcare', 'raw_encounter') }}
