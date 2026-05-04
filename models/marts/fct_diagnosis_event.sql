{% set enable_partitioned_facts = var('enable_partitioned_facts', false) %}

{% if enable_partitioned_facts %}
{{ config(
    partition_by={"field": "diagnosis_event_date", "data_type": "date"},
    cluster_by=["facility_key", "diagnosis_key"]
) }}
{% else %}
{{ config(
    cluster_by=["facility_key", "diagnosis_key"]
) }}
{% endif %}

select
    {{ surrogate_key(['diagnosis.diagnosis_event_id']) }} as diagnosis_event_key,
    diagnosis.diagnosis_event_id,
    encounter_fact.encounter_key,
    patient_dim.patient_key,
    facility_dim.facility_key,
    diagnosis_dim.diagnosis_key,
    cast(format_date('%Y%m%d', diagnosis.diagnosis_event_date) as int64) as diagnosis_event_date_key,
    diagnosis.diagnosis_event_date,
    diagnosis.diagnosis_type,
    diagnosis.diagnosis_code,
    diagnosis.diagnosis_group
from {{ ref('stg_diagnoses') }} as diagnosis
inner join {{ ref('stg_encounters') }} as encounter
    on diagnosis.encounter_id = encounter.encounter_id
inner join {{ ref('fct_encounter') }} as encounter_fact
    on diagnosis.encounter_id = encounter_fact.encounter_id
inner join {{ ref('dim_patient') }} as patient_dim
    on encounter.patient_id = patient_dim.patient_id
inner join {{ ref('dim_facility') }} as facility_dim
    on encounter.facility_id = facility_dim.facility_id
inner join {{ ref('dim_diagnosis') }} as diagnosis_dim
    on diagnosis.diagnosis_code = diagnosis_dim.diagnosis_code
