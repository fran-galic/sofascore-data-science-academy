SELECT
    t.geo_country,
    t.player
FROM
(
    SELECT
        e.geo_country,
        p.name AS player,
        COUNT(*) AS follow_count
    FROM bq.events e
    JOIN sports.player p
        ON e.id = p.id
    WHERE e.event_name = 'follow_player'
      AND e.event_date >= '20240201'
      AND e.event_date < '20240301'
    GROUP BY
        e.geo_country,
        p.name
) t
JOIN
(
    SELECT
        geo_country,
        MAX(follow_count) AS max_follow_count
    FROM
    (
        SELECT
            e.geo_country,
            p.name AS player,
            COUNT(*) AS follow_count
        FROM bq.events e
        JOIN sports.player p
            ON e.id = p.id
        WHERE e.event_name = 'follow_player'
          AND e.event_date >= '20240201'
          AND e.event_date < '20240301'
        GROUP BY
            e.geo_country,
            p.name
    )
    GROUP BY geo_country
) m
    ON t.geo_country = m.geo_country
   AND t.follow_count = m.max_follow_count
ORDER BY t.geo_country;