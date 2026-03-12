CREATE TABLE IF NOT EXISTS raw_api_responses (
    id UInt8,
    raw_json JSON
)
ENGINE = ReplacingMergeTree
ORDER BY id;
