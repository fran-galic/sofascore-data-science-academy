
CREATE TABLE fgalic.daily_event_openings
(
    event_date String,
    event_id Int64,
    count SimpleAggregateFunction(sum, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (event_date, event_id);


CREATE MATERIALIZED VIEW fgalic.mv_daily_event_openings
TO fgalic.daily_event_openings
AS
SELECT
    event_date,
    id AS event_id,
    count() AS count
FROM bq.events
WHERE event_name = 'open_event'
GROUP BY
    event_date,
    event_id;


INSERT INTO fgalic.daily_event_openings
SELECT
    event_date,
    id AS event_id,
    count() AS count
FROM bq.events
WHERE event_name = 'open_event'
GROUP BY
    event_date,
    event_id;