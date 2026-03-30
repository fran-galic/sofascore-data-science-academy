-- Task 3 - Grafana upiti za tablicu fgalic.l4_dataset
-- Ako se koristi druga baza ili tablica, u upitima ispod treba promijeniti fgalic.l4_dataset.

-- 1) Bar chart
-- Naziv panela: Daily row count
SELECT
    toDate(parseDateTimeBestEffort(eventDate)) AS day,
    count() AS rows_count
FROM fgalic.l4_dataset
GROUP BY day
ORDER BY day;


-- 2) Table
-- Naziv panela: Table size
-- Prikazuje komprimiranu veličinu, nekomprimiranu veličinu, broj redaka i broj aktivnih partova.
SELECT
    database,
    table,
    formatReadableSize(sum(data_compressed_bytes)) AS compressed_size,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed_size,
    sum(rows) AS total_rows,
    count() AS active_parts
FROM system.parts
WHERE active = 1
  AND database = 'fgalic'
  AND table = 'l4_dataset'
GROUP BY database, table;


-- 3) Pie chart
-- Naziv panela: Column size share
-- Prikazuje koji stupci zauzimaju najviše prostora u tablici.
SELECT
    column AS column_name,
    sum(data_compressed_bytes) AS compressed_bytes
FROM system.parts_columns
WHERE active = 1
  AND database = 'fgalic'
  AND table = 'l4_dataset'
GROUP BY column_name
ORDER BY compressed_bytes DESC;


-- Bonus 1
-- Naziv panela: Top event names
--  vizualizacija: horizontalni bar chart
SELECT
    eventName,
    count() AS rows_count
FROM fgalic.l4_dataset
GROUP BY eventName
ORDER BY rows_count DESC
LIMIT 10;


-- Bonus 2
-- Naziv panela: Top countries
-- vizualizacija: bar chart ili pie chart
SELECT
    geoCountry,
    count() AS rows_count
FROM fgalic.l4_dataset
GROUP BY geoCountry
ORDER BY rows_count DESC
LIMIT 10;


-- Bonus 3
-- Naziv panela: Platform and status breakdown
-- vizualizacija: stacked bar chart - horizontal
SELECT
    platform,
    status,
    count() AS rows_count
FROM fgalic.l4_dataset
GROUP BY platform, status
ORDER BY platform, rows_count DESC;