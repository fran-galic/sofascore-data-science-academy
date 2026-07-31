# SofaScore Data Science Academy

This repository contains my assignments and project work from the 2026 SofaScore Data Science Academy. The nine assignments follow the course progression from product analytics and SQL to data engineering, experimentation, forecasting, machine learning, and recommendation systems.

It is an educational portfolio repository, not an official SofaScore product or production codebase. Solutions and selected generated outputs are included; source datasets, course handouts, credentials, local environments, and trained model artifacts are intentionally excluded.

## Repository map

| Area | Focus | Main artifacts |
|---|---|---|
| [`HW1`](HW1) | Product analytics, event-tracking proposals, and analytical SQL | Markdown, SQL |
| [`HW2`](HW2) | SFTP ingestion, archive extraction, data cleaning, chunked processing, and ClickHouse loading | Python |
| [`HW3`](HW3) | ClickHouse dictionaries, materialized views, daily and monthly aggregates, and analytical queries | SQL |
| [`HW4`](HW4) | Local ClickHouse and Grafana infrastructure, a containerized import pipeline, and dashboard development | Docker Compose, Python, SQL, screenshots |
| [`HW5`](HW5) | Investigation of a weekly active user decline by acquisition source and user segment | Report, charts |
| [`HW6`](HW6) | A/B test analysis with sample-ratio mismatch checks, statistical testing, guardrails, and a rollout recommendation | Report |
| [`HW7`](HW7) | Time-series decomposition, stationarity testing, ARIMA and exponential-smoothing forecasts, baselines, and dashboard exports | Notebook, SQL, CSV, charts |
| [`HW8`](HW8) | Paid-versus-organic acquisition classification with model comparison and threshold tuning | Notebook |
| [`HW9`](HW9) | Weekly football event recommendations using followed teams, Jaccard similarity, MCC-based neighborhoods, and popularity fallbacks | Notebook |

Each assignment is kept in its own directory. SQL files contain the database work, Python scripts implement ingestion and processing pipelines, notebooks document the modeling workflow, and reports summarize the reasoning and conclusions.

## Technical scope

The work spans:

- SQL analytics and ClickHouse data modeling
- Python data processing with pandas and Paramiko
- Docker Compose, ClickHouse, Grafana, and Superset-ready exports
- experiment analysis and statistical hypothesis testing
- time-series forecasting with classical statistical models
- classification with linear, tree-based, XGBoost, and CatBoost models
- rule-based and collaborative recommendation methods
- analytical communication through reports, tables, and visualizations

## Running the code

The base project targets Python 3.12 and uses `uv` for dependency management:

```bash
uv sync
```

The assignments were developed as separate pieces of coursework. Some notebooks therefore require additional task-specific packages such as Jupyter, Matplotlib, statsmodels, scikit-learn, XGBoost, or CatBoost. The Docker workflow in `HW4` has detailed instructions in its task-level README files.

The datasets required to reproduce the results are not distributed in this repository. Place only authorized local datasets in the paths expected by each task; those paths are ignored by Git.

## Configuration and security

Remote connections are configured through environment variables rather than committed values. Depending on the task, the relevant variables are:

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

Do not commit `.env` files, downloaded datasets, model artifacts, private keys, or notebook outputs containing user-level data. The local services in `HW4/task1` are bound to `127.0.0.1` and require passwords to be provided through the environment.

## License

The original code and written solutions are available under the [MIT License](LICENSE). Third-party datasets and course materials are not included and remain subject to their respective terms.
