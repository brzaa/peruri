{% set enable_partitioned_facts = var('enable_partitioned_facts', false) %}

{% if enable_partitioned_facts %}
{{ config(
    partition_by={"field": "admission_date", "data_type": "date"},
    cluster_by=["facility_key", "patient_key"]
) }}
{% else %}
{{ config(
    cluster_by=["facility_key", "patient_key"]
) }}
{% endif %}

with encounter_base as (
    select
        encounter_id,
        patient_id,
        facility_id,
        admission_date,
        discharge_date,
        length_of_stay,
        encounter_cost,
        payer_type,
        class_of_care,
        lag(discharge_date) over (
            partition by patient_id
            order by admission_date, encounter_id
        ) as previous_discharge_date
    from {{ ref('stg_encounters') }}
)

select
    {{ surrogate_key(['encounter_base.encounter_id']) }} as encounter_key,
    encounter_base.encounter_id,
    patient_dim.patient_key,
    facility_dim.facility_key,
    cast(format_date('%Y%m%d', encounter_base.admission_date) as int64) as admission_date_key,
    cast(format_date('%Y%m%d', encounter_base.discharge_date) as int64) as discharge_date_key,
    encounter_base.admission_date,
    encounter_base.discharge_date,
    encounter_base.length_of_stay,
    encounter_base.encounter_cost,
    encounter_base.payer_type,
    encounter_base.class_of_care,
    encounter_base.previous_discharge_date,
    case
        when encounter_base.previous_discharge_date is not null
            and date_diff(encounter_base.admission_date, encounter_base.previous_discharge_date, day) between 0 and 30
        then true
        else false
    end as revisit_within_30d_flag
from encounter_base
inner join {{ ref('dim_patient') }} as patient_dim
    on encounter_base.patient_id = patient_dim.patient_id
inner join {{ ref('dim_facility') }} as facility_dim
    on encounter_base.facility_id = facility_dim.facility_id
