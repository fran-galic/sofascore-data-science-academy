WITH weekly_sport_openings AS
(
    SELECT
        toMonday(toDate(parseDateTimeBestEffort(event_date))) AS week,
        dictGet(
            'fgalic.sport_dictionary',
            'name',
            toUInt64(
                ifNull(
                    dictGet('fgalic.event_dictionary', 'sport_id', toUInt64(event_id)),
                    0
                )
            )
        ) AS sport,
        sum(count) AS weekly_count
    FROM fgalic.daily_event_openings
    WHERE event_date BETWEEN '20240101' AND '20240128'
    GROUP BY
        week,
        sport
)

SELECT
    week,
    sport,
    weekly_count,
    rank() OVER (PARTITION BY week ORDER BY weekly_count DESC) AS rank
FROM weekly_sport_openings
ORDER BY
    week,
    rank;