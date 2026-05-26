CREATE TABLE IF NOT EXISTS fgalic.hw7_forecast_results
(
    ev_date Date,
    method String,
    series_type String,
    value Nullable(Float64),
    actual_value Nullable(Float64),
    forecast_value Nullable(Float64),
    is_forecast UInt8,
    forecast_day Nullable(UInt8),
    forecast_week Nullable(UInt8),
    previous_week_actual Nullable(Float64),
    wow_change Nullable(Float64),
    wow_change_percent Nullable(Float64)
)
ENGINE = MergeTree
ORDER BY (method, ev_date, series_type);
