{% macro surrogate_key(columns) -%}
to_hex(
    md5(
        concat(
            {%- for column in columns -%}
                coalesce(cast({{ column }} as string), '__dbt_null__')
                {%- if not loop.last %}, '||', {% endif -%}
            {%- endfor -%}
        )
    )
)
{%- endmacro %}

