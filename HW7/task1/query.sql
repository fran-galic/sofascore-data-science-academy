WITH user_daily_events AS (
    SELECT
        toDate(parseDateTimeBestEffort(e.event_date)) AS ev_date,
        e.user_pseudo_id,
        uniqExact(e.id) AS different_events_opened
    FROM bq.events e
    INNER JOIN sports.event se
        ON se.id = toInt32(e.id)
    INNER JOIN sports.sport s
        ON s.id = se.sport_id
    WHERE e.event_name = 'open_event'
      AND e.platform = 'IOS'
      AND e.geo_country = 'Croatia'
      AND e.event_date BETWEEN '20240101' AND '20240530'
      AND s.name = 'Football'
    GROUP BY
        ev_date,
        e.user_pseudo_id
)

SELECT
    ev_date,
    round(avg(different_events_opened), 4) AS avg_events_per_user
FROM user_daily_events
GROUP BY ev_date
ORDER BY ev_date;
