# SofaScore Data Science Academy

This repository contains my assignments and project work from the 2026 SofaScore Data Science Academy. It follows the course progression from product analytics and SQL through data pipelines, experimentation, forecasting, machine learning, and recommendation systems.

The repository contains solutions and selected generated outputs. Source datasets, course handouts, credentials, local environments, and trained model artifacts are intentionally excluded.

## Repository structure

| Directory | Topics |
|---|---|
| `HW1` | Product analytics, event tracking proposals, and analytical SQL |
| `HW2` | Python ingestion over SFTP, archive extraction, data cleaning, chunked processing, and ClickHouse loading |
| `HW3` | ClickHouse dictionaries, materialized views, daily and monthly aggregates, and analytical queries |
| `HW4` | Dockerized ClickHouse and Grafana setup, a containerized import pipeline, dashboard queries, and screenshots |
| `HW5` | Investigation of a weekly active user decline, including acquisition-source and segment analysis |
| `HW6` | A/B test analysis with sample-ratio mismatch checks, statistical testing, guardrails, and a rollout recommendation |
| `HW7` | Time-series decomposition, stationarity checks, ARIMA and exponential-smoothing forecasts, baselines, and dashboard-ready exports |
| `HW8` | Classification of paid versus organic acquisition using linear, tree-based, and CatBoost models with threshold tuning |
| `HW9` | Weekly football event recommendations using followed teams, Jaccard similarity, MCC-based neighborhoods, and popularity fallbacks |

Most directories are self-contained. SQL files hold the database work, Python scripts implement ingestion and processing pipelines, notebooks document the modeling workflow, and Markdown or PDF reports summarize findings.

## Running the code

The base project targets Python 3.12 and uses `uv` for dependency management:

```bash
uv sync
```

Some notebooks use additional assignment-specific libraries such as Jupyter, Matplotlib, statsmodels, scikit-learn, XGBoost, or CatBoost. The Docker setup for `HW4` has task-level instructions in its local README files.

The data needed to reproduce the assignments is not distributed in this repository. Place authorized local datasets in the paths expected by the relevant task. Those paths are ignored by Git.

## Configuration and security

Remote services are configured through environment variables rather than committed values. Depending on the task, the relevant variables are:

```text
SSH_HOST
SSH_USERNAME
SSH_PASSWORD
REMOTE_DIR_PATH
CLICKHOUSE_HOST
CLICKHOUSE_PORT
CLICKHOUSE_USER
CLICKHOUSE_PASSWORD
CLICKHOUSE_DATABASE
CLICKHOUSE_TABLE
CH_HOST
CH_PORT
CH_USER
CH_PASSWORD
CH_SCHEME
```

Do not commit `.env` files, downloaded datasets, model artifacts, private keys, or notebook outputs containing user-level data. The local Docker services in `HW4/task1` are bound to `127.0.0.1` and require passwords to be supplied through the environment.

## License

The original code and written solutions in this repository are available under the MIT License. Third-party datasets and course materials are not included and remain subject to their respective terms.
