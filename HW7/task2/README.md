# HW7 Task 2

This task uses the forecast output prepared in Task 1.

- ClickHouse table: `fgalic.hw7_forecast_results`
- Input file for import: `forecast_results_for_superset.csv`
- Superset dashboard includes:
  - `Actual & Forecast`
  - `Forecast WoW Change`
  - `WoW Change`
- Dashboard filter: `method` with forecast methods `ARIMA`, `ES`, `naive`, `seasonal_naive`, and `mean`
