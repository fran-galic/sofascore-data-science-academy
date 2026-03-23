CREATE TABLE fgalic.daily_entity_follows
(
    event_date String,
    entity LowCardinality(String),
    name Nullable(String),
    count SimpleAggregateFunction(sum, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (event_date, entity, name);


CREATE MATERIALIZED VIEW fgalic.mv_daily_entity_follows
TO fgalic.daily_entity_follows
AS
SELECT
    event_date,
    multiIf(
        event_name = 'follow_team', 'team',
        event_name = 'follow_player', 'player',
        event_name = 'follow_league', 'league',
        'unknown'
    ) AS entity,
    multiIf(
        event_name = 'follow_team',
            dictGet('fgalic.team_dictionary', 'name', toUInt64(id)),
        event_name = 'follow_player',
            dictGet('fgalic.player_dictionary', 'name', toUInt64(id)),
        event_name = 'follow_league',
            dictGet('fgalic.uniquetournament_dictionary', 'name', toUInt64(id)),
        CAST(NULL, 'Nullable(String)')
    ) AS name,
    count() AS count
FROM bq.events
WHERE event_name IN ('follow_team', 'follow_player', 'follow_league')
GROUP BY
    event_date,
    entity,
    name;


INSERT INTO fgalic.daily_entity_follows
SELECT
    event_date,
    multiIf(
        event_name = 'follow_team', 'team',
        event_name = 'follow_player', 'player',
        event_name = 'follow_league', 'league',
        'unknown'
    ) AS entity,
    multiIf(
        event_name = 'follow_team',
            dictGet('fgalic.team_dictionary', 'name', toUInt64(id)),
        event_name = 'follow_player',
            dictGet('fgalic.player_dictionary', 'name', toUInt64(id)),
        event_name = 'follow_league',
            dictGet('fgalic.uniquetournament_dictionary', 'name', toUInt64(id)),
        CAST(NULL, 'Nullable(String)')
    ) AS name,
    count() AS count
FROM bq.events
WHERE event_name IN ('follow_team', 'follow_player', 'follow_league')
GROUP BY
    event_date,
    entity,
    name;