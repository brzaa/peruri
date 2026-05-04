with date_spine as (
    select date_day
    from unnest(generate_date_array(date('2024-01-01'), date('2025-12-31'))) as date_day
)

select
    cast(format_date('%Y%m%d', date_day) as int64) as date_key,
    date_day,
    extract(year from date_day) as calendar_year,
    extract(quarter from date_day) as calendar_quarter,
    extract(month from date_day) as calendar_month,
    format_date('%Y-%m', date_day) as year_month,
    extract(day from date_day) as day_of_month,
    format_date('%A', date_day) as day_name,
    case
        when extract(dayofweek from date_day) in (1, 7) then true
        else false
    end as is_weekend
from date_spine

