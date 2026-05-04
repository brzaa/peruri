select
    encounter_id,
    length_of_stay
from {{ ref('fct_encounter') }}
where length_of_stay < 0

