select
    date_trunc(fct_encounter.admission_date, month) as encounter_month,
    dim_facility.facility_type,
    count(*) as encounter_count,
    avg(fct_encounter.encounter_cost) as avg_encounter_cost
from {{ ref('fct_encounter') }} as fct_encounter
inner join {{ ref('dim_facility') }} as dim_facility
    on fct_encounter.facility_key = dim_facility.facility_key
group by 1, 2
order by 1, 2

