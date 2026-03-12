CREATE TABLE IF NOT EXISTS raw_api_responses (
    id UInt8,
    raw_json JSON
)
ENGINE = ReplacingMergeTree
ORDER BY id;

CREATE TABLE IF NOT EXISTS people (
    craft String,
    name String,
    _inserted_at DateTime
)
ENGINE = MergeTree
ORDER BY (craft, name, _inserted_at);

CREATE MATERIALIZED VIEW IF NOT EXISTS people_mv
TO people AS
SELECT
    JSONExtractString(toJSONString(raw_json), 'craft') AS craft,
    JSONExtractString(toJSONString(raw_json), 'name') AS name,
    now() AS _inserted_at
FROM raw_api_responses;
