SELECT
    bqe.id AS id,
    COUNT(*) AS number_of_openings
FROM bq.events bqe
JOIN sports.event spe
    ON bqe.id = spe.id
JOIN sports.tournament t
    ON spe.tournament_id = t.id
JOIN sports.uniquetournament ut
    ON t.uniquetournament_id = ut.id
WHERE bqe.event_name = 'open_event'
  AND ut.name = 'HNL'
  AND t.name = 'HNL'
  AND spe.startdate >= '2023-07-01 00:00:00'
  AND spe.startdate < '2024-07-01 00:00:00'
GROUP BY bqe.id
ORDER BY number_of_openings DESC
LIMIT 1