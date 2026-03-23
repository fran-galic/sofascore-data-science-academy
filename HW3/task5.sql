
CREATE TABLE fgalic.daily_event_activity
(
    event_date String CODEC(ZSTD(1)),
    event_name LowCardinality(String),
    geo_country LowCardinality(String),
    platform LowCardinality(String),
    count UInt64 CODEC(T64),
    user_count UInt64 CODEC(T64)
)
ENGINE = MergeTree
PARTITION BY substring(event_date, 1, 6)
ORDER BY (event_date, event_name, geo_country, platform)
SETTINGS index_granularity = 8192;


CREATE TABLE fgalic.monthly_event_activity
(
    month String CODEC(ZSTD(1)),
    event_name LowCardinality(String),
    geo_country LowCardinality(String),
    platform LowCardinality(String),
    count UInt64 CODEC(T64),
    user_count UInt64 CODEC(T64)
)
ENGINE = MergeTree
PARTITION BY substring(month, 1, 6)
ORDER BY (month, event_name, geo_country, platform)
SETTINGS index_granularity = 8192;


INSERT INTO fgalic.daily_event_activity
SELECT
    event_date,
    if(isNull(event_name) OR event_name = '', '<all>', event_name) AS event_name,
    if(isNull(geo_country) OR geo_country = '', '<all>', geo_country) AS geo_country,
    if(isNull(platform) OR platform = '', '<all>', platform) AS platform,
    count,
    user_count
FROM
(
    SELECT
        event_date,
        event_name,
        geo_country,
        toString(platform) AS platform,
        sum(count) AS count,
        uniqExact(user_pseudo_id) AS user_count
    FROM aggregations.daily_user_activity
    GROUP BY GROUPING SETS
    (
        (event_date, event_name, geo_country, platform),
        (event_date, event_name, geo_country),
        (event_date, event_name, platform),
        (event_date, geo_country, platform),
        (event_date, event_name),
        (event_date, geo_country),
        (event_date, platform),
        (event_date)
    )
    SETTINGS group_by_use_nulls = 1
);


INSERT INTO fgalic.monthly_event_activity
SELECT
    month,
    if(isNull(event_name) OR event_name = '', '<all>', event_name) AS event_name,
    if(isNull(geo_country) OR geo_country = '', '<all>', geo_country) AS geo_country,
    if(isNull(platform) OR platform = '', '<all>', platform) AS platform,
    count,
    user_count
FROM
(
    SELECT
        event_date AS month,
        event_name,
        geo_country,
        toString(platform) AS platform,
        sum(count) AS count,
        uniqExact(user_pseudo_id) AS user_count
    FROM aggregations.monthly_user_activity
    GROUP BY GROUPING SETS
    (
        (month, event_name, geo_country, platform),
        (month, event_name, geo_country),
        (month, event_name, platform),
        (month, geo_country, platform),
        (month, event_name),
        (month, geo_country),
        (month, platform),
        (month)
    )
    SETTINGS group_by_use_nulls = 1
);