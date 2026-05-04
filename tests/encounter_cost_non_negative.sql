select
    encounter_id,
    encounter_cost
from {{ ref('fct_encounter') }}
where encounter_cost < 0

