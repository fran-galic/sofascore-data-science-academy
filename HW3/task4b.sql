WITH weekly_follows AS
(
    SELECT
        entity,
        name,
        sum(count) AS total_count
    FROM fgalic.daily_entity_follows
    WHERE event_date BETWEEN '20240115' AND '20240121'
    GROUP BY
        entity,
        name
),
ranked_follows AS
(
    SELECT
        entity,
        name,
        total_count,
        row_number() OVER (PARTITION BY entity ORDER BY total_count DESC) AS rank
    FROM weekly_follows
)

SELECT
    entity,
    name,
    total_count,
    rank
FROM ranked_follows
WHERE rank <= 10
ORDER BY
    entity,
    rank;