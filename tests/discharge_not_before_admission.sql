select
    encounter_id,
    admission_date,
    discharge_date
from {{ ref('fct_encounter') }}
where discharge_date < admission_date

