CREATE TABLE fgalic.daily_user_activity
(
    event_date String,
    event_name String,
    user_pseudo_id String,
    geo_country String,
    platform Enum8('ANDROID' = 1, 'IOS' = 2, 'WEB' = 3),
    count UInt64
)
ENGINE = MergeTree()
ORDER BY (event_date, user_pseudo_id, event_name, geo_country, platform);


INSERT INTO fgalic.daily_user_activity
SELECT event_date, event_name, user_pseudo_id, geo_country, platform, COUNT(*) AS count
FROM bq.events
WHERE event_date >=  '20240201'  AND event_date < '20240301'
GROUP BY event_date, event_name ,user_pseudo_id, geo_country, platform




CREATE TABLE fgalic.monthly_user_activity
(
    event_date String,
    event_name String,
    user_pseudo_id String,
    geo_country String,
    platform Enum8('ANDROID' = 1, 'IOS' = 2, 'WEB' = 3),
    count UInt64
)
ENGINE = MergeTree()
ORDER BY (event_date, user_pseudo_id, event_name, geo_country, platform);


INSERT INTO fgalic.monthly_user_activity
SELECT
    month_date AS event_date,
    event_name,
    user_pseudo_id,
    geo_country,
    platform,
    count
FROM
(
    SELECT
        formatDateTime(
            toStartOfMonth(parseDateTimeBestEffort(event_date)),
            '%Y%m%d'
        ) AS month_date,
        event_name,
        user_pseudo_id,
        geo_country,
        platform,
        COUNT(*) AS count
    FROM bq.events
    WHERE event_date >= '20240201'
      AND event_date < '20240301'
    GROUP BY
        month_date,
        event_name,
        user_pseudo_id,
        geo_country,
        platform
)