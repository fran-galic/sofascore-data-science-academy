# Homework 4 - complete folder structure

```text
HW4/
├── README.md
├── task1/
│   ├── README.md
│   ├── docker-compose.yml
│   ├── clickhouse/
│   │   └── initdb/
│   │       └── 01-init.sql
│   └── grafana/
│       └── provisioning/
│           └── datasources/
│               └── clickhouse.yml
├── task2/
│   ├── README.md
│   ├── docker-compose-import.yml
│   └── importer/
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── helpers.py
│       ├── import_march_2024.py
│       └── data/
└── task3/
    ├── README.md
    ├── queries.sql
    └── dashboard.png
```

## Redoslijed rada

### 1. Task 1

```bash
cd HW4/task1
docker compose up -d
```

### 2. Task 2

```bash
cd ../task2
docker compose -f docker-compose-import.yml up --build
```

### 3. Task 3

- otvori Grafanu na `http://localhost:3000`
- login: `admin` / `admin`
- datasource bi već trebao biti provisionan
- napravi dashboard koristeći queryje iz `task3/queries.sql`
- spremi pravi screenshot kao `task3/dashboard.png`

## Brze provjere

### ClickHouse healthcheck

```bash
curl http://localhost:8123/ping
```

### Broj redaka u tablici

```bash
docker exec -it hw4-clickhouse clickhouse-client --user fgalic --password moja_lozinka --query "SELECT count() FROM fgalic.l4_dataset"
```
