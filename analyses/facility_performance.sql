select
    dim_facility.facility_name,
    dim_facility.facility_type,
    count(*) as encounter_count,
    avg(fct_encounter.length_of_stay) as avg_length_of_stay,
    avg(fct_encounter.encounter_cost) as avg_encounter_cost,
    sum(case when fct_encounter.revisit_within_30d_flag then 1 else 0 end) as revisit_30d_count,
    safe_divide(
        sum(case when fct_encounter.revisit_within_30d_flag then 1 else 0 end),
        count(*)
    ) as revisit_30d_rate
from {{ ref('fct_encounter') }} as fct_encounter
inner join {{ ref('dim_facility') }} as dim_facility
    on fct_encounter.facility_key = dim_facility.facility_key
group by 1, 2
order by encounter_count desc, avg_encounter_cost desc

