CREATE TABLE fgalic.daily_event_activity
(
    event_date String,
    event_name String,
    geo_country String,
    platform String,
    count UInt64,
    user_count UInt64
)
ENGINE = MergeTree()
ORDER BY (event_date, event_name, geo_country, platform);

INSERT INTO fgalic.daily_event_activity
SELECT
    event_date,
    event_name,
    geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, event_name, geo_country, platform

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, geo_country, platform

UNION ALL

SELECT
    event_date,
    event_name,
    '<all>' AS geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, event_name, platform

UNION ALL

SELECT
    event_date,
    event_name,
    geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, event_name, geo_country

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    '<all>' AS geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, platform

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, geo_country

UNION ALL

SELECT
    event_date,
    event_name,
    '<all>' AS geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date, event_name

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    '<all>' AS geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.daily_user_activity
GROUP BY event_date;




CREATE TABLE fgalic.monthly_event_activity
(
    event_date String,
    event_name String,
    geo_country String,
    platform String,
    count UInt64,
    user_count UInt64
)
ENGINE = MergeTree()
ORDER BY (event_date, event_name, geo_country, platform);

INSERT INTO fgalic.monthly_event_activity
SELECT
    event_date,
    event_name,
    geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, event_name, geo_country, platform

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, geo_country, platform

UNION ALL

SELECT
    event_date,
    event_name,
    '<all>' AS geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, event_name, platform

UNION ALL

SELECT
    event_date,
    event_name,
    geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, event_name, geo_country

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    '<all>' AS geo_country,
    platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, platform

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, geo_country

UNION ALL

SELECT
    event_date,
    event_name,
    '<all>' AS geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date, event_name

UNION ALL

SELECT
    event_date,
    '<all>' AS event_name,
    '<all>' AS geo_country,
    '<all>' AS platform,
    SUM(count) AS count,
    uniqExact(user_pseudo_id) AS user_count
FROM fgalic.monthly_user_activity
GROUP BY event_date;