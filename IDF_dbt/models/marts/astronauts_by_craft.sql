with latest_people as (
    select
        craft,
        astronaut_name,
        loaded_at,
        row_number() over (
            partition by astronaut_name
            order by loaded_at desc
        ) as row_num
    from {{ ref('stg_people') }}
)
select
    craft,
    count(*) as astronaut_count,
    groupArray(astronaut_name) as astronaut_names,
    max(loaded_at) as snapshot_loaded_at
from latest_people
where row_num = 1
group by craft
order by craft
