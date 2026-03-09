SELECT
    sp.name AS sport_name,
    COUNT(*) AS num_openings -- broji sve open_event zapise, tj. ukupan broj otvaranja sportskih događaja; ako bi se tražio broj različitih otvorenih utakmica, trebalo bi koristiti COUNT(DISTINCT bqe.id)
FROM bq.events bqe
JOIN sports.event spe
    ON bqe.id = spe.id
JOIN sports.sport sp
    ON spe.sport_id = sp.id
WHERE bqe.event_name = 'open_event'
  AND bqe.event_date >= '20240101'
  AND bqe.event_date < '20240201' -- filtriranje po rasponu radi i na stringu jer je datum u formatu YYYYMMDD
GROUP BY sp.name
ORDER BY num_openings DESC

-- baza će u pravilu prvo primijeniti WHERE filter (event_name i event_date)
-- i tek onda raditi JOIN, čime se smanjuje broj redaka koji ulaze u spajanje tablica