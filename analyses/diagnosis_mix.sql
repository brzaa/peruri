select
    date_trunc(fct_diagnosis_event.diagnosis_event_date, month) as diagnosis_month,
    dim_facility.facility_type,
    dim_diagnosis.diagnosis_group,
    countif(fct_diagnosis_event.diagnosis_type = 'primary') as primary_diagnosis_events,
    count(*) as diagnosis_event_count
from {{ ref('fct_diagnosis_event') }} as fct_diagnosis_event
inner join {{ ref('dim_diagnosis') }} as dim_diagnosis
    on fct_diagnosis_event.diagnosis_key = dim_diagnosis.diagnosis_key
inner join {{ ref('dim_facility') }} as dim_facility
    on fct_diagnosis_event.facility_key = dim_facility.facility_key
group by 1, 2, 3
order by 1, 2, 5 desc

