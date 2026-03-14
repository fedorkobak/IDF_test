SELECT
    craft,
    name as astronaut_name,
    _inserted_at as loaded_at
FROM {{ source('astronaut_api', 'people') }}
where craft != ''
  and name != ''
